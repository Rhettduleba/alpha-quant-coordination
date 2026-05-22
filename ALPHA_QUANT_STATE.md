# Alpha Quant — State of Record

**Version:** 3.7
**Last updated:** May 21, 2026
**Owner:** Rhett
**Scope:** Current operational state, open items, recent decisions. Stable rules/architecture live in the `CLAUDE.md` files (auto-loaded by Claude Code). Historical detail lives in `CHANGELOG.md`.

---

## Operating rules (every session, both Claudes)

1. **Verify before asserting.** No system-state claim without reading the file. If unread, label it "unverified."
2. **Surface conflicts, don't silently resolve them.** When two sources disagree, flag to Rhett — don't pick.
3. **No process actions without approval.** Restart bot, kill PID, deploy code, edit risk config → propose first, act after.
4. **Push back honestly.** Don't soften objections. Don't fake disagreement to look critical either.
5. **End every report with "What I did NOT verify."** Explicit section. Catches confabulation.
6. **One question per turn to Rhett.** Never stack multiple asks; never ask + report other items in the same turn.
7. **Times in user-facing text: 12-hour clock with AM/PM ET.** "9:09 AM ET" not "09:09 ET".
8. **Never reason from incomplete data.** Verify load-bearing claims at the source first. "probably / likely / should be" is a trigger to STOP and read the file.

---

## §1 Open items

The May-19 verification series **V1–V5 is all CLOSED**; **GIT is now CLOSED** (May 20 — see §2) — see `CHANGELOG.md` and §2. One item is open now:

| # | Item | Status |
|---|---|---|
| **OBS** | **Observation period** — watch the post-fix-sprint bot for 5+ clean trading days before any tuning or architectural work. | IN PROGRESS (started May 19) |

**OBSERVATION — what to watch, re-verify each trading day:**
- **Journal noise** should drop hard — from ~30k rows/day to ~1–3k/day — confirming the RTH-silence gate works. Count rows in `trade_journal.csv` per day.
- **Advisor reasoning** should come from clean data (memory wiped May 19, hardcoded baseline removed from the prompt). Watch `advisor_run_log.jsonl` and `advisor_memory.json` rebuild.
- **RECOMMEND_HALT behavior** — when the advisor emits `BLOCK_ALL_NEW_ENTRIES`, the bot should log `RECOMMENDED_HALT_NOT_HONORED` and keep trading, not block. Check `advisor_filter_engine.log`.
- **Reconciliation** — `python daily_reconciliation.py --date YYYY-MM-DD` should match broker truth.
- **Watchdog** — no new "Heartbeat stale" events in `watchdog_supervisor.log`.

---

## §2 Recent decisions (most recent first; full detail in `CHANGELOG.md`)

