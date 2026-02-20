# 🎰 Turd Casino — Discord Betting Bot
## Master Build Document — Cline AI Implementation Guide

> **PRIME DIRECTIVE**: Zero placeholders. Zero mock data. Zero stub functions. Zero TODO/FIXME comments in code. Every feature listed must be fully functional before marking it complete. If a feature cannot be built, remove it entirely — do not scaffold it.

> **TODO.MD RULE**: After completing each numbered step, mark it `[x]` in this file immediately. After completing each PHASE, mark the checkpoint `[x]`. This file is always up to date.

---

## ⚙️ RULES (Read Before Every Action)

1. **ASK BEFORE EVERY ACTION.** Show the user a multiple-choice question before each step. No exceptions. No assumptions.
2. **Zero placeholders.** All code is production-ready. No stubs, no mock returns. If an API fails, write real fallback logic.
3. **No TODO/FIXME/HACK in code.** This file is the only place for planned work.
4. **Free APIs only.** Keys go in `.env`.
5. **UTF-8 everywhere.** After every file edit involving emoji, run syntax check.
6. **Syntax check after every file edit.** `python -m py_compile <file>`. Fix before moving on.
7. **Discord embed limits.** Title ≤256. Field name ≤256. Field value ≤1024 (truncate with `...` if over). Description ≤4096. Total embed ≤6000. Max 25 fields. Max 10 embeds per message. Empty field values = HTTP 400 — guard every field with a fallback string.
8. **Never touch backup files.** Files ending in `.backup`, `_fixed.py`, `_restore.py`, `fix_*.py` are artifacts. Do not import or modify.
9. **Rate limits respected.** Cache all API calls in SQLite. Retry with exponential backoff. Discord: 50 req/s max — use `asyncio.sleep(0.02)` when bulk-sending.
10. **Compact embeds.** `inline=True` on all fields where possible.
11. **Windows 11 / cmd.exe.** Run via `python main.py`. No ANSI codes. No Linux-only packages. All paths via `os.path.join()` or `pathlib.Path`.
12. **SQLite WAL mode + timeout=30.** All connections: `PRAGMA journal_mode=WAL`, `PRAGMA foreign_keys=ON`, `timeout=30`. Retry on `OperationalError: database is locked`.
13. **Feature flags in config.py.** Every major feature has an `ENABLE_*` boolean. Check flag before executing.
14. **DASHBOARD CHANNEL = ONE MESSAGE ONLY, ALWAYS AT THE BOTTOM.** The `#betting-dashboard` channel contains exactly ONE message at all times: the dashboard. On startup: delete ALL messages in the channel (`purge` with no limit), then post fresh dashboard. On every update: delete old dashboard message, post new one — the new post is always the most recent (bottom) message. `on_message`: delete ANY non-bot message in this channel immediately (no exceptions). Background task: every 10 minutes, check for stray messages and purge them, then re-anchor dashboard. The dashboard is always the bottom message because it is the ONLY message.
14b. **ALL button interactions open a thread — NEVER post visible messages into the dashboard channel.** When a user clicks any dashboard button, the bot NEVER sends a visible (non-ephemeral) message into the dashboard channel. Two patterns are allowed: (A) **Ephemeral** — only the clicking user sees it, the channel is unaffected — use for: balance, stats, leaderboard, help, daily bonus confirmation. (B) **Private thread off the dashboard message** — for multi-step flows (bet creation, bet management, opponent targeting) create `await dashboard_message.create_thread(name=f"🎲 Bet Setup — {user.display_name}", type=ChannelType.private_thread, auto_archive_duration=60)` and send the user a message in the thread directing them there. The dashboard message never receives a visible reply in the channel.
14c. **Public announcements go to `ANNOUNCEMENTS_CHANNEL_ID` only.** Bankruptcy shame, weekly leaderboard results, and any server-wide announcements post to `#betting-announcements` (separate channel, `ANNOUNCEMENTS_CHANNEL_ID` in `.env`). NOTHING public is ever posted in the dashboard channel except the dashboard itself. Bet resolution announcements post in the bet's own thread (in `#betting-threads`), not in dashboard.
15. **All Views use `timeout=None` + persistent=True.** Register all persistent Views in `setup_hook()` via `bot.add_view()`. Each button `custom_id` is a hardcoded string that never changes across restarts. For bet-specific buttons (thread views), use `discord.ui.DynamicItem` with a regex pattern to encode the `bet_id` directly in the `custom_id`.
16. **No global state outside the database.** All state (bets, balances, config) lives in SQLite.
17. **All slash commands have permission checks.** Use `@app_commands.checks` decorators.
18. **Parameterized queries only.** Never f-string SQL with user input.
19. **Log everything.** `logging` module. Rotate at 10MB. Log all bets, transactions, admin actions, errors.
20. **Validate all user input.** Sanitize before DB insert. Amounts must be positive integers. Text fields have max lengths enforced both in modal and in code.
21. **Defer long interactions.** Any handler taking >3 seconds must call `await interaction.response.defer(ephemeral=True)` first, then `await interaction.followup.send(...)` after. Failure to defer = Discord interaction timeout error.
22. **Test database isolation.** All test scripts use `tests/test_turd_gambling.db`. Never use the production `turd_gambling.db` in tests. Tests clean up after themselves via teardown.
23. **Update todo.md after every step.** Mark `[x]` on completed items immediately.
24. **Modal field limit = 5.** Discord modals support a maximum of 5 `TextInput` fields. Any modal exceeding 5 fields must be split into a multi-step flow.
28. **MAX 300 LINES PER FILE** - No file shall exceed 300 lines. When adding new functionality would exceed this limit, create a new module (e.g., bets2.py, dashboard_views.py) and import it. This ensures easier file editing.
27. **discord.py minimum version 2.6.0.** Required for DynamicItem support. In `requirements.txt`: `discord.py>=2.6.0`.
28. **NO SLASH COMMANDS.** All user interaction is through dashboard buttons, dropdowns, and modals. No `/bet`, `/balance` slash commands.

