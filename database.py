"""
SQLite database layer for the NeetCode Daily bot.

Tables
------
problems          – static problem catalogue seeded from problems.py
daily_challenges  – one row per day (date is unique)
completions       – one row per (challenge, user) pair
"""

import aiosqlite
import random
from datetime import date
from typing import Optional

DB_PATH = "neetcode_bot.db"


# ─────────────────────────────────────────────────────────────────────────────
# Initialisation
# ─────────────────────────────────────────────────────────────────────────────

async def init_db(problems: list[tuple]) -> None:
    """Create tables and seed the problems catalogue (idempotent)."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript("""
            PRAGMA journal_mode=WAL;

            CREATE TABLE IF NOT EXISTS problems (
                id              INTEGER PRIMARY KEY,
                name            TEXT    NOT NULL,
                difficulty      TEXT    NOT NULL,
                topic           TEXT    NOT NULL,
                url             TEXT    NOT NULL,
                selected        INTEGER NOT NULL DEFAULT 0,
                selection_order INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS daily_challenges (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id     INTEGER NOT NULL,
                challenge_date TEXT    NOT NULL UNIQUE,
                message_id     INTEGER,
                FOREIGN KEY (problem_id) REFERENCES problems (id)
            );

            CREATE TABLE IF NOT EXISTS completions (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                challenge_id INTEGER NOT NULL,
                user_id      INTEGER NOT NULL,
                username     TEXT    NOT NULL,
                completed_at TEXT    NOT NULL,
                UNIQUE (challenge_id, user_id),
                FOREIGN KEY (challenge_id) REFERENCES daily_challenges (id)
            );
        """)

        # Seed problems (INSERT OR IGNORE keeps existing data intact)
        await db.executemany(
            "INSERT OR IGNORE INTO problems (id, name, difficulty, topic, url) "
            "VALUES (?, ?, ?, ?, ?)",
            problems,
        )
        await db.commit()


# ─────────────────────────────────────────────────────────────────────────────
# Problem selection
# ─────────────────────────────────────────────────────────────────────────────

async def pick_random_unselected() -> Optional[dict]:
    """
    Return a random problem that has not yet been used in this cycle.
    If all 150 have been used, reset the cycle and start over.
    Returns None only if the problems table is empty (should never happen).
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        # Count unseen problems
        cur = await db.execute(
            "SELECT COUNT(*) AS cnt FROM problems WHERE selected = 0"
        )
        row = await cur.fetchone()
        if row["cnt"] == 0:
            # Full cycle complete – reset and start over
            await db.execute(
                "UPDATE problems SET selected = 0, selection_order = 0"
            )
            await db.commit()

        # Fetch all unseen problems and pick one at random (avoids RANDOM()
        # ordering full-scan on large tables, though 150 rows is trivial)
        cur = await db.execute(
            "SELECT id, name, difficulty, topic, url FROM problems "
            "WHERE selected = 0"
        )
        rows = await cur.fetchall()
        if not rows:
            return None

        chosen = random.choice(rows)
        return dict(chosen)


async def pick_truly_random() -> Optional[dict]:
    """Return any random problem (ignores selection state). Used by /random."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, name, difficulty, topic, url FROM problems "
            "ORDER BY RANDOM() LIMIT 1"
        )
        row = await cur.fetchone()
        return dict(row) if row else None


# ─────────────────────────────────────────────────────────────────────────────
# Daily challenge management
# ─────────────────────────────────────────────────────────────────────────────

async def get_daily_challenge(challenge_date: str) -> Optional[dict]:
    """
    Return today's challenge row joined with its problem data, or None if
    no challenge has been posted for that date yet.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """
            SELECT dc.id, dc.message_id, dc.challenge_date,
                   p.id AS problem_id, p.name, p.difficulty, p.topic, p.url
            FROM   daily_challenges dc
            JOIN   problems p ON p.id = dc.problem_id
            WHERE  dc.challenge_date = ?
            """,
            (challenge_date,),
        )
        row = await cur.fetchone()
        return dict(row) if row else None


async def create_daily_challenge(challenge_date: str) -> dict:
    """
    Pick an unseen problem, mark it selected, and persist the daily challenge.
    Returns the full challenge dict (same shape as get_daily_challenge).
    Raises RuntimeError if a challenge already exists for that date.
    """
    existing = await get_daily_challenge(challenge_date)
    if existing:
        raise RuntimeError(f"Challenge already exists for {challenge_date}")

    problem = await pick_random_unselected()
    if problem is None:
        raise RuntimeError("No problems found in database")

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        # Determine the next selection_order value
        cur = await db.execute(
            "SELECT COALESCE(MAX(selection_order), 0) AS max_order FROM problems"
        )
        row = await cur.fetchone()
        next_order = row["max_order"] + 1

        # Mark problem as selected
        await db.execute(
            "UPDATE problems SET selected = 1, selection_order = ? WHERE id = ?",
            (next_order, problem["id"]),
        )

        # Insert daily challenge row
        await db.execute(
            "INSERT INTO daily_challenges (problem_id, challenge_date) VALUES (?, ?)",
            (problem["id"], challenge_date),
        )
        await db.commit()

    return await get_daily_challenge(challenge_date)


