# ALPHA QUANT — STATE OF RECORD
**The single source of truth for the Alpha Quant project.**

- **Version:** 1.7
- **Created:** 2026-05-18
- **Owner:** Rhett Duleba
- **Maintained by:** Planning chat (Claude, browser) for decisions/standards; Claude Code for verified system state.
- **Location:** workspace root — `…\Trade station Main\ALPHA_QUANT_STATE.md`

> **This document supersedes** all prior knowledge-base versions and the project's prior handoff documents — specifically, the files moved to `Archive/` (the freeze-fix handoff, the Handoff 003 response, the VPS ramp-up handoff, the prior master `CLAUDE_CODE_HANDOFF.md`, and the ramp-up bundle). Earlier "numbered handoffs" referenced in conversation mostly lived only in the planning-chat session and were never separate files on disk. When anything here conflicts with another document, **this document wins** — except where the actual code/files contradict it, in which case the files win and this document gets corrected.

---

## CHANGELOG
*(Newest first. Every material change gets one dated line. This is how a reader sees what moved since they last read the doc.)*

- **2026-05-19 — v1.7** — Live-state update from Claude Code (verified at ~05:55 ET 2026-05-19). (a) Overnight freeze event: PID 5468 froze at 2026-05-18 17:34 ET (Heartbeat stale 184s), watchdog auto-restarted as PID 2360 at 17:35 ET. Since PID 5468 was launched at 16:07 ET — before the fixed `run_bot.py`'s 16:42 mtime — this is consistent with PID 5468 running OLD pre-freeze-fix code. **PID 2360 is the first bot instance likely to have the freeze fix loaded; today's 8 AM PRE_MARKET advisor slot is the definitive deployment test.** (b) Current `advisor_control_latest.json` is still the 2026-05-18 16:33 EOD file — contains `BLOCK_ENTRIES_AFTER_TIME: 11:00:00`, will be in force from market open until overwritten by today's 8 AM run. The v1.6 prompt edit's effect first visible at that 8 AM run.
- **2026-05-18 — v1.6** — **Afternoon block: prompt nudge removed.** Owner approval received (post-Handoff 009 Phase 1; chose "remove" over roadmap #10's "replace with `REQUIRE_MIN_SCORE_DURING_WINDOW`"). Claude Code edited `ai-trading-strategy-agent/src/advisor/prompt_builder.py` — deleted 4 lines (the two "Consider BLOCK_ENTRIES_AFTER_TIME" prompt bullets at former lines 61-64, plus their stale-statistic preambles that the Phase 1 journal contradicted). The `BLOCK_ENTRIES_AFTER_TIME` control type **remains in the AVAILABLE CONTROL TYPES vocabulary** (architecture unchanged; advisor *could* still emit it via independent reasoning, but the prompt push is gone). §4 afternoon-block bullet updated. **Behavior change first visible at PRE_MARKET advisor run 8:00 ET 2026-05-19** — current `advisor_control_latest.json` from 16:33 today still contains the block until overwritten. Memory-reinforcement risk flagged for follow-up if 8 AM run still emits the block from inertia.
- **2026-05-18 — v1.5** — Claude Code §1.4 + §4 update (verified-state ownership per §10), from Handoff 009 Phase 1 journal analysis. §1.4 now leads with the journal-verified 540-trade baseline (57.2% WR, $69.66 avg P&L); the prior "~4,274 trades / 60.6% WR" baseline is preserved as unreconciled because its source can't be found in any file. §4 afternoon-block bullet updated with verified source: `prompt_builder.py:60-67` hardcoded "STANDING RULES FROM HISTORICAL ANALYSIS" text — the unverified "ChatGPT-era test artifact" characterization is removed. Three hardcoded prompt statistics (10-11 AM = 73.7% WR; 11-12 AM = 36.6% WR; 25,520 all-time trades) are contradicted by the journal — see §1.4. Phase 2 of the afternoon-block work is planning-chat owned and pending.
- **2026-05-18 — v1.4** — §10 wording corrected (caught by Claude Code, rule 6): the coordination repo holds the coordination *documents* (State of Record + C1 + README), not "this file and nothing else." Also recorded: the repo's local working tree lives outside OneDrive (`C:\repos\alpha-quant-coordination\`) to avoid OneDrive/git lock conflicts.
- **2026-05-18 — v1.3** — (a) Removed the §2.5 note about `ALPHA_QUANT_HANDOFF.md`'s stale "12:30" — Claude Code corrected that source file, so the note is resolved. (b) §7 now carries a prominent **NOT FIT FOR USE** warning on the C1 statistical thresholds: Claude Code's critique is correct — §3.1's 100-trade minimum is statistically incompatible with §3.2's +2pp effect-size bar (2pp is inside the noise band of a 100-trade sample). C1 §3 needs a structural rewrite and the §1.4 baseline needs verification before C1 can evaluate anything, including roadmap item #3. This is logged honestly: the planning chat initially answered the C1 critique with a label change rather than engaging it; that was a dodge, now corrected.
- **2026-05-18 — v1.2** — Two corrections caught by Claude Code's Handoff 006 Response review: (a) the §0 "supersedes (001–005)" phrasing referenced numbered handoffs that were never separate files on disk — reworded to name the actual archived files; (b) §7 referenced `AQ_EVALUATION_STANDARDS_C1.md` as "archived" but that file was never installed in the workspace — it exists only as a planning-chat draft. §7 reworded to treat C1 as a companion file to be installed alongside this one. Both were planning-chat rule-1 violations (asserting unverified file state); both fixed.
- **2026-05-18 — v1.1** — Corrections from Claude Code Handoff 006 Response (verified against files): MIDDAY advisor slot is **12:00–12:25 ET**, not 12:30 (`run_bot.py:32`) — corrected in §1/§2.5, removed from §9 open questions. `anthropic` package confirmed installed on the VPS (v0.101.0) — §4 risk downgraded. Coordination-repo workflow added to §10. Note: `ALPHA_QUANT_HANDOFF.md` §4 still carries the stale "12:30" and must be fixed at source.
- **2026-05-18 — v1.0** — Initial consolidated State of Record. Built from: original `HANDOFF.md` (2026-05-12), the ChatGPT-era handoffs (filtered), the freeze-fix documents, Handoff 003 verification, `CLAUDE_CODE_HANDOFF.md`, and the full ramp-up bundle (three `CLAUDE.md` files, `ALPHA_QUANT_HANDOFF.md`, `V1_SCOPE.md`, the 19-question discussion log). Three stale knowledge-base facts corrected (advisor model, hostname, universe count). Roadmap fairly represented as reasoned decisions. Two open verification items logged (§9).

---

## HOW THIS DOCUMENT WORKS

- **§1 Identity & verified state** — what Alpha Quant is, every fact source-cited.
- **§2 Architecture** — the two-pipeline structure, the one-way channel.
- **§3 Safety guardrails** — load-bearing, do-not-touch.
- **§4 Current operational state** — what's deployed, what's pending right now.
- **§5 The roadmap** — the 16 items, their reasoning, and their evaluation status.
- **§6 Rejected / superseded** — things decided against, so they're not revisited.
- **§7 Evaluation standards (C1)** — the bar every change must clear.
- **§8 Operating rules & roles** — how the project stays coordinated.
- **§9 Open questions** — unresolved items needing verification.
- **§10 Roles & sync protocol** — who does what, how this file is kept current.

**Sync model:** Claude Code reads and updates this file on disk. The planning chat receives it by paste at the start of a session. The changelog tells any reader what moved. One file, one source of truth.

---

## 1. IDENTITY & VERIFIED STATE

Alpha Quant ("AQ") is a SIM-only automated intraday equity day-trading system on TradeStation. It runs on a Windows VPS. Two cooperating Python applications under one OneDrive-synced workspace.

### 1.1 Verified facts (source-cited)
| Fact | Value | Source |
|---|---|---|
| Account | `SIM1623888M` — SIM only | `bot_loop.py` SIM safety stop |
| Advisor model | `claude-sonnet-4-6` | `claude_client.py:14` |
| VPS hostname | `win-fibssoqki7k` | `machine_guard.py:35-37` |
| Symbol universe | 34 total — 31 stocks + 3 ETFs | `symbol_universe.py:25-42` |
| Daily max loss | `$10,000` | `risk_config.py:1` |
| Max open positions | `4` | `bot_loop.py:78` |
| Max position size | `25%` of equity | `bot_loop.py:35` |
| Max total exposure | `$100,000` | `bot_loop.py:79` |
| Max sector positions | `2` | `symbol_universe.py:74` |
| Min price filter | `$20` | `bot_loop.py` |
| Min net change filter | `0.25%` | `bot_loop.py` |
| Min volume filter | `500,000` | `bot_loop.py` |
| Max spread filter | `$0.25` | `bot_loop.py` |
| Re-entry cooldown | `900s` (15 min) | `bot_loop.py` `REENTRY_COOLDOWN_SECONDS` |
| Limit offset | `$0.10` flat (roadmap #5 changes this) | `submit_limit_order.py` |
| Staged ramp | Stage 3–4 of 6 | `ALPHA_QUANT_HANDOFF.md` |

> **Corrections from prior knowledge base (were stale):** advisor model was wrongly recorded as "Opus 4.5" (truth: Sonnet 4.6); hostname was wrongly "win-b3-8-us-east-va-1" (truth: win-fibssoqki7k); universe was wrongly "37" (truth: 34).

### 1.2 Entry logic (two stages)
**Stage 1 — hard filters** (pass/fail eligibility): price ≥ $20, net change ≥ 0.25%, volume ≥ 500k, spread ≤ $0.25.
**Stage 2 — composite score** (ranks eligible survivors), from `entry_signals.py`:
- Momentum 35% (net change %, max at ±2.5%)
- Volume 25% (vs floor, max at 3× floor)
- Spread quality 20% (tighter better, max at $0 spread)
- Price action 20% (above open AND prev close for longs; reversed for shorts)
- Composite must be ≥ 0.40. Bot picks highest composite among eligible.
- **Currently missing from the score:** earnings risk, news, sector relative strength, options activity, macro context (roadmap #13–15 address this).

### 1.3 Exit logic (`exit_bot_v2.py:14-34`)
| Mechanism | Trigger | Effect |
|---|---|---|
| Hard stop | 0.50% loss from avg | Exit immediately |
| Tier 1 trailing | +0.20% profit | Trail 0.08% from high |
| Tier 2 trailing | +0.75% profit | Trail 0.05% |
| Tier 3 trailing | +1.50% profit | Trail 0.03% |
| Breakeven lock | +0.40% profit | Stop locked at avg + 0.05% |

> **Flagged:** These values are tight by day-trading convention (0.5% hard stop vs textbook 1–2%; all trailing tiers active within 1.5% profit). Roadmap #2 is a discussion of whether to loosen. Do not change without explicit decision.

### 1.4 Backtest baseline

**Verified 2026-05-18 by Claude Code from `trade_journal.csv` (BOT_LOG_CONTEXT tier, FIFO entry/exit pairing):** n = **540 closed trades**, 2026-04-16 → 2026-05-18 (~22 trading days). **57.2% WR, $69.66 avg P&L/trade, $37,614 total P&L.** Longs (n=407): 64.1% WR, ~$135 avg. Shorts (n=133): 38.3% WR, ~−$80 avg.

**Hour-of-day pattern (combined, entry-time ET, journal assumed ET — see §9):** Strongest hour = **15 ET (72.1% WR / $302 avg / n=43)**, driven by longs. Weakest = **11 ET (48.7% WR / −$34 avg / n=78)** — but the weakness is shorts-only at 11 AM (21.1% WR, n=19); longs at 11 AM are profitable (57.6% WR / +$17 avg / n=59). 09 ET is also weak (52.9% combined / −$28 avg) driven by shorts.

**Unreconciled prior claims** (preserved per rule 6 — sources not found in any file I read):
- "~4,274 closed trades / 60.6% WR / 1.30 PF / $35.85 avg" baseline carried in earlier State of Record versions. Origin unknown; may refer to a longer historical dataset not in the current journal (per-machine archives `trade_journal-BOOK-*-*.csv` were not loaded and merged).
- `ai-trading-strategy-agent/src/advisor/prompt_builder.py:60-67` hardcodes "25,520 trades / 57.0% WR / $42.02 avg" plus "10-11 AM = 73.7% WR / 11-12 AM = 36.6% WR" as **"STANDING RULES FROM HISTORICAL ANALYSIS (always apply these)"** prompt text. The 73.7% and 36.6% figures specifically are contradicted by the journal-verified numbers above (10 AM = 60.2%, 11 AM = 48.7%). The 25,520 trade-count source is unknown.

Short win rate ~38% (this journal) is roughly in line with retail day-trading literature (~32%) and is not a system failure — but the magnitude of short losses concentrated at 9 AM (−$140 avg, n=38) and 11 AM (−$193 avg, n=19) is a structural issue worth flagging.

Full Phase 1 evidence and methodology: Handoff 009 Phase 1 response.

---

## 2. ARCHITECTURE

### 2.1 The two applications
**`tradestation-bot/`** — "The Bot." Polls TradeStation REST API ~every 5–15s during market hours, scans the universe, scores candidates, places SIM limit orders, manages exits, enforces hard risk limits. Intentionally narrow, deterministic, reviewable. Entry point `run_bot.py` → `bot_loop.py`.

**`ai-trading-strategy-agent/`** — "The Advisor." Contains **two separate pipelines** — do not conflate them:
1. **Operational control loop** (`run_advisor.py`) — calls Claude, writes the typed control file the bot obeys. Scheduled 3×/day.
2. **V1 research pipeline** (`src/main.py`) — daily reports, operator dashboard, weekly review, proposals, experiment registry. Human-review surface. **Does not feed the bot.**

### 2.2 The architectural rule (do not violate)
> *"The agent should know a lot. The bot should do only what has been proven."*

The advisor never reaches into the bot. It writes one JSON file. The bot reads it with paranoid validation. There is no other channel.

### 2.3 The one-way channel
The advisor writes `advisor_control_latest.json` to `ai-trading-strategy-agent/outputs/advisor_guidance/`. The bot's `advisor_filter_engine.py` re-reads it every loop and **rejects** it if: file missing, bad JSON, `environment != "SIM_ONLY"`, `live_allowed != false`, `free_text_control_allowed != false`, or past `expiration_time` (24h TTL). **On rejection the bot defaults to ALLOW** — a missing/stale advisor must never lock the bot out. Every decision is logged to `advisor_filter_engine.log`.

### 2.4 The control vocabulary (the bot's hard contract)
Only these control types are legal. Anything else is silently ignored. Extending this list requires a coordinated change in BOTH `control_writer.py` (advisor) and `advisor_filter_engine.py` (bot).

`BLOCK_ALL_NEW_ENTRIES` · `BLOCK_SYMBOL` · `ALLOW_SYMBOLS_ONLY` · `BLOCK_ENTRIES_AFTER_TIME` · `REDUCE_MAX_POSITIONS` · `SET_MAX_POSITION_PCT` · `REQUIRE_MIN_NET_CHANGE_PCT` · `REQUIRE_MIN_NEG_CHANGE_PCT` · `NO_CONTROLS`

### 2.5 Advisor schedule
Three slots, verified verbatim from `run_bot.py:30-34`:
- **PRE_MARKET** — 8:00–8:25 ET
- **MIDDAY** — 12:00–12:25 ET
- **EOD** — 16:30–16:55 ET (`--relearn` removed; pattern analysis is RAM-intensive on VPS)

Plus a drawdown trigger at −$2,000 (30-min cooldown). Earnings-freshness check re-runs the advisor with refresh flags if the earnings calendar is >7 days old, before PRE_MARKET.

### 2.6 Advisor 9-step pipeline (operational loop)
1. Collect data (quotes, sector ETFs, account, journal, session reports, earnings, news)
2. Historical pattern analysis → `learned_patterns.json` (RAM-heavy; cached)
3. Load advisor memory (`advisor_memory.json`)
4. Analyze → regime label, P&L, rolling averages
5. Build prompt
6. Call Claude (Sonnet 4.6); on API failure writes `NO_CONTROLS` fallback
7. Parse strict JSON
8. Write control file + human guidance file
9. Update memory

---

## 3. SAFETY GUARDRAILS — DO NOT TOUCH WITHOUT EXPLICIT APPROVAL

1. **SIM safety stop** — `bot_loop.py` ~line 164: refuses to trade if account ID doesn't start with `SIM`.
2. **Machine guard** — `machine_guard.py:35-37`: `ALLOWED_HOSTNAMES = {"win-fibssoqki7k"}`. Adding a hostname = letting another machine run the live bot.
3. **Control-file validation** — `advisor_filter_engine.py`: the rejection rules in §2.3. Default-to-ALLOW on rejection is intentional.
4. **Control vocabulary** — §2.4. Typed list; coordinated change required to extend.
5. **Hard risk floors** — `risk_config.py` and `bot_loop.py` defaults (§1.1). Advisor can REDUCE via controls; cannot RAISE.
6. **TradeStation token reuse** — `ts_client.py`. Tokens last ~20 min; refresh only within a ~60s buffer. Never refresh per call/cycle — excessive refresh can disable the API key.
7. **Per-trade exit logic** — `exit_bot_v2.py:14-34`. Roadmap #2 may revisit; no change without explicit decision.
8. **Advisor control safety fields** — `control_writer.py` stamps `environment: "SIM_ONLY"`, `live_allowed: false`, `free_text_control_allowed: false`, 24h TTL on every run.
9. **Advisory-only boundary** — the V1 research pipeline never writes into `tradestation-bot/`. Strategy/risk changes go through proposal artifacts + explicit approval in `config/manual_approvals.yaml`.

---

## 4. CURRENT OPERATIONAL STATE
*(As of 2026-05-18. Re-verify when starting work — files change.)*

- **Freeze fix:** Code-complete in `run_bot.py` (Option B — heartbeat-while-waiting + orphan reaper). Compile-checked. **Deployment AMBIGUOUS** — VPS bot last restarted 16:07 ET, ~35 min before the fixed code's local mtime. Verify at next 8 AM advisor slot: no "Heartbeat stale" entry, `advisor_running.json` appears briefly, PID stable. If not deployed, restart bot on VPS (market closed, with approval).
- **Afternoon block — REMOVED 2026-05-18 (owner-approved prompt edit):** The two prompt bullets steering the advisor to emit `BLOCK_ENTRIES_AFTER_TIME` were deleted from `ai-trading-strategy-agent/src/advisor/prompt_builder.py` (formerly lines 61-64, the "10-11 AM strongest" / "11-12 AM worst" window claims + their "Consider BLOCK_ENTRIES_AFTER_TIME" suggestions). The control type is still in the AVAILABLE CONTROL TYPES vocabulary at line 52, so architecture is unchanged — Claude could still emit the control via independent reasoning, but the heavy prompt nudge is gone. **Behavior change first visible at the PRE_MARKET advisor run, 8:00 ET 2026-05-19.** The current `advisor_control_latest.json` (written 2026-05-18 16:33 ET, TTL 24h) still contains the block and will until overwritten. **Watch tomorrow's 8 AM run** — if it still emits `BLOCK_ENTRIES_AFTER_TIME` despite the prompt fix, the cause is likely memory-reinforcement (`advisor_memory.json` records prior runs); a separate memory edit would be the follow-up. Owner chose "remove" over roadmap #10's "replace with `REQUIRE_MIN_SCORE_DURING_WINDOW`." See §1.4 for the verified hour-by-hour data that justified removal.
- **`requirements.txt` gap:** The `anthropic` package is NOT listed in `ai-trading-strategy-agent/requirements.txt`. Verified 2026-05-18: it IS installed on the VPS (v0.101.0, Python 3.14), so the silent-failure risk is not currently live — but a fresh machine would hit it. `anthropic` should still be added to `requirements.txt`. Also: the `pydantic==2.11.3` pin fails on Python 3.14 and should be loosened.
- **Bot live state at last check (verified 2026-05-19 ~05:55 ET):** PID **2360**, alive, loop 2581, last_seen 05:51 ET. PID 5468 (manual restart at 16:07 ET 2026-05-18) froze at 17:34 ET with Heartbeat stale 184s — watchdog auto-restarted to PID 2360 at 17:35 ET. PID 2360 has been stable through the night (12+ hours, no heartbeat-stale events). The 17:34 freeze is consistent with PID 5468 running OLD pre-fix code (its 16:07 launch predates the fixed run_bot.py's 16:42 mtime). PID 2360 is the first bot launched after the fix file landed locally — today's 8 AM advisor run is the test.

---

## 5. THE ROADMAP

The 16 items below came from a substantive 19-question working session (`Alpha_Quant_Discussion_Log.docx`, 2026-05-18) — real reasoning, two-sided answers, owner pushback. They are **reasoned decisions**, not a casual brainstorm. However, "decided in discussion" is not the same as "passed evaluation" — items that change live trading behavior or risk still go through §7 (C1) before they ship.

**Profitability goal (context for the whole roadmap):** the project's single solid goal is consistent profitability, targeted at $500+/day. Per Claude's own Q5 analysis this is ~0.5% daily / ~250% annualized — ambitious; most retail day traders aim for 0.1–0.3% daily. Achievable only if data, execution, and reliability improvements land.

| # | Item | Type | Evaluation status |
|---|---|---|---|
| 1 | 8 AM freeze fix | Done | Code-complete; deployment verification pending (§4) |
| 2 | Review per-trade stop-loss values | Discussion | Discussion only — no code. Tight values may be right or may cap winners |
| 3 | Tiered daily-loss guard ($200/$400/$500) | Code | **MUST clear C1 before shipping — see flag below** |
| 4 | 5 safety features (circuit breaker, VIX gate, halt/SSR check, latency monitor, heartbeat self-test) | Code | Bundled — should be split and evaluated individually |
| 5 | Percentage-based limit offset + 3-retry cap | Code | Touches order placement — high-care; needs test plan |
| 6 | Marginable-only filter | Research+Code | Low risk; research the TS API field first |
| 7 | Decision/fill latency instrumentation | Code | Measurement only — low risk, good to do |
| 8 | Smart sleep schedule (bot idle off-hours) | Code | Low risk; may also help freeze pattern |
| 9 | Reorganize operator dashboard | Code | UX; 6-section structure already sketched |
| 10 | Replace `BLOCK_ENTRIES_AFTER_TIME` with `REQUIRE_MIN_SCORE_DURING_WINDOW` | Code | Right permanent fix for the afternoon block |
| 11 | Add `SET_SECTOR_CAP` control type | Code | Additive control type; ceiling 4/sector |
| 12 | Score-weighted sizing (≥0.70→25%, 0.55–0.70→15%, 0.40–0.55→10%) | Code | Concept sound; thresholds need backtest validation |
| 13 | Tier 1 data: FRED macro + VIX + treasury yields into advisor prompt | Code | High-leverage; aligns with "pre-trade intelligence" |
| 14 | Tier 2 data: FMP earnings calendar | Setup+Code | Half-wired; needs API key |
| 15 | Full data acquisition plan document (Tier 1–5) | Document | Planning doc |
| 16 | WebSocket streaming for sub-second execution | Deferred | ~1-month project; deferred until basics solid |

### 5.1 FLAG — Item #3 (tiered daily-loss guard)
The Q5 design hard-stops the day at **−$500 of loss**. The profit goal is **+$500/day**. These are the same magnitude. A 60%-win-rate strategy with normal variance will have ordinary losing days that hit −$500 through noise alone — and an over-tight loss cap mechanically prevents the recovery days needed to hit the profit goal. **Before item #3 ships, someone must compute, from real historical daily P&L: how many normal trading days would a −$500 hard stop have killed?** If few, proceed. If many, the threshold strangles the system and must be raised. This is exactly what §7 exists to catch.

### 5.2 Suggested sequencing
Discussion-session order was 1→4 first (freeze, stop review, daily guard, safety features). Adjusted recommendation: deploy #1, do #7/#8 (low-risk), resolve #10 + Handoff 004 (afternoon block), and put #3 through §7 before it ships. #13–15 (data) are the highest-leverage engine improvements and align with the "pre-trade intelligence" direction.

---

## 6. REJECTED / SUPERSEDED (do not revisit without new evidence)

- **Same-symbol cooldown** — 7-day broker-confirmed replay showed best variant cost −$218 P&L. Do not implement.
- **Old flat exit thresholds** (0.50/0.25/1.00 etc.) — superseded by tiered T1/T2/T3.
- **Old 7-symbol / "40-symbol" universe counts** — actual is 34.
- **Advisor as Opus 4.5** — actual is Sonnet 4.6.
- **TSLA-specific After-11 filter** — generalized into `BLOCK_ENTRIES_AFTER_TIME`; that in turn being replaced by #10.
- **Cutting shorts entirely** — considered (Q1); rejected. Shorts are structurally harder (~32% win rate is normal for retail day trading) but cutting them halves opportunity. Keep, with short-specific criteria and bearish-regime gating.
- **Market orders instead of limit orders** — considered (Q9a); rejected. Limits save ~$2–5k/month in spread; asymmetric risk favors limits.
- **More frequent advisor calls right now** — considered (Q14); rejected for now. Better data per call beats more calls. Revisit (maybe 5/day) only after data sources improve and only if measured to help.
- **Deep learning / LSTM models in execution** — research-only, deferred indefinitely.
- **ChatGPT in the workflow** — the old ChatGPT project is closed. Not reintroduced.

---

## 7. EVALUATION STANDARDS (C1)

> **⚠ STATUS: C1 §3 (statistical thresholds) is NOT FIT FOR USE pending a structural rewrite.** Claude Code identified a real, structural flaw: the §3.1 minimum sample size (100 trades) is statistically incompatible with the §3.2 effect-size bar (+2pp win rate). A 2pp win-rate move sits *inside* the ~5pp noise band of a 100-trade sample — so C1 as written would certify random noise as a real edge, the exact opposite of its purpose. Three further issues: the §1.4 baseline is unverified (and every threshold depends on it); the §3.3 walk-forward "2/3 of windows" rule doesn't specify a window count; the §3.4 multiple-comparisons treatment is not a correct Bonferroni formulation. **Until §3 is rewritten and the baseline verified, no change may be "evaluated against C1" — this explicitly includes roadmap item #3 (the tiered daily-loss guard).** The rewrite is the next C1 work item. The summary below and the companion document remain useful for the *non-statistical* parts (evidence tiers as a concept, evidence hierarchy, one-change-at-a-time, rollback discipline).

Every change that could affect trading performance must clear this bar before it ships. Bug fixes and pure measurement (e.g., #7) are exempt.

- **Evidence tier required:** A (backtest-supported, effect holds across ≥3 periods), B (live-data-supported, ≥30 days / ≥300 trades), or C (theory-supported — limited, must be A/B-tested, max 2 active at once). Anything below these is not actionable.
- **Effect size to call something "meaningful":** +2pp win rate, OR +0.10 profit factor, OR +$5/trade, OR −15% drawdown without harming the others.
- **Sample minimums:** ≥100 trades per condition for a claim; ≥50 for a sub-tier (flagged preliminary); ≥30 per symbol.
- **Anti-overfitting:** walk-forward validation; reserve the most recent 20% of data for final validation only; complexity penalty on every new parameter.
- **Post-implementation:** every change has a pre-defined evaluation window (default 30 trading days / 300 trades) and explicit keep/rollback thresholds. Rollback is the system working, not a failure.
- **Evidence hierarchy** (project-wide): `BROKER_TRUTH > BROKER_EXPORT > LOCAL_RECONSTRUCTION > BOT_LOG_CONTEXT > ADVISORY_RESEARCH`. Conclusions cite the highest available source; lower-tier conclusions are labeled as such, never presented as broker-confirmed.
- **One change at a time.** Bundled changes can't be evaluated or rolled back individually (this is why #4's "5 features" must be split).

Full proposal format and detailed thresholds live in the companion document `AQ_EVALUATION_STANDARDS_C1.md` (installed alongside this file in the coordination repo and the workspace root). The summary above is the working subset; the companion file is authoritative for the detail.

---

## 8. OPERATING RULES

Rules for every session — planning chat and Claude Code alike. Each is tied to a mechanism, not just an intention.

1. **Did I read it, or did I invent it?** No fact about system state is asserted unless just read from a file, or explicitly marked "unverified." (The "Roman" confabulation — an invented project-owner name — is the cautionary example.)
2. **State confidence explicitly.** Every recommendation is *verified* (read the files), *reasoned* (logic from verified facts), or *unverified* (from a handoff not yet confirmed).
3. **One source of truth.** A decision is not real until it's in this document. Not in a memory file, not in a handoff alone.
4. **Push back before executing, not after.** If a requested action looks like a mistake, say so first. The owner can override — but hears the objection.
5. **No bundling.** One change at a time, evaluated on its own.
6. **Surface disagreement, don't silently resolve it.** If Claude Code's verified view conflicts with this document, or two sources conflict, that goes to the owner as an explicit "these disagree" — neither side silently picks.
7. **Planning chat: no flattery, no agreeable hedging.** Weak ideas are named as weak. "I don't know" is said when true.
8. **Planning chat: don't pretend to be synced when not.** If a question depends on context not in hand, say what's missing rather than generating over the gap.
9. **Claude Code: every report ends with "what I did NOT verify."** An explicit section. This is the mechanism that catches confabulation.
10. **Claude Code: no process actions without explicit approval.** Restarting the bot, killing PIDs, deploying code, editing risk config — propose, get approval, then act.

**Enforcement:** every Claude Code handoff opens by restating rules 1, 2, 9, 10. The owner's check on the planning chat (rules 7–8): if pushback ever feels performative rather than substantive, call it out.

---

## 9. OPEN QUESTIONS — NEED VERIFICATION

1. **Item #3 loss-guard calibration.** §5.1 — needs the historical loss-day distribution computed before the tiered guard ships.
2. **Afternoon-block statistic.** The advisor cites "11 AM hour = 45.4% win rate / −$13.98 avg." Never independently verified against the trade journal. Handoff 004's analysis settles this.
3. **Freeze-fix deployment status.** §4 — ambiguous until verified at the next 8 AM advisor slot.

*Resolved in v1.1: MIDDAY advisor slot confirmed 12:00–12:25 ET (`run_bot.py:32`).*

---

## 10. ROLES & SYNC PROTOCOL

**Roles:**
- **Planning chat (Claude, browser)** — strategy, filtering, decisions, evaluation standards. Owns §5–§9 (decisions/standards). The brain.
- **Claude Code** — implementation; verified system state. Owns §1, §4 (verified facts). The hands.
- **Browser-Claude (UX consultant)** — narrow dashboard visual/UX help only. Has its own scoped handoff.
- **ChatGPT** — not in the loop.

**How this file stays current:**
- This file lives at the workspace root on the VPS. Claude Code reads it at the start of every session and updates it on disk when verified state changes.
- **Coordination repo (the shared channel):** a small dedicated git repo — `alpha-quant-coordination` — holds only the coordination documents (`ALPHA_QUANT_STATE.md`, `AQ_EVALUATION_STANDARDS_C1.md`, and a `README.md`) — no AlphaQuant code, no secrets, ever. Its local working tree lives outside the OneDrive workspace (at `C:\repos\alpha-quant-coordination\`) to avoid OneDrive/git file-lock conflicts. Claude Code pushes the current State of Record and C1 to that repo whenever they update. The planning chat reads the State of Record directly from the repo's raw file URL — no manual relay in the Claude-Code → planning-chat direction.
- **Planning-chat → Claude-Code direction:** the planning chat produces an updated whole file; it is moved intact (committed to the repo, or handed to Claude Code to commit). The file is moved whole, never summarized or excerpted.
- Every change adds a dated CHANGELOG line at the top and bumps the version.
- Neither role silently overwrites the other's sections. A conflict between Claude Code's verified state and a planning-chat decision is surfaced to the owner (rule 6).
- Superseded documents are archived, not left in the read path.

---

**END — ALPHA QUANT STATE OF RECORD v1.4**
