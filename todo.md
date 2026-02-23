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
15. **All Views use `timeout=None`.** Register all persistent Views in `setup_hook()` via `bot.add_view()`. Each button `custom_id` is a hardcoded string that never changes across restarts. For bet-specific buttons (thread views), use `discord.ui.DynamicItem` with a regex pattern to encode the `bet_id` directly in the `custom_id`.
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

## 🎯 CHANNEL SETUP (Complete)

- [x] Create `channels.py` - Channel setup and management
- [x] Add channel names to `config.py`
- [x] Update `main.py` - call channel setup on startup
- [x] Update dashboard - post to #Turd-Gambling
- [x] Update bet flow - create thread in #Turd-Bets
- [x] Add Win/Lose/Dispute buttons to bet threads
- [x] Update resolution - archive to #Turd-Archive, dispute to #Turd-Admin
- [x] Test and verify

> **CHECKPOINT**: All channel & bet flow features implemented!

## ✅ PHASE 0 — Pre-Work (Complete)

- [x] **0.1** Discord bot token obtained from Turd-News-Network
- [x] **0.2** `.env` created with bot token
- [x] **0.3** `.env.example` created

> ✅ **CHECKPOINT 0**: Pre-work complete.

---

## 🎯 PHASE 1 — Custom Bet System (Complete)

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

## 🎯 PHASE 2 — Enhanced Verification System

Multiple verification methods for bet resolution with dual-confirmation flow.

### 2.1 Verification Dropdown Options
Add the following options to the verification method dropdown in the bet creation modal:
- [x] 🤝 **Manual** - Both parties must agree on winner
- [ ] 🗳️ **Vote** - Community votes to decide winner
- [ ] 🔗 **Link Proof** - Either party submits proof, admin resolves
- [ ] 🤖 **AI Verification** - Bot scrapes URL and verifies result
- [ ] ⏰ **Scheduled** - Bot pings at specified date for resolution

### 2.2 Bet Creation Modal Updates
- [ ] Add date/time field to bet creation modal for scheduled verification
- [ ] Add URL field for AI verification (what to scrape)
- [ ] Add expected result field for AI verification (what to check)
- [ ] Update verification dropdown in dashboard_views.py
- [ ] Syntax check dashboard_views.py

### 2.3 Database Schema Updates
Add new columns to the bets table:
- [ ] `verification_url` - URL for AI verification to scrape
- [ ] `verification_claim` - Expected result/claim to verify
- [ ] `verification_date` - Date/time for scheduled verification
- [ ] `pending_confirmation` - Boolean, true when waiting for second user
- [ ] `first_responder_id` - User ID who first clicked win/lose
- [ ] `first_response` - Which side they chose (A or B)
- [ ] Update database.py with new fields
- [ ] Syntax check database.py

### 2.4 Dual-Confirmation Resolution Flow (Manual & Link Proof)
**IMPORTANT**: Bet must NOT resolve until BOTH parties agree or dispute is filed.

Implementation in bet_threads.py:
- [ ] Modify IWinButton callback to NOT immediately resolve
- [ ] Store first responder's choice in database (pending_confirmation=true)
- [ ] Send ping to second user: "User X claims they won. Please confirm or dispute."
- [ ] Add ConfirmButton - second user agrees, bet resolves
- [ ] Add DisputeButton - second user disputes, goes to admin
- [ ] Update ILoseButton to work the same way
- [ ] Bet stays in "pending_confirmation" until both agree or dispute
- [ ] If first user changes mind before second responds, allow them to cancel their claim
- [ ] Syntax check bet_threads.py

### 2.5 Submit Proof Button (Link Proof Verification)
Add to bet thread for both users:
- [ ] Create SubmitProofButton with custom_id pattern: `proof_{bet_id}_{user_id}`
- [ ] Button label: "📎 Submit Proof"
- [ ] Opens modal with TextInput for proof URL
- [ ] Stores proof_url in database
- [ ] Posts proof to bet thread
- [ ] Both users can submit proof before resolution
- [ ] Syntax check bet_threads.py

### 2.6 Scheduled Verification System
- [ ] Create background task in main.py to check scheduled bets
- [ ] Run every 5 minutes to check for bets at verification time
- [ ] At verification time, ping both users in thread: "Time to resolve! Click I Win/I Lose"
- [ ] For Vote: Automatically start vote poll at verification time
- [ ] For AI: Run verification check at this time
- [ ] Syntax check main.py

### 2.7 Vote Verification System
- [ ] Create VoteStartButton in bet_threads.py
- [ ] Creates poll embed with reactions for each side
- [ ] Allows all server members to vote
- [ ] 24 hour vote timeout
- [ ] Majority wins, tie goes to creator
- [ ] Auto-resolves or flags for admin if unclear
- [ ] Syntax check bet_threads.py

### 2.8 AI Verification System (URL Scraping)
Create new module `verification.py`:
- [ ] Create `scrape_url(url)` function using requests + beautifulsoup4
- [ ] Create `verify_claim(content, claim)` function
- [ ] Support numeric comparisons: >, <, >=, <=, ==, !=
- [ ] Support text contains: "contains X"
- [ ] Create verification result: WIN_A, WIN_B, UNCLEAR
- [ ] If UNCLEAR, flag for admin review
- [ ] Cache scraped data to avoid rate limits
- [ ] Syntax check verification.py

