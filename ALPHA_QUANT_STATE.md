# Alpha Quant — State of Record

**Version:** 2.6
**Last updated:** May 19, 2026
**Owner:** Rhett
**Scope:** Current operational state, open verifications, recent decisions.
Stable rules and architecture live in the repo's `CLAUDE.md` files (auto-loaded by Claude Code).
Historical edits live in `CHANGELOG.md`.

> This file replaces `ALPHA_QUANT_STATE.md` v1.7. Slimmed deliberately — anything stable,
> architectural, or historical was moved out. If something here doesn't change session to
> session, it belongs in `CLAUDE.md` instead.

---

## Operating rules (every session, both Claudes)

1. **Verify before asserting.** No system-state claim without reading the file. If unread, label it "unverified."
2. **Surface conflicts, don't silently resolve them.** When two sources disagree, flag to Rhett — don't pick.
3. **No process actions without approval.** Restart bot, kill PID, deploy code, edit risk config → propose first, act after.
4. **Push back honestly.** Don't soften objections. Don't fake disagreement to look critical either.
5. **End every report with "What I did NOT verify."** Explicit section. Catches confabulation.
6. **One question per turn to Rhett.** Never stack multiple asks; never ask + report other items in the same turn.
7. **Times in user-facing text: 12-hour clock with AM/PM.** "9:09 AM ET" not "09:09 ET". Know the current time.

---

## §1 Open verifications

| # | Verification | Trigger | Status |
|---|---|---|---|
| V1 | Prompt fix removes the 11 AM `BLOCK_ENTRIES_AFTER_TIME` nudge | 8 AM advisor run May 19 | **RESOLVED (nuanced).** The 11 AM block from the deleted prompt lines is gone. Advisor independently emitted a new `BLOCK_ENTRIES_AFTER_TIME` at **3:00 PM ET** based on data ("Worst setups cluster at 15:xx for META LONG and NVDA SHORT"). Architecture working as designed — prompt no longer biases, advisor reasons from data. |
| V2 | PID 2360 survives the 8 AM advisor run with no Heartbeat stale event | 8 AM advisor run May 19 | **PASSED.** PID 2360 alive at 9:09 AM ET May 19, loop_count 3254. **Zero "Heartbeat stale" events on May 19** (every day May 13-18 had one at ~8:03 AM). Option B freeze fix verified. |
| V3 | TradeStation UI shows ~$-378.70 for May 18 daily P&L | Rhett checks TS UI | **CLOSED (no UI validation available).** SIM accounts don't expose P&L through the TradeStation web UI. We trust the broker API result: $-378.70 net of fees ($-326.10 gross + $52.60 commissions). |
| V4 | Re-verify the 540-trade / $-37,614 baseline using broker fills | Reconciliation across the 22-day window | **CLOSED by V5.** See V5 below. |
| V5 | Get full 22-day broker baseline (was: pagination missing / bot not running?) | `historicalorders?since=&until=` server-side scoping | **CLOSED May 19, 2026.** TS API supports `until=` (verified). Modified `get_broker_fills()` to send both. Full result: **1,194 fills, 593 closed pairs, $-2,282.41 net, avg $-3.85/pair across 21/22 trading days April 17 to May 18**. The 600-cap was silently truncating the older 10 days; `until=` scopes server-side and eliminates the cap. Authoritative result in `V5_BROKER_TRUTH_BASELINE.json`. The bot WAS running in late April (not pre-launch as one hypothesis suggested) — the missing data was purely the API cap. The SOR v1.7 cited "$-37,614" baseline was overstated by ~$35,331. |

---

## §2 Recent decisions (last 7 days)

