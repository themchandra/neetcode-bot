"""
NeetCode Daily Discord Bot
──────────────────────────
Posts one NeetCode 150 problem every day at 8 AM Pacific.
Tracks completions per member via a "Mark Complete" button.
Provides /daily, /random, and /stats slash commands.
"""

from __future__ import annotations

import os
import re
import logging
from datetime import datetime, timezone

import discord
from discord import app_commands
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

import database as db
from problems import PROBLEMS, DIFFICULTY_EMOJI, TOPIC_EMOJI

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

load_dotenv()

TOKEN      = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
# Optional: comma-separated Discord user IDs to @mention in daily posts
MEMBER_IDS_RAW = os.environ.get("MEMBER_IDS", "")
MEMBER_IDS: list[int] = [
    int(x.strip()) for x in MEMBER_IDS_RAW.split(",") if x.strip()
]

PACIFIC_TZ = pytz.timezone("America/Los_Angeles")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("neetcode-bot")

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def today_pacific() -> str:
    """Return today's date in Pacific time as YYYY-MM-DD."""
    return datetime.now(PACIFIC_TZ).strftime("%Y-%m-%d")


def build_challenge_embed(
    challenge: dict,
    completions: list[dict],
    total_members: int,
) -> discord.Embed:
    """Construct the rich embed for a daily challenge message."""
    problem     = challenge
    diff        = problem["difficulty"]
    topic       = problem["topic"]
    diff_emoji  = DIFFICULTY_EMOJI.get(diff, "⬜")
    topic_emoji = TOPIC_EMOJI.get(topic, "📌")

    # Colour by difficulty
    colour = {
        "Easy":   discord.Colour.green(),
        "Medium": discord.Colour.gold(),
        "Hard":   discord.Colour.red(),
    }.get(diff, discord.Colour.blurple())

    embed = discord.Embed(
        title=f"📅 Daily Challenge — {challenge['challenge_date']}",
        colour=colour,
    )
    embed.add_field(
        name="Problem",
        value=f"[{problem['name']}]({problem['url']})",
        inline=False,
    )
    embed.add_field(
        name="Difficulty",
        value=f"{diff_emoji} {diff}",
        inline=True,
    )
    embed.add_field(
        name="Topic",
        value=f"{topic_emoji} {topic}",
        inline=True,
    )

    # Completion tracker
    count      = len(completions)
    done_names = ", ".join(c["username"] for c in completions) if completions else "—"
    bar        = _progress_bar(count, total_members)
    embed.add_field(
        name=f"Completions  {bar}  {count}/{total_members}",
        value=done_names,
        inline=False,
    )

    embed.set_footer(text="Click ✅ to mark yourself complete • toggle to undo")
    return embed


def build_random_embed(problem: dict) -> discord.Embed:
    """Construct a simple embed for /random output."""
    diff        = problem["difficulty"]
    topic       = problem["topic"]
    diff_emoji  = DIFFICULTY_EMOJI.get(diff, "⬜")
    topic_emoji = TOPIC_EMOJI.get(topic, "📌")

    colour = {
        "Easy":   discord.Colour.green(),
        "Medium": discord.Colour.gold(),
        "Hard":   discord.Colour.red(),
    }.get(diff, discord.Colour.blurple())

    embed = discord.Embed(title="🎲 Random Blind 75 Problem", colour=colour)
    embed.add_field(
        name="Problem",
        value=f"[{problem['name']}]({problem['url']})",
        inline=False,
    )
    embed.add_field(name="Difficulty", value=f"{diff_emoji} {diff}", inline=True)
    embed.add_field(name="Topic", value=f"{topic_emoji} {topic}", inline=True)
    return embed


def _progress_bar(done: int, total: int, length: int = 5) -> str:
    filled = round(done / total * length) if total else 0
    return "█" * filled + "░" * (length - filled)


# ─────────────────────────────────────────────────────────────────────────────
# Persistent "Mark Complete" button (DynamicItem)
# Encodes the challenge date in the custom_id so old buttons auto-expire.
# ─────────────────────────────────────────────────────────────────────────────

