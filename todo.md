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
- [x] 🗳️ **Vote** - Community votes to decide winner
- [x] 🔗 **Link Proof** - Either party submits proof, admin resolves
- [x] 🤖 **AI Verification** - Bot scrapes URL and verifies result
- [x] ⏰ **Scheduled** - Bot pings at specified date for resolution

### 2.2 Bet Creation Modal Updates
- [x] Add date/time field to bet creation modal for scheduled verification
- [x] Add URL field for AI verification (what to scrape)
- [x] Add expected result field for AI verification (what to check)
- [x] Update verification dropdown in dashboard_views.py
- [x] Syntax check dashboard_views.py

### 2.3 Database Schema Updates
Add new columns to the bets table:
- [x] `verification_url` - URL for AI verification to scrape
- [x] `verification_claim` - Expected result/claim to verify
- [x] `verification_date` - Date/time for scheduled verification
- [x] `pending_confirmation` - Boolean, true when waiting for second user
- [x] `first_responder_id` - User ID who first clicked win/lose
- [x] `first_response` - Which side they chose (A or B)
- [x] Update database.py with new fields
- [x] Syntax check database.py

### 2.4 Dual-Confirmation Resolution Flow (Manual & Link Proof)
**IMPORTANT**: Bet must NOT resolve until BOTH parties agree or dispute is filed.

Implementation in bet_threads.py:
- [x] Modify IWinButton callback to NOT immediately resolve
- [x] Store first responder's choice in database (pending_confirmation=true)
- [x] Send ping to second user: "User X claims they won. Please confirm or dispute."
- [x] Add ConfirmButton - second user agrees, bet resolves
- [x] Add DisputeButton - second user disputes, goes to admin
- [x] Update ILoseButton to work the same way
- [x] Bet stays in "pending_confirmation" until both agree or dispute
- [x] If first user changes mind before second responds, allow them to cancel their claim
- [x] Syntax check bet_threads.py

### 2.5 Submit Proof Button (Link Proof Verification)
Add to bet thread for both users:
- [x] Create SubmitProofButton with custom_id pattern: `proof_{bet_id}_{user_id}`
- [x] Button label: "📎 Submit Proof"
- [x] Opens modal with TextInput for proof URL
- [x] Stores proof_url in database
- [x] Posts proof to bet thread
- [x] Both users can submit proof before resolution
- [x] Syntax check bet_threads.py

### 2.6 Scheduled Verification System
- [x] Create background task in main.py to check scheduled bets
- [x] Run every 5 minutes to check for bets at verification time
- [x] At verification time, ping both users in thread: "Time to resolve! Click I Win/I Lose"
- [x] For Vote: Automatically start vote poll at verification time
- [x] For AI: Run verification check at this time
- [x] Syntax check main.py

### 2.7 Vote Verification System
- [x] Create VoteStartButton in bet_threads.py
- [x] Creates poll embed with reactions for each side
- [x] Allows all server members to vote
- [x] 24 hour vote timeout
- [x] Majority wins, tie goes to creator
- [x] Auto-resolves or flags for admin if unclear
- [x] Syntax check bet_threads.py

### 2.8 AI Verification System (URL Scraping)
Create new module `verification.py`:
- [x] Create `scrape_url(url)` function using requests + beautifulsoup4
- [x] Create `verify_claim(content, claim)` function
- [x] Support numeric comparisons: >, <, >=, <=, ==, !=
- [x] Support text contains: "contains X"
- [x] Create verification result: WIN_A, WIN_B, UNCLEAR
- [x] If UNCLEAR, flag for admin review
- [x] Cache scraped data to avoid rate limits
- [x] Syntax check verification.py

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
- [x] Create `bet_flow.py` - New module for multi-step bet creation
- [x] Step 1: User clicks "Custom Bets" → Creates private thread off dashboard
- [x] Step 2: Bot prompts for opponent selection with user dropdown
- [x] Step 3: Bot prompts for bet type (1v1, 1vMany, ManyvMany)
- [x] Step 4: Bot prompts for bet topic and amount
- [x] Step 5: Bot prompts for category (Sports, Gaming, Real Life, Random)
- [x] Step 6: Bot prompts for payout odds (Even, Custom)
- [x] Step 7: Bot prompts for visibility (Open, Invite Only)
- [x] Step 8: Bot prompts for expiration (24h, 7d, Never)
- [x] Step 9: Summary confirmation → Post to #turd-bets