- **May 19, 2026, ~1:00–1:30 PM ET** — **FIX SPRINT EXECUTED (Rhett-approved, all 7 steps complete).**
  1. **Trading halted** via `daily_shutdown.json` (`shutdown_active=true`, reason: fix sprint). Verified bot logs `Daily shutdown active` for both bot_loop and short_bot at 1:07 PM ET.
  2. **RTH-silence gate** added to `tradestation-bot/bot_loop.py` (line 173) and `tradestation-bot/short_bot.py` (line 172): immediately after SIM account confirmation, `is_market_open()` is checked; if false, `raise SystemExit(0)` skips all per-cycle work. Heartbeat continues to be written by `run_bot.py:470`. Syntax verified PASS for both.
  3. **Hardcoded wrong baseline removed** from `ai-trading-strategy-agent/src/advisor/prompt_builder.py:62-63`. The "25,520 all-time trades, 57.0% win rate, $42.02 avg P&L" and "SHORT trades 32.2% win rate, -$70.29 avg P&L" lines were derived from journal limit prices and V4-disproven. Replaced with explanatory note pointing advisor to reason from recent-performance + historical-pattern sections (not a single global claim).
  4. **`advisor_memory.json` archived + wiped.** Prior 27-run memory (20.2 KB) preserved at `Archive/Root_Cleanup_2026-05-19/advisor_memory_2026-05-19_pre_wipe.json`. Active memory reset to blank `_blank_memory()` schema with a `wipe_history` audit field recording why and where the original lives.
  5. **`BLOCK_ALL_NEW_ENTRIES` downgraded to RECOMMEND_HALT semantic** in `tradestation-bot/advisor_filter_engine.py:129-138`. Bot now returns `block=False` and logs `RECOMMENDED_HALT_NOT_HONORED` with the advisor's reason. Advisor keeps alarm capability; bot keeps trading; humans use `daily_shutdown.json` to actually halt. Functional test PASS — emitted BLOCK_ALL no longer blocks any entry.
  6. **V5 pagination implemented + baseline reconciliation complete.** Probe found TS API supports `until=` parameter (verified) and `pageSize=N`+`NextToken` cursor pagination. Used `until=` for server-side date-range scoping; modified `get_broker_fills()` in `daily_reconciliation.py` to send `&until=<date+1>` alongside `since=`, eliminating the 600-cap silent truncation. Full 22-day window (April 17 to May 18) now returns: **1,194 fills, 593 closed pairs, $-2,282.41 net of $1,365.54 fees, avg $-3.85/pair**. Authoritative baseline saved to `V5_BROKER_TRUTH_BASELINE.json` in this repo.
  7. **Bot trading restarted** by clearing `daily_shutdown.json` (`shutdown_active=false`). Verified next bot cycle resumed normal evaluation.
- **V4/V5 reconciled comparison:**

  | Source | Closed pairs | Net P/L | Avg per pair | Window |
  |---|---:|---:|---:|---|
  | SOR v1.7 cited "baseline" | 540 | $-37,614 | $-69.66 | 22 days (per claim) |
  | **V5 broker truth (authoritative)** | **593** | **$-2,282.41** | **$-3.85** | 22 days (April 17 to May 18) |
  | Delta vs cited | +53 | +$35,331.59 | +$65.81 | — |

  The cited "verified baseline" was overstated by ~$35k. Real system performance is nearly break-even, not the catastrophic loss the prior baseline implied. V5 closes the V4 partial finding and supersedes the prior cited number.