---

## ✅ PHASE 0 — Pre-Work (Complete)

- [x] **0.1** Discord bot token obtained from Turd-News-Network
- [x] **0.2** `.env` created with bot token
- [x] **0.3** `.env.example` created

> ✅ **CHECKPOINT 0**: Pre-work complete.

---

## 🎯 PHASE 1 — Custom Bet System (START HERE)

The foundation: users create bets against each other (1v1, 1vMany, ManyvMany).

### 1.1 Configuration & Constants
- [x] Create `config.py` with all constants from `.env`
- [x] Syntax check config.py

### 1.2 Database Layer
- [x] Create `database_init.py` - tables: users, bets, transactions
- [x] Create `database.py` - CRUD operations
- [x] Syntax check database files

### 1.3 Turd Coins Economy
- [x] Create `currency.py` - balance management, daily bonus
- [x] Syntax check currency.py

### 1.4 Bet System Core
- [x] Create `bets.py` - bet creation, joining, resolution
- [x] Syntax check bets.py

### 1.5 Character Quips (Turd Bird Industries)
- [x] Create `quips.py` - Fred, Larry, Ronald quotes for dashboard flavor
- [x] Syntax check quips.py

### 1.6 Dashboard UI
- [x] Create `dashboard.py` - main dashboard embed + buttons
- [x] Create `dashboard_views.py` - button handlers (under 300 lines)
- [x] Syntax check dashboard files

### 1.7 Bot Main Entry
- [x] Create `main.py` - bot setup, dashboard refresh, background tasks
- [x] Create `run_bot.bat` - launch script
- [x] Create `requirements.txt`
- [x] Syntax check main.py

> ✅ **CHECKPOINT 1**: Peer Bet System complete.

---

## 🎯 PHASE 2 — Sports Betting (Future)

- [ ] API integration for live scores
- [ ] Sports-specific bet types
- [ ] Odds display

---

## 🎯 PHASE 3 — Prediction Markets (Future)

- [ ] Election betting
- [ ] Event outcome betting
- [ ] Market resolution

---

## 📁 Project File Structure

```
turd-gambling-network/
├── main.py                    # Bot entry point
├── config.py                  # Configuration
├── database_init.py           # DB schema
├── database.py                # DB operations
├── currency.py                # Turd Coins
├── bets.py                    # Bet logic
├── quips.py                   # Character quotes
├── dashboard.py               # Dashboard embed
├── dashboard_views.py         # Button handlers
├── requirements.txt           # Dependencies
├── .env                       # Private config
├── .env.example              # Config template
├── run_bot.bat               # Launch script
├── tests/                    # Test files
└── turd_gambling.db         # SQLite database (auto-created)
```