class CompleteButton(
    discord.ui.DynamicItem[discord.ui.Button],
    template=r"complete:(?P<date>\d{4}-\d{2}-\d{2})",
):
    """
    A persistent button whose custom_id embeds the challenge date.
    Interactions from previous days are rejected with an ephemeral notice.
    """

    def __init__(self, challenge_date: str) -> None:
        super().__init__(
            discord.ui.Button(
                label="✅ Mark Complete",
                style=discord.ButtonStyle.success,
                custom_id=f"complete:{challenge_date}",
            )
        )
        self.challenge_date = challenge_date

    @classmethod
    async def from_custom_id(
        cls,
        interaction: discord.Interaction,
        item: discord.ui.Button,
        match: re.Match,
    ) -> "CompleteButton":
        return cls(match.group("date"))

    async def callback(self, interaction: discord.Interaction) -> None:
        today = today_pacific()

        # ── Expiry guard ────────────────────────────────────────────────────
        if self.challenge_date != today:
            await interaction.response.send_message(
                f"⏰ This challenge (`{self.challenge_date}`) has expired.\n"
                f"Use `/daily` to see today's challenge.",
                ephemeral=True,
            )
            return

        # ── Fetch today's challenge ─────────────────────────────────────────
        challenge = await db.get_daily_challenge(today)
        if not challenge:
            await interaction.response.send_message(
                "No daily challenge found. Something went wrong — ping a server admin.",
                ephemeral=True,
            )
            return

        challenge_id = challenge["id"]
        user         = interaction.user
        user_id      = user.id
        username     = user.display_name

        # ── Toggle completion ───────────────────────────────────────────────
        completions = await db.get_completions(challenge_id)
        already_done = any(c["user_id"] == user_id for c in completions)

        if already_done:
            await db.unmark_complete(challenge_id, user_id)
            action_msg = "↩️ Unmarked as complete."
        else:
            await db.mark_complete(challenge_id, user_id, username)
            action_msg = "✅ Marked as complete!"

        # ── Refresh completions & update the embed ─────────────────────────
        completions   = await db.get_completions(challenge_id)
        total_members = max(len(MEMBER_IDS), 3)  # default expectation: 3
        embed         = build_challenge_embed(challenge, completions, total_members)

        await interaction.response.edit_message(embed=embed)
        await interaction.followup.send(action_msg, ephemeral=True)


class DailyView(discord.ui.View):
    """View that wraps a date-stamped CompleteButton."""

    def __init__(self, challenge_date: str) -> None:
        super().__init__(timeout=None)
        self.add_item(CompleteButton(challenge_date))


# ─────────────────────────────────────────────────────────────────────────────
# Bot setup
# ─────────────────────────────────────────────────────────────────────────────

intents = discord.Intents.default()

bot  = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


# ─────────────────────────────────────────────────────────────────────────────
# Core: post / fetch daily challenge
# ─────────────────────────────────────────────────────────────────────────────

async def post_daily_challenge(date_str: str | None = None) -> None:
    """
    Create (or retrieve) the daily challenge for *date_str* (defaults to today
    Pacific) and post it to CHANNEL_ID.  Safe to call multiple times — only
    one post is created per date.
    """
    date_str = date_str or today_pacific()
    channel  = bot.get_channel(CHANNEL_ID)
    if channel is None:
        log.error("Channel %s not found — is CHANNEL_ID correct?", CHANNEL_ID)
        return

    # Re-use existing challenge if already created (e.g. bot restarted)
    challenge = await db.get_daily_challenge(date_str)
    if not challenge:
        try:
            challenge = await db.create_daily_challenge(date_str)
            log.info("Created daily challenge for %s: %s", date_str, challenge["name"])
        except RuntimeError as exc:
            log.error("Failed to create challenge: %s", exc)
            return

    # Skip if a message was already posted today
    if challenge.get("message_id"):
        log.info("Daily challenge message already posted for %s", date_str)
        return

    completions   = await db.get_completions(challenge["id"])
    total_members = max(len(MEMBER_IDS), 3)
    embed         = build_challenge_embed(challenge, completions, total_members)
    view          = DailyView(date_str)

    # Build mention string
    mention_str = ""
    if MEMBER_IDS:
        mention_str = " ".join(f"<@{uid}>" for uid in MEMBER_IDS)

    msg = await channel.send(content=mention_str or None, embed=embed, view=view)
    await db.save_message_id(date_str, msg.id)
    log.info("Posted daily challenge for %s (message %s)", date_str, msg.id)


# ─────────────────────────────────────────────────────────────────────────────
# Events
# ─────────────────────────────────────────────────────────────────────────────

