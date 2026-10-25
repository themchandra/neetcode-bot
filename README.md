# NeetCode Daily Discord Bot

A Discord bot that posts one random [NeetCode 150](https://neetcode.io/practice) problem every day at **8 AM Pacific** to a designated channel. Members can mark problems complete via a button; the bot tracks everyone's progress in a local SQLite database.

---

## Features

| Feature | Detail |
|---|---|
| 📅 Daily post | 8 AM Pacific, auto-picked from NeetCode 150 |
| 🔄 No repeats | Cycles through all 150 before repeating |
| ✅ Completion tracking | Button toggles your completion on/off |
| 🚫 Expired buttons | Previous-day buttons are rejected gracefully |
| 🔀 `/random` | Fetch any NeetCode 150 problem on demand |
| 📅 `/daily` | Show (or create) today's challenge |
| 📊 `/stats` | Personal completions, streak, and leaderboard |
| 💾 SQLite | All data stored locally in `neetcode_bot.db` |

---

## Quick Start

### 1. Prerequisites

- Python **3.11+**
- A Discord account with access to your server

### 2. Clone / download the project

```bash
git clone <your-repo-url>
cd "Neetcode Bot"
```

### 3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Create a Discord application & bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and click **New Application**.
2. Name it (e.g. *NeetCode Daily*) and click **Create**.
3. Open the **Bot** tab → click **Add Bot** → confirm.
4. Under **Token** click **Reset Token** and copy it — you'll need it in a moment.
5. Under **Privileged Gateway Intents** enable **Message Content Intent** (required for the `!` prefix fallback).
6. Open the **OAuth2 → URL Generator** tab.
   - Scopes: `bot`, `applications.commands`
   - Bot Permissions: `Send Messages`, `Embed Links`, `Read Message History`
7. Copy the generated URL, paste it in a browser, and invite the bot to your server.

### 5. Get your channel ID

1. In Discord, go to **Settings → Advanced** and enable **Developer Mode**.
2. Right-click the channel where you want daily problems posted.
3. Choose **Copy Channel ID**.

### 6. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
DISCORD_TOKEN=your-bot-token-here
CHANNEL_ID=123456789012345678

# Optional — comma-separated user IDs to @mention in each daily post
MEMBER_IDS=111111111111111111,222222222222222222,333333333333333333
```

**How to get a user ID:** Right-click a user in Discord (with Developer Mode on) → **Copy User ID**.

### 7. Run the bot

```bash
python bot.py
```

You should see:

```
Logged in as NeetCode Daily#1234 (ID ...)
Synced 3 slash command(s)
Scheduler started — next post at 08:00 Pacific
```

The bot will post the first problem at 8 AM Pacific. To test immediately, use `/daily` in your server.

---

## Slash Commands

| Command | Who can use | Description |
|---|---|---|
| `/daily` | Anyone | Shows today's challenge. Creates one on demand if the scheduler hasn't fired yet. |
| `/random` | Anyone | Fetches a random NeetCode 150 problem. Does **not** count as the daily. |
| `/stats` | Anyone | Shows your completion count, streak, and the server leaderboard (ephemeral). |

> **Note:** Slash commands propagate globally and may take up to an hour to appear after the first run. Subsequent syncs are instant.

---

## How the Daily Cycle Works

1. On each run the bot picks one random **unselected** problem from the 150.
2. The problem is marked *selected* and stored in SQLite with the current date.
3. When all 150 have been used, the cycle resets automatically and starts over.
4. If the bot is restarted mid-day, it detects the existing challenge and skips re-posting.

---

## Completion Button

- Clicking **✅ Mark Complete** records your completion and updates the embed counter.
- Clicking again **toggles it off** (unmarks).
- Buttons from **previous days** silently expire — clicking one shows an ephemeral error message and has no effect on today's challenge.

---

## Deployment (always-on)

### Option A — systemd (Linux VPS / Raspberry Pi)

Create `/etc/systemd/system/neetcode-bot.service`:

```ini
[Unit]
Description=NeetCode Daily Discord Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/Neetcode Bot
ExecStart=/path/to/Neetcode Bot/.venv/bin/python bot.py
Restart=on-failure
RestartSec=10
EnvironmentFile=/path/to/Neetcode Bot/.env

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable neetcode-bot
sudo systemctl start neetcode-bot
sudo journalctl -u neetcode-bot -f    # live logs
```

### Option B — screen / tmux (quick & dirty)

```bash
screen -S neetcode-bot
python bot.py
# Ctrl-A D to detach
```

### Option C — Railway / Render / Fly.io

These platforms support always-on Python processes with a free tier:

1. Push the project to a **private** GitHub repository.
2. Connect the repo to your chosen platform.
3. Set the environment variables in the platform's dashboard.
4. Set the **start command** to `python bot.py`.
5. Deploy — the platform will keep the process alive 24/7.

> ⚠️ Never commit your `.env` file or expose your bot token publicly.

---

## Project Structure

```
Neetcode Bot/
├── bot.py           # Discord bot, slash commands, scheduler, button handler
├── database.py      # SQLite async layer (aiosqlite)
├── problems.py      # All 150 NeetCode problems as a Python list
├── requirements.txt # Python dependencies
├── .env.example     # Environment variable template
└── README.md        # This file
```

`neetcode_bot.db` is created automatically on first run and should **not** be committed to version control (add it to `.gitignore`).

---

## Resetting the Database

To start completely fresh:

```bash
rm neetcode_bot.db
python bot.py
```

To reset only the problem cycle (keep completion history):

```python
import asyncio, aiosqlite

async def reset():
    async with aiosqlite.connect("neetcode_bot.db") as db:
        await db.execute("UPDATE problems SET selected = 0, selection_order = 0")
        await db.commit()

asyncio.run(reset())
```

---

## Contributing

Pull requests welcome! The problem list in `problems.py` is straightforward to extend if NeetCode updates its curriculum.