- **May 19, 2026, ~11:20 AM ET** — **Bot manually unblocked for today.** Rhett approved editing `advisor_control_latest.json` to remove the `BLOCK_ALL_NEW_ENTRIES` entry. Other controls (BLOCK_SYMBOL × 3, REQUIRE_MIN_NEG_CHANGE_PCT, SET_MAX_POSITION_PCT, REDUCE_MAX_POSITIONS, BLOCK_ENTRIES_AFTER_TIME) left intact. Verified at 11:18:41 AM ET: bot's filter engine now returns `block=False ALL_CONTROLS_PASSED`. `manual_edits[]` array added to the control file recording the change. Next advisor run at ~12:00 PM ET will overwrite.
- **May 19, 2026** — **Q1 DECIDED (Rhett):** Bot stays running 24/7 but goes SILENT outside RTH via `is_market_open()` gate — no scanning, no journal writes when market closed. Smaller change than process lifecycle machinery; watchdog already keeps process warm. Implementation lands as part of R1–R8 execution (P0 candidate).
- **May 19, 2026** — **Q2 REFRAMED (browser Claude + Rhett):** Don't delete `BLOCK_ALL_NEW_ENTRIES` — downgrade it to a `RECOMMEND_HALT` semantic that surfaces for human confirmation rather than a control the bot silently honors. Preserves advisor's ability to flag real concerns without unilateral total-halt power. Implementation folds into R8.
- **May 19, 2026** — SYSTEM_REVIEW_PLAN v1.1 published with browser-Claude review corrections folded in: §3 relabeled as hypothesis, R3 widened to all 9 control types, R4 expanded with advisor_memory.json inspection, midday slot corrected from 12:30 PM to ~12:00 PM ET (verified empirically). Q6 flagged as unresolved — browser Claude's cited "STATE §6" doesn't exist in actual STATE.md.
- **May 19, 2026** — System Review Plan v1.0 written and pushed to `SYSTEM_REVIEW_PLAN.md` in this repo. Triggered by Rhett's correct observation that the bot runs 24/7 and logs 20k+ "Market closed" rejections per day (including weekends), and that the advisor reads this noise and emits `BLOCK_ALL_NEW_ENTRIES` defensively (May 15 lost a full trading day this way; May 19 lost the morning). Plan proposes R1–R8 investigation scope, fix prioritization framework, and explicit no-performance-work-until-plumbing-fixed hard rule. Awaiting browser Claude's review per Rhett's direction.
- **May 19, 2026** — V4 partial result: for 11 trading days (May 1-18), broker truth shows 297 closed pairs / $-2,846.49 net of fees. SOR v1.7's claimed "540 trades / $-37,614" baseline is materially overstated for this verifiable window. The earlier 10 days (April 17-30) returned zero broker fills via `historicalorders?since=` — cause distinguishing TBD in V5. Per-day breakdown was generated in the bot folder and discarded; rerunnable any time by re-creating the V4 script that loops `get_pnl_for_date` over a date list.
- **May 19, 2026** — Workspace root cleanup: archived 14 items (Marketing/, Learning/, Trades/, Launchers/, Sync/, broken .lnk launchers, handoff docs, build_discussion_log.js, etc.) to `Archive/Root_Cleanup_2026-05-19/`. Deleted stale v1.7 .md duplicates at root (canonical lives in this repo). Root now shows exactly five files: `Start TradeStation Bot.bat`, `Stop TradeStation Bot.bat`, `Start_Dashboard.bat`, `Alpha_Quant_Discussion_Log.docx`, `CLAUDE.md`.
- **May 19, 2026** — Replaced broken .lnk bot launchers with new portable .bat files. **Start TradeStation Bot.bat** launches `watchdog_supervisor.py` with a duplicate-detection safety check (filters to `python.exe` to avoid self-referencing PowerShell). **Stop TradeStation Bot.bat** runs `exit_bot.py` to flatten open positions, then kills all `python.exe` matching `watchdog_supervisor.py` or `run_bot.py` by command-line. Old .lnk files targeted hardcoded `C:\Users\rdule\...` paths from an old user profile AND called `run_bot.py` directly, which would conflict with the modern watchdog architecture.
- **May 19, 2026** — Rewrote `Alpha_Quant_Discussion_Log.docx` as a living Q&A tracker. 19 questions ported, Rhett text in black, Claude text in blue, italic-bold date-stamped speaker labels, gray paragraph shading + `[done]` tag for 6 questions (Q2 scan-speed, Q7 position-cap, Q12 stop-loss-correction, Q14 call-frequency, Q15 scoring-acknowledged, Q16 time-blocking-pushback) — Rhett to confirm/edit. Original archived to `Archive/Alpha_Quant_Discussion_Log_2026-05-18_original.docx`.
- **May 19, 2026** — TradeStation API endpoint inventory recorded. Working on SIM: `/brokerage/accounts`, `/balances`, `/bodbalances`, `/positions`, `/orders`, `/historicalorders?since=`, `/marketdata/quotes`, `/symbols/{symbol}`, `/barcharts/{symbol}`, `/symbols/{symbol}/news`. NOT available: `/executions`, `/fills`, `/activities`, `/transactions` (404), `/marketdata/options/*` (403). `/historicalorders?since=` is capped at **600 orders per call** — pagination required for windows longer than ~11 trading days at current volume.
- **May 19, 2026** — Built scope S of the broker-truth library: `get_pnl_for_date(date_str, account_id=None, client=None)` in `tradestation-bot/daily_reconciliation.py`. Returns dict with `gross_pnl`, `commissions`, `routing_fees`, `net_pnl`, `fill_count`, `closed_pair_count`, `fills`, `closed_pairs`, `source="TRADESTATION_HISTORICAL_ORDERS"`. Smoke-tested against May 18: `net_pnl = $-378.70`, matches the full reconciliation script.
- **May 19, 2026** — Fixed three pre-existing bugs in `tradestation-bot/daily_reconciliation.py`: (1) was calling `/brokerage/accounts/{id}/orders` (current-orders endpoint, returns 0 for past dates) — switched to `/historicalorders?since=`; (2) `parse_broker_order` read `order["TradeAction"]` which doesn't exist top-level — now derives action from leg's `BuyOrSell` + `OpenOrClose`; (3) `compute_pnl_from_fills` processed fills in reverse-chrono API order, losing pair matches — now sorts chronologically; `reconcile` didn't consume matched fills — now tracks `consumed_order_ids`. Surfaced commissions as a separate line.
- **May 19, 2026** — Rule set: Claude Code executes every read-only / local-analysis / coordination-repo action without asking. Still propose-first for: restart bot, kill PID, deploy bot code, edit risk config / risk floors / control vocabulary, modify advisor control files the bot reads.
- **May 19, 2026** — SOR process slimmed. v2.0 replaced v1.7. Single-machine + single-toolchain commitment retires cross-machine concerns. CHANGELOG.md is now the running edit log.
- **May 18, 2026** — Prompt-builder edit: removed two `BLOCK_ENTRIES_AFTER_TIME` nudges from `ai-trading-strategy-agent/src/advisor/prompt_builder.py`. Control type stays in vocabulary; independent reasoning can still emit it. First visible effect: PRE_MARKET advisor run May 19 — see V1 resolution above.
- **May 18, 5:35 PM ET** — Watchdog auto-restarted bot from frozen PID 5468 (pre-fix code) to PID 2360 (first instance running the fixed `run_bot.py` Option B). PID 2360 has now run continuously through the May 19 8 AM advisor slot — see V2 resolution above.