- **May 21, 2026, ~8:10 PM ET — Supervisor guardian added; "who watches the watchdog" gap closed.** Today's incident exposed it: the supervisor died and nothing restarted it. New `tradestation-bot/supervisor_guardian.py` + Windows Scheduled Task `AlphaQuant Supervisor Guardian` (every 2 min): if `watchdog_supervisor.py` is not running, the guardian kills any orphaned `run_bot` and relaunches the supervisor, firing a CRITICAL alert. If the process scan fails it does nothing (never acts on uncertainty). Task Scheduler — the OS — runs the guardian, so the watch chain now terminates at the OS and does not recurse infinitely. **Verified end-to-end:** killed the supervisor + run_bot; the guardian detected it and restored both within seconds. Watch chain: child scripts ← `run_bot` ← `watchdog_supervisor` ← `supervisor_guardian` ← OS Task Scheduler. Follow-up: fold the guardian task into `setup_autostart.py` so a future re-install keeps it.
- **May 21, 2026, 7:47 PM ET — Freeze fix + remaining PROP-SAFETY-002 bits DEPLOYED.** The supervisor was found dead — `run_bot` had been orphaned/unsupervised since ~4:04 PM ET (killed externally; no crash log). Restarted via the `AlphaQuant Bot Supervisor` scheduled task with the market closed and the account flat: new supervisor PID 5088 → new `run_bot` PID 9852, heartbeat now writing to `%LOCALAPPDATA%\AlphaQuant\bot_heartbeat.json` (verified fresh). Now live: watchdog debounce (3 consecutive stale reads) + exception logging, atomic/local heartbeat write, supervisor EOD window 3:50–4:20 PM, `run_bot` startup stale-order sweep. The whole PROP-SAFETY-001/002 + freeze-fix stack is now fully deployed.
- **May 21, 2026 — Recurring bot "freeze" root-caused as a FALSE POSITIVE; watchdog fixed.** The ~daily "Heartbeat stale — force restarting" events (May 16–21) were not real freezes. `bot_heartbeat.json` lived in the OneDrive-synced tree; OneDrive transiently locks synced files, so the watchdog's heartbeat read intermittently failed and it force-restarted a healthy bot — with no debounce (one failed read = instant kill). Proof: the "never written" signature means an *unreadable* file, not a stale-but-readable one (a real freeze leaves a readable file with an old timestamp). Today's noon event killed the bot mid-advisor-run, causing a duplicate midday advisor run (wasted Claude call). **Fix implemented + tested** (deploys on next supervisor restart): heartbeat moved out of OneDrive to `%LOCALAPPDATA%\AlphaQuant\bot_heartbeat.json` (`project_paths.HEARTBEAT_PATH`); `run_bot._write_heartbeat` writes atomically (temp + `os.replace`); `watchdog_supervisor` requires 3 consecutive stale reads before restart and now logs the real exception. Files: `project_paths.py`, `run_bot.py`, `watchdog_supervisor.py`, `bot_monitor.py`.
- **May 21, 2026 — PROP-SAFETY-001/002 went live and worked on real positions.** First live day: the EOD flatten closed both open positions (IWM, MCD) in ~2 seconds each at 3:50 PM ET (marketable DAY limit, attempt 1); all 35 intraday exits filled; account confirmed flat. The May 20 GOOGL failure mode did not recur. The advisor→bot universe channel (PROP-UNIVERSE-001) fell back cleanly to CORE_UNIVERSE while `advisor_universe_latest.json` was absent, then went active. A supervisor restart is still pending to deploy the remaining PROP-SAFETY-002 bits (supervisor EOD window 3:50–4:20, `run_bot` startup stale-order sweep) — the same restart deploys the freeze fix above.
- **May 21, 2026 — PROP-SAFETY-001/002 approved and implemented (dry-run tested).** Rhett approved both parts for implementation (recorded in `config/manual_approvals.yaml`). Implemented: new shared module `exit_orders.py` (`flatten_symbol` — marketable limit orders, DAY/GTC+ by clock, cancel-and-verify, poll-for-fill, adapt-on-reject, single-instance lock); `market_hours.py` (entry cutoff + forced flatten moved to 3:50 PM ET); `eod_watchdog.py` rewritten to use the helper + lock; `exit_bot_v2.py` exits routed through the helper, stuck-position skip blocks removed; `run_bot.py` startup sweep of stale prior-day orders; `watchdog_supervisor.py` EOD safety window widened to 3:50–4:20 PM. Tested: syntax, imports, unit tests, EOD dry-run self-test, simulated close-window run, and a live SIM order-format probe — all pass. The probe found the TradeStation API **rejects the literal `GTC+`** (`400 Invalid duration`); the correct submit code is **`GCP`** (Good-til-Cancelled Plus extended hours, which the order feed displays back as `GTC+` — matching Rhett's May 20 manual order). `exit_orders.py` corrected to emit `GCP`. **Still unverified:** the full submit→fill path with a real open position (account is flat) — covered by the proposal's controlled-SIM-rehearsal step. **Deployment note:** `run_bot.py` relaunches the child scripts each cycle from disk, so the exit/EOD changes go live at the next market open with no restart; the `run_bot.py`/`watchdog_supervisor.py` changes need a process restart to activate.
- **May 21, 2026 — EOD flatten failed on May 20; safety-fix proposal written (observation day 1 finding).** A GOOGL long (63 sh) was never closed by any automated path on May 20. The EOD watchdog submitted 83 sell orders 3:56–4:18 PM ET; TradeStation rejected **all 83** — 66 for `No Day orders after 4:00PM Eastern` (the watchdog builds every order as `Duration: DAY`; a market order is DAY-bound and rejected after 4:00 PM), the rest `EC703` (stale working order, never cancelled). The journal logged each rejection as `HTTP 200` because the watchdog never checks order status. Position was closed only by Rhett's **manual `GTC+` limit order at 4:18 PM ET** — not held overnight, but the automated safety net failed 100%. Verified from the `historicalorders` API (BROKER_TRUTH). Fix proposal: `ai-trading-strategy-agent/outputs/proposals/PROP-SAFETY-eod-and-exit-fix.md` — see §3. This is a safety fix and supersedes the observation hold.
- **May 20, 2026 — Advisor truncation bug found + fixed (observation day 1).** The May 20 08:05 advisor run hit *exactly* 2048 output tokens, truncating the response mid-JSON; `response_parser.py` rejected it (`parse_errors: 1`) and the advisor fell back to `NO_CONTROLS` / "Unable to parse advisor response" / `data_quality: POOR` — i.e. the advisor produced no real guidance that run. Bot unaffected (the `NO_CONTROLS` fail-safe = trade normally). Root cause: `MAX_TOKENS = 2048` in `claude_client.py:15`; the operational loop calls `call_claude()` with no explicit override. Fixed → `4096` (commit `1f19087`, `alpha-quant` repo). First parse failure in 45 logged runs. **Not a billing/funding issue** — the API call succeeded and returned a full 2048-token response; it was a config ceiling. This is exactly the kind of plumbing fault the observation period exists to catch.
- **May 20, 2026 — GIT open item CLOSED.** Bot + advisor code now under git. One repo (rooted at `Trade station Main`, captures both project folders + root docs/launchers) — chosen over two repos because cross-cutting changes like the fix sprint touch both halves and the bot↔advisor relative-path coupling means they ship as a unit. Git directory lives at `C:\repos\trade-station-main-git\` **outside OneDrive**, with `core.worktree` pointed into the OneDrive tree, so OneDrive never syncs git internals and there is **zero `.git` artifact inside OneDrive**. Initial commit `98620d9` = post-fix-sprint baseline, 303 files. `.gitignore` excludes secrets (`.env`, `token_cache*.json`), logs, journals (`trade_journal*.csv`), per-machine state, and runtime outputs. No pre-sprint history is recoverable. Pushed to a **private** GitHub remote: `github.com/Rhettduleba/alpha-quant` (pairs with `alpha-quant-coordination`).
- **May 19, 2026 — FIX SPRINT COMPLETE** (Rhett-approved, 7 steps): halted trading; added RTH-silence gate to `bot_loop.py` + `short_bot.py`; removed hardcoded wrong baseline from `prompt_builder.py:62-63`; archived + wiped `advisor_memory.json`; downgraded `BLOCK_ALL_NEW_ENTRIES` to a RECOMMEND_HALT semantic in `advisor_filter_engine.py`; implemented V5 `until=` pagination in `daily_reconciliation.py`; restarted trading. Full 7-step detail in `CHANGELOG.md`. **These bot/advisor code changes are NOT in git** — the GIT open item exists to fix that.
- **May 19, 2026 — V5 authoritative baseline:** 22-day broker truth = 1,194 fills, 593 closed pairs, **$-2,282.41 net, $-3.85/pair**. Supersedes the disproven SOR v1.7 "$-37,614 / 540-trade" baseline (overstated by ~$35k). Per-day detail in `V5_BROKER_TRUTH_BASELINE.json`.
- **May 19, 2026 — Profitability strategy drafted** — a five-wave plan (trade-quality filters → regime-aware promotion controls → richer advisor info → dynamic universe → re-fit scoring from clean data). Implementation deferred until the observation period confirms plumbing is stable. Doc currently held by Rhett; not yet in this repo.
- **May 19, 2026 — Browser-Claude coordination flagged unreliable.** Browser Claude's fetch tool returned fictional file content (claimed STATE.md was "v1.4" with sections that do not exist) and then accused Claude Code of confabulation. Verified false three independent ways — `git ls-remote`, GitHub branches API, raw fetch — all confirm `main` at the correct commit and STATE at v2.6/v2.7. Recommendation: only use a *fresh* browser-Claude session with content *pasted in* (never ask it to fetch); use the second AI for judgment questions, not facts.
- **May 19, 2026 — SYSTEM_REVIEW_PLAN v1.1** exists in this repo. Largely overtaken by the fix sprint, which shipped the high-priority fixes directly. Treat the formal R1–R8 investigation as optional — revisit only if the observation period surfaces a problem.
- **May 19, 2026 — Architectural-tweaks queue** (8 items: one-way-valve advisor, criteria-based universe, etc.) parked in Claude Code memory. Do NOT action during the observation period.

---

## §3 Active proposals

| Proposal | File | Status |
|---|---|---|
| **PROP-SAFETY-001** — Exit strategy: exits use marketable limit orders + fill verification. | `ai-trading-strategy-agent/outputs/proposals/PROP-SAFETY-eod-and-exit-fix.md` | APPROVED — IMPLEMENTED, dry-run tested |
| **PROP-SAFETY-002** — EOD flatten rebuilt: 3:50 PM start, marketable limits, `GTC+` after 4:00 PM, adapt-on-reject, cancel-and-verify, single-owner, honest confirmation. | (same file) | APPROVED — IMPLEMENTED, dry-run tested |
| **PROP-SAFETY-003** — SSR (Reg SHO Rule 201) handling for short entries: detect short-sale-restricted symbols and skip them, falling through to the next-best candidate. | `ai-trading-strategy-agent/outputs/proposals/PROP-SAFETY-003-ssr-short-entry.md` | PENDING_HUMAN_REVIEW — parked until observation period closes |

PROP-SAFETY-001/002 arise from the May 20 EOD flatten failure. Approved + implemented May 21 (§2). The after-4:00 PM extended-hours order code (`GCP`) was verified live on SIM May 21. Remaining: a controlled SIM rehearsal of the full submit→fill path with a real position, then a multi-day SIM observation of clean closes.

PROP-SAFETY-003 is a *preventive* gap from the May 21 short-vs-long robustness review — the short bot prices `SELLSHORT` limits at `last − $0.10` (hits the bid) with no SSR awareness, so the order can't execute on Rule-201-restricted names. Code-verified gap; live impact unobserved (SIM likely does not enforce Rule 201). Not an emergency — does **not** supersede the observation hold; expected to sit `deferred` until observation closes and live-readiness work begins.

---

## §4 Current bot / advisor state — SNAPSHOT, re-verify at next session start

This is a snapshot from the May 19 fix sprint. **A new session MUST re-read the live files for current state — do not trust these numbers as current.**

Last verified (May 19, ~1:14 PM ET):
- Bot PID 2360, alive, trading. First post-fix-sprint broker fill landed 1:13:59 PM ET.
- RTH-silence gate is live in code — bot goes silent outside ~9:30 AM–4:00 PM ET.
- `BLOCK_ALL_NEW_ENTRIES` patched — advisor may still emit it; bot logs `RECOMMENDED_HALT_NOT_HONORED` and keeps trading.
- `advisor_memory.json` wiped May 19 1:10 PM ET; rebuilding (1 clean run logged as of May 19 EOD).

**To get current state, read:** `tradestation-bot/bot_heartbeat.json`, `tradestation-bot/advisor_filter_engine.log` (tail), `tradestation-bot/watchdog_supervisor.log` (tail), `ai-trading-strategy-agent/outputs/advisor_guidance/advisor_control_latest.json`.

---

## §5 How to maintain this file

- Edit on state change; append a dated line to `CHANGELOG.md`.
- Roll §2 entries older than 7 days into `CHANGELOG.md`.
- Bump the version on every edit.
- Keep it slim. Architecture, risk floors, control vocabulary, SIM guards, working rules → `CLAUDE.md`, not here.
- C1 (`AQ_EVALUATION_STANDARDS_C1.md`) is fetched only when evaluating a proposal.