async def save_message_id(challenge_date: str, message_id: int) -> None:
    """Persist the Discord message ID for a daily challenge (for future edits)."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE daily_challenges SET message_id = ? WHERE challenge_date = ?",
            (message_id, challenge_date),
        )
        await db.commit()


# ─────────────────────────────────────────────────────────────────────────────
# Completion tracking
# ─────────────────────────────────────────────────────────────────────────────

async def mark_complete(challenge_id: int, user_id: int, username: str) -> bool:
    """
    Record a completion.  Returns True if newly inserted, False if the user
    had already marked this challenge complete.
    """
    from datetime import datetime, timezone
    completed_at = datetime.now(timezone.utc).isoformat()

    async with aiosqlite.connect(DB_PATH) as db:
        try:
            await db.execute(
                "INSERT INTO completions (challenge_id, user_id, username, completed_at) "
                "VALUES (?, ?, ?, ?)",
                (challenge_id, user_id, username, completed_at),
            )
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            # UNIQUE constraint: already completed
            return False


async def get_completions(challenge_id: int) -> list[dict]:
    """Return all completions for a given challenge."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT user_id, username, completed_at FROM completions "
            "WHERE challenge_id = ? ORDER BY completed_at",
            (challenge_id,),
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def unmark_complete(challenge_id: int, user_id: int) -> bool:
    """
    Remove a completion (toggle off).
    Returns True if a row was deleted, False if none existed.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "DELETE FROM completions WHERE challenge_id = ? AND user_id = ?",
            (challenge_id, user_id),
        )
        await db.commit()
        return cur.rowcount > 0


# ─────────────────────────────────────────────────────────────────────────────
# Stats
# ─────────────────────────────────────────────────────────────────────────────

async def get_user_stats(user_id: int) -> dict:
    """Return completion stats for a specific user."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        cur = await db.execute(
            "SELECT COUNT(*) AS total FROM completions WHERE user_id = ?",
            (user_id,),
        )
        row = await cur.fetchone()
        total_completed = row["total"]

        cur = await db.execute(
            "SELECT COUNT(*) AS total FROM daily_challenges"
        )
        row = await cur.fetchone()
        total_challenges = row["total"]

        # Streak: consecutive days ending today (or most recent completion)
        cur = await db.execute(
            """
            SELECT dc.challenge_date
            FROM   completions c
            JOIN   daily_challenges dc ON dc.id = c.challenge_id
            WHERE  c.user_id = ?
            ORDER  BY dc.challenge_date DESC
            """,
            (user_id,),
        )
        date_rows = await cur.fetchall()
        streak = _calculate_streak([r["challenge_date"] for r in date_rows])

        # Recent completions (last 5)
        cur = await db.execute(
            """
            SELECT p.name, p.difficulty, dc.challenge_date
            FROM   completions c
            JOIN   daily_challenges dc ON dc.id = c.challenge_id
            JOIN   problems p ON p.id = dc.problem_id
            WHERE  c.user_id = ?
            ORDER  BY dc.challenge_date DESC
            LIMIT  5
            """,
            (user_id,),
        )
        recent = [dict(r) for r in await cur.fetchall()]

        return {
            "total_completed": total_completed,
            "total_challenges": total_challenges,
            "streak": streak,
            "recent": recent,
        }


async def get_leaderboard() -> list[dict]:
    """Return all users sorted by completion count."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """
            SELECT username, user_id, COUNT(*) AS completed
            FROM   completions
            GROUP  BY user_id
            ORDER  BY completed DESC
            """
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def get_cycle_progress() -> dict:
    """Return how many problems have been used in the current cycle."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT COUNT(*) AS used FROM problems WHERE selected = 1"
        )
        used = (await cur.fetchone())["used"]
        cur = await db.execute("SELECT COUNT(*) AS total FROM problems")
        total = (await cur.fetchone())["total"]
        return {"used": used, "total": total}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _calculate_streak(dates: list[str]) -> int:
    """
    Given a list of date strings (YYYY-MM-DD) sorted descending,
    return the length of the current consecutive-day streak.
    """
    if not dates:
        return 0

    from datetime import date, timedelta

    streak = 1
    prev = date.fromisoformat(dates[0])
    for ds in dates[1:]:
        cur = date.fromisoformat(ds)
        if prev - cur == timedelta(days=1):
            streak += 1
            prev = cur
        else:
            break
    return streak
