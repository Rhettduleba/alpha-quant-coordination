# Session Handoff — Backtesting & the advisor learning loop

- **Date:** May 21, 2026 (evening session, VPS)
- **Author:** Claude Code
- **Session topic:** Alpha Quant backtesting — review the existing backtest tooling, fix what's broken, and design how the advisor should learn from backtest evidence.
- **Cost note for the next session:** everything done here was zero-API-cost (local compute + git). No Claude API calls, no TradeStation API calls were made.

---

## 1. TL;DR

The session set out to run backtesting. It found the existing backtest tooling was producing fiction, fixed the cause, found the same bug was corrupting the **live advisor's** pattern learning, fixed that too, and then established what a *trustworthy* backtest must be built on. A design proposal (`PROP-LEARN-001`) was drafted for how the advisor learns from backtest evidence.

**Bottom line:** the bot's risk machinery was not touched and is unaffected. But the advisor has, until today, been learning patterns from badly corrupted data. The corruption is now removed; the data is "much less wrong" but still not broker-truth-accurate — the real fix is scoped in `PROP-LEARN-001` and is gated on the observation period.

---

## 2. What was done, in order

1. **Ramp-up.** Read `ALPHA_QUANT_STATE.md`, the feedback memory files, re-verified §4 live state. Bot was alive (PID 1708, loop 1441). Advisor control file valid (15 active controls). Noted a 12:02 PM ET watchdog restart — later confirmed as the known OneDrive-heartbeat-lock false positive (STATE v3.4), not a new fault.
2. **Ran `tradestation-bot/backtest.py`.** It reported 30,613 closed pairs / **+$1,222,396 net**. Broker truth (V5 baseline) for the comparable window is 593 pairs / **−$2,282**. The tool was producing fiction.
3. **Root-caused it.** `load_all_journal_rows()` in `ai-trading-strategy-agent/src/advisor/trade_pattern_analyzer.py` globbed **every** `trade_journal*.csv` file (56 files, ~27M rows). Those machine-suffixed files are overlapping per-machine rotation snapshots of the *same* journal — every trade was multiply-counted ~27×.
4. **Fixed it** (after Rhett reversed an initial "defer" decision to "fix now"). De-duplicate each relevant row on its full content before FIFO matching. **Commit `675dcf5`** in the `alpha-quant` code repo. One fix corrects both `backtest.py` and the live advisor (they share the loader). Verified: 34,346→1,342 rows, 30,613→1,143 pairs, +$1.22M→**+$25,925**.
5. **Found the bug had reached the live advisor.** `build_full_pattern_analysis()` (same module) writes `learned_patterns.json`, which is injected into every Claude advisory prompt. The on-disk `learned_patterns.json` was **9 days stale (May 12) AND corrupt**: 25,526 trades / +$1,070,415, with physically impossible artifacts (32-hour average holds; a "481 wins / 0 losses" setup). Today's advisor control file cited it verbatim ("MSFT −$84,211 all-time").
6. **Regenerated `learned_patterns.json`** with the fixed loader. Corrupt original backed up to `ai-trading-strategy-agent/outputs/advisor_guidance/learned_patterns.CORRUPT-pre-dedup-fix-2026-05-21.json.bak`. New file: 1,143 trades / +$25,925, date range now current.
7. **Verified the regenerated file is still flawed.** 607 of 1,143 pairs (53%) "hold" longer than a full trading day — impossible for a bot that flattens by 3:50 PM. Root cause: the journal logs order *submissions*, not fills (of 1,342 rows: 1,271 status `HTTP 200` = submit accepted, only 35 `FILLED`, 1 rejected `HTTP 400` still counted). Journal-based analysis is structurally `LOCAL_RECONSTRUCTION` and cannot match broker truth.
8. **Evaluated a ChatGPT handoff** ("Advisor Learning From Backtesting"). Found the framework sound; added 7 refinements (data-source prerequisite, define backtest type, concrete overfitting controls, reuse existing scaffolding, cost discipline, etc.).
9. **Drafted `PROP-LEARN-001`** — `ai-trading-strategy-agent/outputs/proposals/PROP-LEARN-backtest-learning-loop.md`.
10. **Verified the broker-truth fix is mostly an assembly job.** `ai-trading-strategy-agent/outputs/cache/broker_truth/*.json` already contains `broker_trades` arrays — FIFO-paired closed trades with real fill prices/times — that reproduce `V5_BROKER_TRUTH_BASELINE.json` per-day P&L to the penny (9/9 cached trading days checked). Updated `PROP-LEARN-001` §9 Phase 0 accordingly.

---

## 3. Key findings

