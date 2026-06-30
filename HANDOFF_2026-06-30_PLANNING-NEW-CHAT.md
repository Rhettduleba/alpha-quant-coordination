# ALPHA QUANT — PLANNING SESSION HANDOFF (new chat ramp-up)
**Written 2026-06-30 ~11:25 AM ET by Claude Code (Opus 4.8, the VPS empirical node) for a fresh Planning Claude chat.**
The prior Planning chat got too long to continue. This document ramps you (new Planning Claude) from cold.

---

## 0. WHO YOU ARE & HOW THIS PROJECT IS STAFFED
- **You are "Planning Claude"** — the strategy/architecture brain. You run in Rhett's Claude app (NOT a terminal). You think, design, propose, and decide what work to hand to Claude Code. You do NOT touch the VPS directly.
- **"Claude Code"** = me, running on the VPS (`WIN-FIBSSOQKI7K`, live root `C:\AlphaQuant`). I read/write the real files, run the bot, verify against broker truth, and report back. I push back on plans that don't survive contact with live data.
- **Rhett (Duleba)** = owner/operator. Not a day-trading expert by trade; this is OUR project. He owns every gate that changes live behavior, risk, or universe. He relays handoffs between you and me.
- **Working split:** You propose → I verify/stress-test/build → Rhett approves anything that changes live trading behavior. I will tell you when a plan's premise is wrong (it has happened 3× this week — see §6).

