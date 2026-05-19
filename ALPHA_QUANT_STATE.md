# Alpha Quant — State of Record

**Version:** 2.3
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
| V4 | Re-verify the 540-trade / $-37,614 baseline using broker fills | Reconciliation across the 22-day window | **PARTIAL — significant finding.** For the 11 trading days May 1-18 (with May 15 as a no-trade day), broker truth shows **297 closed pairs, $-2,846.49 net of fees** (avg $-9.58/pair). The earlier 10 days (April 17-30) returned zero broker fills — cause unknown, see V5. For the 11 verifiable days, the journal-derived methodology overstated losses by roughly $35k vs. broker truth. |
| V5 | Distinguish: did the 600-order API cap truncate April 17-30 fills, or was the bot not running then? | Test `historicalorders` pagination + check earliest run_bot.py launch | **NEW.** Needed to fully close V4. If pagination works, complete the 22-day reconciliation. If the bot truly wasn't running in late April, the SOR v1.7 "540 trades over 22 days" claim was wrong about the window, not just the methodology. |

---

## §2 Recent decisions (last 7 days)

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
- **Advisor last run:** 8:04 AM ET May 19 (PRE_MARKET, post-prompt-fix). Control file TTL valid through 8:04 AM ET May 20.
- **Advisor next scheduled:** 12:30 PM ET May 19 (MID_DAY).
- **Heartbeat-stale events on May 19:** 0.
- **Today's regime read (from 8 AM advisor):** BROAD_SELLOFF, 86% bearish symbols, data quality POOR.
- **Active controls in force:**
  - `BLOCK_ALL_NEW_ENTRIES` — reason cited "Market is closed" (advisor ran at 8:04 AM, ~86 min before market open). Control persists until next advisor run at 12:30 PM. **Means the bot will not enter new positions from market open (9:30 AM) until at least 12:30 PM today — ~3 hours of trading time blocked.**
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