@bot.event
async def on_ready() -> None:
    log.info("Logged in as %s (ID %s)", bot.user, bot.user.id)

    # Initialise database
    await db.init_db(PROBLEMS)

    # Register dynamic item handler (handles all complete:YYYY-MM-DD custom IDs)
    bot.add_dynamic_items(CompleteButton)

    # Sync application commands
    try:
        synced = await tree.sync()
        log.info("Synced %d slash command(s)", len(synced))
    except Exception as exc:
        log.error("Failed to sync slash commands: %s", exc)

    # Start the daily scheduler
    scheduler = AsyncIOScheduler(timezone=PACIFIC_TZ)
    scheduler.add_job(
        post_daily_challenge,
        CronTrigger(hour=8, minute=0, timezone=PACIFIC_TZ),
        id="daily_challenge",
        replace_existing=True,
    )
    scheduler.start()
    log.info("Scheduler started — next post at 08:00 Pacific")


# ─────────────────────────────────────────────────────────────────────────────
# Slash commands
# ─────────────────────────────────────────────────────────────────────────────

@tree.command(name="daily", description="Show today's NeetCode daily challenge")
async def cmd_daily(interaction: discord.Interaction) -> None:
    await interaction.response.defer(ephemeral=False)

    date_str  = today_pacific()
    challenge = await db.get_daily_challenge(date_str)

    if not challenge:
        # No challenge posted yet today — create one on demand
        try:
            challenge = await db.create_daily_challenge(date_str)
        except RuntimeError as exc:
            await interaction.followup.send(f"❌ Error: {exc}", ephemeral=True)
            return

    completions   = await db.get_completions(challenge["id"])
    total_members = max(len(MEMBER_IDS), 3)
    embed         = build_challenge_embed(challenge, completions, total_members)
    view          = DailyView(date_str)

    msg = await interaction.followup.send(embed=embed, view=view)

    # Persist message_id only if not already set (first post wins)
    if not challenge.get("message_id"):
        await db.save_message_id(date_str, msg.id)


@tree.command(
    name="random",
    description="Get a random Blind 75 problem (does not count as the daily)",
)
async def cmd_random(interaction: discord.Interaction) -> None:
    await interaction.response.defer(ephemeral=False)

    problem = await db.pick_truly_random()
    if not problem:
        await interaction.followup.send("❌ No problems found in the database.", ephemeral=True)
        return

    embed = build_random_embed(problem)
    await interaction.followup.send(embed=embed)


@tree.command(name="stats", description="View your personal completion stats")
async def cmd_stats(interaction: discord.Interaction) -> None:
    await interaction.response.defer(ephemeral=True)

    user_id  = interaction.user.id
    username = interaction.user.display_name
    stats    = await db.get_user_stats(user_id)
    progress = await db.get_cycle_progress()
    board    = await db.get_leaderboard()

    total_c = stats["total_completed"]
    total_h = stats["total_challenges"]
    pct     = f"{total_c / total_h * 100:.0f}%" if total_h else "—"

    embed = discord.Embed(
        title=f"📊 Stats for {username}",
        colour=discord.Colour.blurple(),
    )
    embed.add_field(
        name="✅ Problems Completed",
        value=f"**{total_c}** / {total_h} challenges posted ({pct})",
        inline=False,
    )
    embed.add_field(
        name="🔥 Current Streak",
        value=f"**{stats['streak']}** day{'s' if stats['streak'] != 1 else ''}",
        inline=True,
    )
    embed.add_field(
        name="🔄 Cycle Progress",
        value=f"{progress['used']} / {progress['total']} problems used",
        inline=True,
    )

    if stats["recent"]:
        recent_lines = "\n".join(
            f"{DIFFICULTY_EMOJI.get(r['difficulty'], '⬜')} `{r['challenge_date']}` — {r['name']}"
            for r in stats["recent"]
        )
        embed.add_field(name="🕐 Recent Completions", value=recent_lines, inline=False)

    # Leaderboard
    if board:
        lb_lines = []
        medals   = ["🥇", "🥈", "🥉"]
        for i, entry in enumerate(board):
            medal = medals[i] if i < 3 else f"{i+1}."
            mark  = " ← you" if entry["user_id"] == user_id else ""
            lb_lines.append(f"{medal} **{entry['username']}** — {entry['completed']}{mark}")
        embed.add_field(name="🏆 Leaderboard", value="\n".join(lb_lines), inline=False)

    await interaction.followup.send(embed=embed, ephemeral=True)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    bot.run(TOKEN, log_handler=None)