### 2.9 Admin Resolution Workflow
- [ ] When dispute filed, post to #turd-admin
- [ ] Include all proof submitted
- [ ] Include both users' claims
- [ ] Admin can resolve with winner selection
- [ ] Admin can cancel and refund
- [ ] Syntax check dashboard_views.py

### 2.10 Archive Updates
- [ ] Archive posts to ALL guilds the bot is in (already implemented)
- [ ] Include verification method in archive embed
- [ ] Include proof links if submitted

> **CHECKPOINT**: Enhanced Verification System complete!

---

## 🎯 PHASE 3 — Custom Bets Revamp (Multi-Step Thread Flow)

Comprehensive revamp of the Custom Bets button with full feature set.

### 3.1 Multi-Step Thread Flow Setup
- [ ] Create `bet_flow.py` - New module for multi-step bet creation
- [ ] Step 1: User clicks "Custom Bets" → Creates private thread off dashboard
- [ ] Step 2: Bot prompts for opponent selection with user dropdown
- [ ] Step 3: Bot prompts for bet type (1v1, 1vMany, ManyvMany)
- [ ] Step 4: Bot prompts for bet topic and amount
- [ ] Step 5: Bot prompts for category (Sports, Gaming, Real Life, Random)
- [ ] Step 6: Bot prompts for payout odds (Even, Custom)
- [ ] Step 7: Bot prompts for visibility (Open, Invite Only)
- [ ] Step 8: Bot prompts for expiration (24h, 7d, Never)
- [ ] Step 9: Summary confirmation → Post to #turd-bets

### 3.2 User Dropdown Integration
- [ ] Add `get_server_members()` function to fetch guild members
- [ ] Create user select dropdown with search/filter
- [ ] Handle 1vMany with multiple user selection
- [ ] Syntax check bet_flow.py

### 3.3 Bet Type Selection
- [ ] 1v1 (head-to-head)
- [ ] 1vMany (creator vs multiple opponents)
- [ ] ManyvMany (team vs team)

### 3.4 Bet Category Selection
- [ ] Sports
- [ ] Gaming
- [ ] Real Life
- [ ] Random/Challenge

### 3.5 Payout Odds Selection
- [ ] Even (1:1)
- [ ] Custom odds input

### 3.6 Visibility Options
- [ ] Open (anyone can join)
- [ ] Invite Only (specific users)

### 3.7 Expiration Options
- [ ] 24 hours
- [ ] 7 days
- [ ] Never

### 3.8 Update Bet Threads
- [ ] Modify bet_threads.py for new bet types
- [ ] Add participant management for multi-user bets
- [ ] Add edit bet functionality
- [ ] Add cancel bet functionality
- [ ] Syntax check bet_threads.py

> **CHECKPOINT**: Custom Bets Revamp complete!

---

## 🎯 PHASE 4 — Additional Features

Extra features to enhance the betting experience.

### 4.1 Bet Images/Screenshots
- [ ] "Upload Proof" button
- [ ] Image upload handling
- [ ] Store images locally or via CDN
- [ ] Display in thread

### 4.2 Bet Editing
- [ ] "Edit Bet" button for creator
- [ ] Edit topic, amount, description
- [ ] Cannot edit after participant joins
- [ ] Log edit history

### 4.3 Bet Cancellation
- [ ] "Cancel Bet" button for creator
- [ ] Cancellation fee (10% of bet amount)
- [ ] Refund to participants
- [ ] Log cancellation

### 4.4 Bet Tags
- [ ] Predefined tags: high-stakes, friendly, tournament, practice
- [ ] Custom tag creation
- [ ] Filter bets by tag
- [ ] Tag analytics

### 4.5 Bet Reminders
- [ ] Notification 1 hour before expiration
- [ ] Notification when bet is joined
- [ ] Notification when vote starts
- [ ] Notification when resolution required

### 4.6 Bet Analytics
- [ ] Track win rates by category
- [ ] Track win rates by bet type
- [ ] Most active bettors
- [ ] Popular bet categories
- [ ] "My Stats" enhanced display

### 4.7 Bet Chat
- [ ] Allow messages in bet threads
- [ ] Bot welcomes in thread
- [ ] Thread stays open for discussion

### 4.8 Side Bets
- [ ] Add prop bets to existing bet
- [ ] Track multiple outcomes
- [ ] Separate resolution

> **CHECKPOINT**: Additional Features complete!

---

## 🎯 PHASE 5 — Sports Betting (Future)

- [ ] API integration for live scores
- [ ] Sports-specific bet types
- [ ] Odds display

---

## 🎯 PHASE 6 — Prediction Markets (Future)

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
├── bet_flow.py                # Multi-step bet creation
├── bet_threads.py             # Thread views
├── verification.py            # AI verification system (NEW)
├── quips.py                   # Character quotes
├── dashboard.py               # Dashboard embed
├── dashboard_views.py         # Button handlers
├── requirements.txt           # Dependencies
├── .env                      # Private config
├── .env.example              # Config template
├── run_bot.bat               # Launch script
├── tests/                    # Test files
└── turd_gambling.db         # SQLite database (auto-created)
```