## 1. READ THESE FIRST (in order) — do not plan from memory
On the VPS these live under `C:\AlphaQuant\`. Ask Rhett to have me paste any you need.
1. **`CLAUDE.md`** (repo root) — operational primer + the architectural rules + the typed advisor→bot control vocabulary. **The single most important file.**
2. **`ALPHA_QUANT_HANDOFF.md`** — the deep architecture write-up (start here for the "why").
3. **`SESSION_LOG.md`** — the living turn-by-turn log + crash-recovery brief. **Top "CURRENT STATE" block = today's posture; "FINDINGS & TEST RESULTS LEDGER" = what every recent study found; "VERIFIED LEDGER" (newest first) = per-loop work.** This is the canonical handoff surface between you and me — I update it every turn.
4. **`CSHV_FINDINGS.md`** — Continuous System Health Verifier output (runs every 5 min). Any FAIL/WARN here outranks other work.
5. **`bot_alerts.jsonl`** — append-only critical bot events (every scan/entry/SL/EOD/auth failure). Run `python C:\AlphaQuant\tradestation-bot\alerts_bridge.py` for a 24h summary.
6. **`ai-trading-strategy-agent/V1_SCOPE.md`** — what's ACTIVE vs PARKED in the advisor repo (don't assume "in repo" = "in the live path").
7. **`ai-trading-strategy-agent/outputs/advisor_guidance/advisor_control_latest.json`** — what the bot will actually obey today.
8. **`tradestation-bot/advisor_filter_engine.py`** + **`bot_loop.py`** + **`risk_config.py`** — the only advisor interpreter, the single bot cycle, and the hard risk floor.
9. **Coordination repo** `C:\repos\alpha-quant-coordination` (public GitHub Rhettduleba/alpha-quant-coordination) — gets the SESSION_LOG mirror + CHAT_LOG each turn. This is how you can see my latest work without Rhett copy-pasting.

## 2. WHAT THE SYSTEM IS (60-second architecture)
Two **separate** Python systems that share ONE JSON file and never import each other:
- **The Bot** (`tradestation-bot/`) — places SIM equity orders on TradeStation, enforces risk. Intentionally narrow, dumb, reviewable. Strategy = **ORB (Opening Range Breakout) v1.6**. Entry point `run_bot.py` → per-cycle `bot_loop.py`. Runs a single sequential subprocess loop: LONG entry → SHORT entry → ORB RUNNER (9:35 scan + stop placement) → ORB MULTI-SCAN (re-arm) → EXIT BOT → EOD WATCHDOG. `orb_runner`/`orb_multiscan` spawn fresh each cycle (pick up code edits immediately, no restart).
- **The Advisor** (`ai-trading-strategy-agent/`) — Claude-driven daily analysis + research/dashboards. May be smart and opinionated. Writes ONE typed JSON control file; the bot reads it with paranoid validation.
- **THE ARCHITECTURAL RULE (do not violate):** *The agent should know a lot. The bot should do only what has been proven.* The advisor never reaches into bot config. It writes one typed file; the bot interprets ONLY a fixed vocabulary of control types and **defaults to ALLOW** if the file is missing/stale (a dead advisor must never lock the bot out).

## 3. SIM-ONLY — NON-NEGOTIABLE
- Account `SIM1623888M`. Bot refuses to start if the account ID doesn't begin with `SIM`.
- Advisor stamps every control file `environment: "SIM_ONLY"`, `live_allowed: false`.
- Never edit those guards or add a path that bypasses them. We are NOWHERE NEAR live.

## 4. WHERE WE ARE IN THE STAGED RAMP (6 stages)
1. Verify environment ✓
2. Reporting & reconciliation ✓
3. **SIM testing with full logs ← HERE**
4. **AI advisor layer ← actively shipping, not yet trusted to graduate**
5. Controlled strategy improvements (gated)
6. Carefully controlled live trading (only with explicit human approval)
**Nothing should quietly advance the system past where Rhett has approved it.** P&L is NOT the success metric right now — diverse, correct, well-logged trades are. SIM resets when a winning + bug-free system is confirmed.

## 5. HISTORICAL ARC (how we got here — the short version)
- **Strategy rebuilt on evidence.** The old backtested strategy was −99.92%. We rebuilt around **ORB** (H1 hypothesis). Universe is **criteria-based / whole-exchange** (research brain), not a hardcoded symbol list.
- **Central finding (3-day dollar split, real broker fields):** the **9:35 AM morning entries are the loss engine**; the **re-arm path made money all 3 days → DO NOT TOUCH the re-arm path.** Preventable-at-ENTRY losses 60% vs manageable-at-EXIT 40%. The entry lever that matters is **extension magnitude**, not relative strength.
- **Exit experiments.** A "Loop-123" aggressive exit was forward-tested and **KILLED 6/25** (day −$2,016 < −$2k stop; one name −$1,670). Rhett's FINAL call: do NOT revert — **keep the live `candle_1.4atr_chandelier` exit, improve in SHADOW only.** Shadow studies (L1/L2 entry guards, combined) cut 3-day red −81% with 0 winners cut but are N<30 → DIRECTIONAL ONLY, not promoted.
- **$500 per-trade dollar-cap exit — LIVE (Loop 187).** `DOLLAR_STOP_CAP=500`, `DOLLAR_STOP_CAP_ENABLED=True` in `risk_config.py`; placed in `orb_runner` as `sl_dist = min(1.4×ATR, $500/qty)`. Replay proved it recovers ~+$1,672 across the bad days, and **no managed-exit rule we studied beats the flat $500 floor.**
- **6/29 incident.** Re-arm fills had **0% resting-stop coverage** + the TW (Tape Watcher) live-exit owner was the sole protection with day-1 stream gaps (max 152s). Exposed the BEFORE-LIVE gap: re-arm cohort needs real resting stops. Partly addressed (Loop 177 `_register_rearm_resting_stops`); coverage materially improved (11 resting stops placed today).
- **Capital deployment raised 6/29:** `DEPLOY_TARGET_PCT` 0.75→0.95 ($300k→$380k of a $400k DEPLOY_BASE), approved (`PROP-DEPLOY-TARGET-095`). Only lifts the re-arm admit ceiling (the winning path); 9:35 path unaffected. Per-position $25k / per-side $200k caps unchanged.
- **TODAY (6/30) — the HTB/SIM-borrow bug, found and FIXED.** The bot traded ZERO this morning. Root cause: the Hard-To-Borrow gate (`htb_filter.py`) trusts TradeStation's **SIM** `IsHardToBorrow` flag, which is **unreliable** — on 6/30 it returned `true` for ALL symbols (incl. AAPL/MSFT), so every candidate was excluded (it had armed 23 fills on 6/29 → the flag flips day-to-day = junk SIM data). Rhett pushed back correctly when I first over-stated it as "TradeStation fails" — it is the **bot trusting an unreliable SIM endpoint**, not live TS failing. **FIX (Loop 201, Rhett-approved, non-watched file):** made `htb_filter` SIM-aware — in SIM the borrow flags are **advisory (don't block)**; `HALTED` + `NO_QUOTE` still block; on the live API the original fail-safe gate is 100% intact. **Production-proven:** at the 10:35 re-arm the bot armed 16 ORB entries + placed 11 stops, 0 FAIL/CRIT. Bot is trading again.

## 6. THINGS PLANNING SHOULD KNOW IT GOT WRONG THIS WEEK (so you don't repeat)
- The "160 mass-reject" alarm was diagnosed (by you) as a Monday-open transient needing a code fix. It was actually **weekend re-arm submissions** (a separate known bug). I pushed back twice with broker truth before building the wrong fix.
- The HTB 0-trades was first framed as "TradeStation data anomaly." Rhett corrected it: TS live is fine; it's the **SIM endpoint flag + the bot trusting it.** Lesson now a standing rule: **verify every warning against live/broker truth before acting; Rhett's direct observation outranks a tidy explanation.**

## 7. OPEN DECISIONS / CARRIED ITEMS AWAITING RHETT (your queue to think about)
1. **PROP-REARM-TRADINGDAY-GATE** (approved, NOT yet deployed) — `orb_multiscan.py:261` gates re-arm on holidays only, not `is_regular_trading_day()`, so it submits orders on **weekends**. Deploy after close (WATCHED file).
2. **Restore live risk guards BEFORE any live use:** `DAILY_MAX_LOSS` ($2k daily stop) and the 5% account-DD kill are **DISABLED in SIM** for data collection. Must be restored + a real-time intraday clamp added before live. (`PROP-DEPLOY-TARGET-400K` real-time available-BP gate + sector/correlation cap also required before live.)
3. **Advisor per-symbol-P&L prompt leak** — per-symbol P&L must NEVER feed the advisor (strategy, not symbols). Audit the advisor prompt.
4. **Pre-open GO/NO-GO gate arming** — flip `SAFE_MODE_ENFORCE` to give the gate teeth (currently shadow); wants ~3-5 clean shadow mornings first.
5. **9:30 AM open-window loop-stall** — recurring main-loop freeze >4 min at the open (self-recovers). Fix = non-blocking open-window processing / open-time watchdog (WATCHED `bot_loop`/`orb_runner` → needs a proposal). Ties to the clean-day count.
6. **Clean-day test bar** — need 5 clean days on the post-6/19 config before Phase 4 scale. **OPEN QUESTION (Rhett, 6/25): does a kill-stop day count toward the 5?** Currently `consecutive_clean=0` (honest: 6/26 loop-stall broke a 3-day run).
7. **Post-test exit gauntlet (PROP-CONFIRM-KEYED-EXIT)** — GATED, DO NOT BUILD yet. Key exit aggressiveness on confirmation state; 3-sided net-of-cost + N≥30 + must-not-cut-winners. Superseded in part by the $500-cap finding.
8. **Re-arm vs 9:35 expectancy** — track both ORB paths; REVISIT at N≥30/path. First read: re-arm winning, 9:35 losing.

## 8. STANDING RULES (apply to every plan you write)
- **Preserve the one-way valve** — advisor never writes bot config; bot never executes free-text; never loosen the typed-schema gate in `advisor_filter_engine.py`. Legal control types are a FIXED list (see CLAUDE.md); anything else is silently ignored.
- **WATCHED trading files — never auto-edit mid-session or without Rhett's go:** `risk_config.py, bot_loop.py, exit_bot_v2.py, candle_close_exit.py, advisor_filter_engine.py, symbol_universe.py, orb_runner.py, orb_multiscan.py, short_bot.py, mover_scanner.py`. Changes go through a proposal under `outputs/proposals/` + explicit approval in `config/manual_approvals.yaml`. (`htb_filter.py` and most monitoring/dashboard files are NON-watched.)
- **VERIFY BEFORE YOU STATE** — never present a guess as fact; verify load-bearing claims against live data / real code / broker truth first, or label them "unverified."
- **Evidence hierarchy:** BROKER_TRUTH > BROKER_EXPORT > LOCAL_RECONSTRUCTION > BOT_LOG_CONTEXT > ADVISORY_RESEARCH. Cite the highest available; label reconstructions as such.
- **Symbol-agnostic logic** — no hardcoded AAPL/TSLA branches; watchlists are config data, not code.
- **Warning-triage protocol** — every warning: read+verify vs live truth → classify (false / real-non-watched / real-WATCHED / ambiguous) → fix-safe or ESCALATE-gated → LOG to SESSION_LOG. A warning is not automatically a fix.
- **Token discipline** — TradeStation access tokens last ~20 min and are reused (refresh only inside a 60s buffer). Never refresh per call/cycle (can get the API key disabled).
- **Copiable handoffs** — when you hand work to me via Rhett, write it as a self-contained block (paths + enough detail to act cold). One question per turn to Rhett.

## 9. CURRENT STATE SNAPSHOT (verified live, 2026-06-30 ~11:20 AM ET)
- **Bot:** ALIVE (`run_bot` PID 6824), trading normally. Today: 16 ORB entries armed, 11 resting stops placed, **0 FAIL/CRIT**. HTB fix live + proven.
- **Live exit:** `candle_1.4atr_chandelier` + the $500 per-trade dollar cap. TW (Tape Watcher) is the live exit owner on re-arm fills.
- **Advisor control:** `NO_CONTROLS`, `SIM_ONLY`, `live_allowed=false`, valid to 2026-07-01 08:04 ET. (Generated 08:04 pre-market; noted an off-hours feed anomaly — benign.)
- **Health:** CSHV ~45 OK / few benign WARN / 0 FAIL. SAFE_MODE_ENFORCE = OFF (gate in shadow). No naked-position / order-reject / auth / crash-loop alerts.
- **Last loop:** Code Loop 201 (HTB fix). Coordination repo HEAD `cfafcfc`, in sync with origin.
- **H5/futures stack:** sidelined today (`H5_SIDELINED` ×30) — separate sub-project (Gao @MES on SIM1623889F), not the equity bot.

## 10. SUGGESTED FIRST MOVE FOR THE NEW PLANNING CHAT
Acknowledge you've read 1–9, then ask Rhett (one question) which thread to pick up: the carried queue in §7 (most pressing pre-live = #1 weekend re-arm gate + #2 restore risk guards), or a new direction. Have Rhett relay anything you need me (Claude Code) to read/paste/verify — I have the live files and broker truth.