| # | Finding | Status |
|---|---|---|
| F1 | `load_all_journal_rows()` multiply-counted trades ~27× by globbing all rotation-snapshot journals. Hit both `backtest.py` and the live advisor. | **FIXED** — commit `675dcf5` |
| F2 | Live `learned_patterns.json` was 9-day stale + corrupt (+$1.07M, impossible artifacts); advisor cited it into control files. | **FIXED** — regenerated, corrupt copy backed up |
| F3 | Even deduped, the journal is a submission log, not a fill log → journal-based backtesting/pattern-learning is structurally `LOCAL_RECONSTRUCTION`, cannot match broker truth, overstates win rate, flips P&L positive. | Open — addressed by `PROP-LEARN-001` Phase 0 |
| F4 | The broker-truth per-trade dataset **already exists** in `outputs/cache/broker_truth/*.json` and matches V5 exactly. The proper fix is assembly, not a from-scratch build. | Informational |
| F5 | `backtest.py` ignores commissions; V5 shows commissions ($1,365) exceed the gross loss — so omitting them flips conclusions. | Open — noted in `PROP-LEARN-001` |
| F6 | Large amount of uncommitted production code in the `alpha-quant` working tree (all the PROP-SAFETY work, the `src/brain/` research brain). Only the truncation fix and today's `675dcf5` are committed. | Flagged — not this session's job |
| F7 | `pytest` shows 10 pre-existing failures (test_v1_agent, test_dashboard_routes, test_ingest, etc.). Verified none touch `trade_pattern_analyzer` — not caused by today's change. | Flagged |

---

## 4. Code & artifact changes

**Code repo (`alpha-quant`, git dir `C:\repos\trade-station-main-git\.git`):**
- Commit `675dcf5` — "Fix journal double-counting in load_all_journal_rows()". One file: `ai-trading-strategy-agent/src/advisor/trade_pattern_analyzer.py`. **Committed locally, NOT pushed to the remote** — left for Rhett, since pushing production code is a propose-first action.

**Advisor outputs:**
- `outputs/advisor_guidance/learned_patterns.json` — regenerated (corrected data).
- `outputs/advisor_guidance/learned_patterns.CORRUPT-pre-dedup-fix-2026-05-21.json.bak` — the corrupt original, for revert/audit.
- `outputs/proposals/PROP-LEARN-backtest-learning-loop.md` — new proposal `PROP-LEARN-001` (AWAITING HUMAN APPROVAL).

**Coordination repo (`alpha-quant-coordination`) — committed and pushed:**
- `CHANGELOG.md` — finding + fix entries.
- This handoff file.

**Memory (Claude Code auto-memory):**
- New: `feedback_objective_proactive.md` — be objective, push back only when genuinely needed, be proactive.
- Reinforced: `feedback_just_do_the_work.md` — anything I think I should do, I do that turn; "what I did NOT verify" is not a parking lot.
- `MEMORY.md` index updated.

---

## 5. State of `PROP-LEARN-001` (the deliverable to act on next)

A design proposal for how the advisor learns from backtesting. **AWAITING HUMAN APPROVAL — design only, nothing builds until approved AND the observation period ends.**

Core content:
- The handoff's learning loop is adopted (study → recommend → human approves → retest → accept only if it beats a null baseline and overfitting is controlled).
- **§3 — the hard prerequisite:** the loop must be fed broker truth, not the journal.
- **§5 — concrete overfitting controls:** out-of-sample holdout, walk-forward, minimum sample size, multiple-comparisons guard, null baseline.
- **§9 — 6-phase build plan.** Phase 0 (broker-truth dataset) is mostly assembly: consolidate the existing `broker_trades` cache arrays → backfill dates not yet cached (cache stops ~May 1) → net in commissions → join the journal as a metadata sidecar for exit reason / signal score. Acceptance test: reproduce V5 (593 pairs / −$2,282).

**Four open questions for Rhett** (`PROP-LEARN-001` §10): backtest type (what-if vs price-replay); train/test policy + minimum-trades bar; whether to fold the live-advisor pattern-source fix into Phase 0; cadence (weekly / monthly / on-demand).

**Implementation model agreed in discussion:** backtesting is NOT wired into the trading loop. It runs offline, beside the loop, and feeds the bot only through the existing human gate (proposal → `manual_approvals.yaml` → applied as a normal propose-first change → SIM observation). The backtest narrows candidates; the live SIM forward-test validates them. No auto-tuning.

---

## 6. What was deliberately NOT done (and why)

- **No full advisor run / control-file rewrite triggered.** That rewrites the live file the bot obeys — propose-first, and the scheduled 8:00 AM ET run will pick up the corrected cache anyway.
- **No patch to `build_all_closed_trades`** to force same-day matching (which would hide the 53% impossible-holds artifact). Deliberate — that polishes the wrong data source; the correct fix is broker-truth sourcing (Phase 0).
- **Commit `675dcf5` not pushed** to the code remote.
- **No build work on `PROP-LEARN-001`** — it is architectural; gated on the observation period.

---

## 7. For the next session

1. **Re-verify live state first** — per `ALPHA_QUANT_STATE.md` §4. Bot/supervisor state changed during/after this session (CHANGELOG records STATE v3.5/v3.6 — supervisor restart, new `supervisor_guardian.py`). STATE.md is now at v3.6. Do not trust this handoff's §2 ramp-up numbers as current.
2. **Tomorrow's 8:00 AM ET advisor run** will read the regenerated (corrected) `learned_patterns.json` for the first time. Worth checking the resulting control file looks sane.
3. **`PROP-LEARN-001` needs Rhett's four §10 answers** before Phase 0 can be scoped into a build.
4. The observation period (STATE.md §1, OBS) is still in progress — no tuning/architecture until it completes. `PROP-LEARN-001` build waits for that.
5. Open housekeeping (not urgent): push `675dcf5`; the large uncommitted code-repo working tree (F6); the 10 pre-existing pytest failures (F7).