---

## §3 Active proposals

_None tracked yet. Populate from `ai-trading-strategy-agent/outputs/proposals/` when a proposal is awaiting Rhett's approval. Format per row: filename, one-line summary, the blocking question for Rhett._

---

## §4 Current bot / advisor state

- **Bot:** PID **2360**, alive, last_seen 9:09 AM ET May 19, loop_count 3254. Continuous uptime ~15.5 hours since the May 18 5:35 PM ET restart.
- **Advisor last run:** 8:04 AM ET May 19 (PRE_MARKET, post-prompt-fix). Control file TTL valid through 8:04 AM ET May 20. Control file was manually edited at ~11:18 AM ET to remove `BLOCK_ALL_NEW_ENTRIES` and unblock the bot.
- **Advisor next scheduled:** ~12:00 PM ET May 19 (MID_DAY) — verified from empirical run log, NOT 12:30 PM as `run_advisor.py:22-25` docstring claims (stale).
- **Heartbeat-stale events on May 19:** 0.
- **Today's regime read (from 8 AM advisor):** BROAD_SELLOFF, 86% bearish symbols, data quality POOR.
- **Active controls in force:**
  - ~~`BLOCK_ALL_NEW_ENTRIES`~~ — **REMOVED via manual edit at 11:18 AM ET May 19 per Rhett approval. Bot is now trading normally.**
  - `BLOCK_SYMBOL` × 3: MSFT, AAPL, META
  - `REQUIRE_MIN_NEG_CHANGE_PCT` −0.8%
  - `SET_MAX_POSITION_PCT` 0.15
  - `REDUCE_MAX_POSITIONS` 2
  - `BLOCK_ENTRIES_AFTER_TIME` 3:00 PM ET — newly emitted today from data-driven reasoning, replacing yesterday's prompt-driven 11:00 AM block

---

## §5 How to maintain this file

- Edit STATE.md when state changes; append one dated line to `CHANGELOG.md`.
- Roll §2 entries older than 7 days into `CHANGELOG.md`.
- Bump the version on every edit (2.0 → 2.1 → 2.2 …).
- Don't grow this file. Architecture, risk floors, control vocabulary, SIM guards, working rules → all already in the project `CLAUDE.md` files. Do not duplicate here.
- C1 (`AQ_EVALUATION_STANDARDS_C1.md`) is fetched only when evaluating a proposal — not at ramp-up.