### 3.2 User Dropdown Integration
- [x] Add `get_server_members()` function to fetch guild members
- [x] Create user select dropdown with search/filter
- [x] Handle 1vMany with multiple user selection
- [x] Syntax check bet_flow.py

### 3.3 Bet Type Selection
- [x] 1v1 (head-to-head)
- [x] 1vMany (creator vs multiple opponents)
- [x] ManyvMany (team vs team)

### 3.4 Bet Category Selection
- [x] Sports
- [x] Gaming
- [x] Real Life
- [x] Random/Challenge

### 3.5 Payout Odds Selection
- [x] Even (1:1)
- [x] Custom odds input

### 3.6 Visibility Options
- [x] Open (anyone can join)
- [x] Invite Only (specific users)

### 3.7 Expiration Options
- [x] 24 hours
- [x] 7 days
- [x] Never

### 3.8 Update Bet Threads
- [x] Modify bet_threads.py for new bet types
- [x] Add participant management for multi-user bets
- [ ] Add edit bet functionality
- [ ] Add cancel bet functionality
- [x] Syntax check bet_threads.py

> **CHECKPOINT**: Custom Bets Revamp complete!

---

## 🎯 PHASE 4 — Additional Features

Extra features to enhance the betting experience.

### 4.1 Bet Images/Screenshots
- [x] "Upload Proof" button
- [x] Image upload handling
- [x] Store images locally or via CDN
- [x] Display in thread

### 4.2 Bet Editing
- [x] "Edit Bet" button for creator
- [x] Edit topic, amount, description
- [x] Cannot edit after participant joins
- [x] Log edit history

### 4.3 Bet Cancellation
- [x] "Cancel Bet" button for creator
- [x] Cancellation fee (10% of bet amount)
- [x] Refund to participants
- [x] Log cancellation

### 4.4 Bet Tags
- [x] Predefined tags: high-stakes, friendly, tournament, practice
- [x] Custom tag creation
- [x] Filter bets by tag
- [x] Tag analytics

### 4.5 Bet Reminders
- [x] Notification 1 hour before expiration
- [x] Notification when bet is joined
- [x] Notification when vote starts
- [x] Notification when resolution required

### 4.6 Bet Analytics
- [x] Track win rates by category
- [x] Track win rates by bet type
- [x] Most active bettors
- [x] Popular bet categories
- [x] "My Stats" enhanced display

### 4.7 Bet Chat
- [x] Allow messages in bet threads
- [x] Bot welcomes in thread
- [x] Thread stays open for discussion

### 4.8 Side Bets
- [x] Add prop bets to existing bet
- [x] Track multiple outcomes
- [x] Separate resolution

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

## 🎯 NEW — Prediction Verification System

Users enter predictions before bet is made, winner determined by closest prediction.

### 6.1 Database Updates
- [ ] Add prediction_a field to bets table
- [ ] Add prediction_b field to bets table
- [ ] Add prediction_actual field for actual result
- [ ] Add "prediction" to verification_type options
- [ ] Syntax check database files

### 6.2 Bet Creation Flow
- [ ] Add "Prediction" option to verification dropdown
- [ ] Update modal to ask for predictions from both users
- [ ] Both users must enter prediction before bet is finalized
- [ ] Syntax check dashboard_views.py

### 6.3 Prediction Entry in Thread
- [ ] Add "Enter Prediction" button for both participants
- [ ] Modal for entering numeric/text prediction
- [ ] Store prediction in database
- [ ] Show predictions in thread embed

### 6.4 Resolution Logic
- [ ] At resolution, compare actual result to predictions
- [ ] Winner = user with closest prediction (for numeric)
- [ ] Winner = exact match (for text)
- [ ] Handle tie-breaking
- [ ] Update verification.py with prediction comparison

### 6.5 Testing
- [ ] Test prediction entry flow
- [ ] Test numeric comparison (closest wins)
- [ ] Test exact match comparison
- [ ] Test tie scenarios

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
