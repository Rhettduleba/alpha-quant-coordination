# EDGE_TUNES.md — canonical candidate-tune ledger (Planning Loop 118; curated Loop 120)

> **CANDIDATE LEDGER — most entries are UNVALIDATED. This is NOT a verdict and NOT a roadmap.**
> It is the durable master list of candidate edge tunes / guardrails / strategies and *where each one
> sits in the pipeline*. It **LINKS** the existing logs, it does not duplicate them:
> - tests run → `research/trial_registry.csv` (joined per tune by `trial_match` against source_ref/variant_name/linked_report)
> - changes made → `strategy_changes/strategy_change_log.jsonl` (joined per tune by `hypothesis_id`)
>
> **Planning is the content gatekeeper.** Status/links are updated as trials and changes accrue.
> Rendered read-only at the dashboard `/edge-tunes` (with the joined evidence). Committed here +
> mirrored to the coordination repo. Logged as a strategy change of type `logging_only`.
>
> STATUS vocabulary: `candidate · shadow-active · tested-inconclusive · tested-promising ·
> tested-failed · implemented · guardrail · parked · rejected` (an entry may annotate in parentheses).

<!-- The table below is the machine-readable source the /edge-tunes page parses. One row per tune.
     Columns (do NOT reorder): id | name | category | status | one_line | dependencies | hypothesis_id | trial_match | last_updated
     hypothesis_id / trial_match are LINK KEYS only (no copied results). "-" = none. -->

| id | name | category | status | one_line | dependencies | hypothesis_id | trial_match | last_updated |
|----|------|----------|--------|----------|--------------|---------------|-------------|--------------|
| TUNE-01 | Fade-vs-breakout split | selection | candidate | per-name mean-reversion + ownership-mix to choose fade vs breakout; +multi-horizon breakout_R/fade_R logger @15/60m/EOD (pure logging); +auction-imbalance MR as large-cap/extended-from-VWAP fade evidence; +test SKIP/veto direction (NET avoided-losers minus missed-winners) | data: institutional % | - | - | 2026-06-19 |
| TUNE-02 | RS-vs-market directional gate | direction | candidate | long only if name outperforms SPY/sector; residual-move dual use; +RS-confirms-vs-conflicts validation; +sector-ETF leg; +residual_return_z (move minus market/sector-beta-expected); +ETF-flow spillover (stock-specific vs basket); +skip-direction test | data: RS (9:35 only today) | - | - | 2026-06-19 |
| TUNE-03 | RelVol threshold tuning | selection | implemented | in-play gate ON, day-RelVol>=1.5; +volume_surprise_z + volume_persistence_score vs per-minute expected-volume curve (beats simple RelVol AFTER cost?); +skip-direction test | - | - | - | 2026-06-19 |
| TUNE-07 | Candidate-pool discipline (top-20) | selection | candidate | test top-20 vs wider pools | - | - | - | 2026-06-18 |
| TUNE-08 | Opening-range window (5 vs 15/30m) | timing | candidate (low-pri) | test 5-min OR vs 15/30-min | - | - | - | 2026-06-18 |
| TUNE-09 | Afternoon re-arm windows | timing | tested-inconclusive | per-window net expectancy (9:35 lost / re-arm won, N=2); +9:35 worst-spread-at-open per-window net exp (candidate cause of live 9:35 underperformance) | - | - | - | 2026-06-19 |
| TUNE-10 | Earned-loosening exit redesign | exit | shadow-active | NOTE: the LIVE exit (2026-06-19) is the simpler 1.4xATR chandelier (see TUNE-12); V7 earned-loosening (floor-with-room) stays in SHADOW to test if it beats the deployed chandelier; results pending OOS-forward N>=30 + multiple-testing correction (NOT the partial preview); +vol-state-adaptive / time-stop / OR-invalidation harness variants; +alpha-decay-by-horizon diagnostic | gating: live-exit instrumentation (now passing) | PROP-EXIT-FALSE-STOPOUT | V7 | 2026-06-19 |
| TUNE-11 | Cancel resting stop on confirm | exit | folded into TUNE-10 | folded into TUNE-10 (confirm-swap = V2) | - | PROP-EXIT-FALSE-STOPOUT | V2_CONFIRM | 2026-06-18 |
| TUNE-12 | Stop-distance tuning (0.15 vs 1.0 ATR) | exit | implemented | **LIVE 2026-06-19** -- DEPLOYED as candle_1.4atr_chandelier (1.4xATR ratchet floor replaces the 0.15 phase-1); KILL-GATED 5d (AQ-20260619-ORB-EXIT-REENTRY-001; reverts to V0 if it doesn't beat V0-shadow / single < -$800 / day < -$2,000); V1 wide-init shadow continues for attribution | live; reversible ORB_EXIT_MODE=candle_close | PROP-EXIT-FALSE-STOPOUT | V1_WIDE | 2026-06-19 |
| TUNE-19 | VWAP-trailing exit | exit | shadow-active | V4 in harness; results pending after-close authoritative --score + OOS-forward N>=30 | data: VWAP not logged | PROP-EXIT-FALSE-STOPOUT | V4_VWAP | 2026-06-19 |
| TUNE-08b | Two-adverse-closes exit | exit | shadow-active | V8 in harness; results pending OOS-forward N>=30 + multiple-testing correction | gating: V0 gate (now passing) | PROP-EXIT-FALSE-STOPOUT | V8 | 2026-06-19 |
| TUNE-13 | Entry collar width (5 vs 25-50bps) | execution | candidate | missed-runners vs slippage; +adverse-fill measure (fill-prob vs post-fill MFE/MAE); +9:35-entry spread-cost (vs later windows); +cost-by-session-segment (open/midday/close); +fill-prob-by-order-type (have via broker truth) | - | - | - | 2026-06-19 |
| TUNE-21 | Fast-alpha / micro-pullback entry | execution | candidate (info-only) | micro-pullback entry after breakout | - | - | - | 2026-06-18 |
| TUNE-14 | Re-entry discipline (cap vs fresh-breakout gate) | reentry | implemented | **LIVE 2026-06-19** -- DEPLOYED as cap 1/name/day (R1, ORB_MAX_ENTRIES_PER_NAME=1); KILL-GATED 5d (AQ-20260619-ORB-EXIT-REENTRY-001); R0-R3 shadow continues for attribution | live; reversible ORB_MAX_ENTRIES_PER_NAME=0 | PROP-REENTRY-DRAG | reentry | 2026-06-19 |
| TUNE-15 | VWAP-confirmation filter | selection | candidate | require VWAP-side confirmation on entry; +skip-direction test | data: vwap_status not wired | - | - | 2026-06-19 |
| TUNE-16 | Catalyst-quality filter | selection | candidate | gate on catalyst quality; +news-integrity sanitization guard (prompt-injection/homoglyph/entity) as PREREQUISITE; +earnings-day regime (tag earnings-day; continuation-vs-fade single split; ties deferred earnings-veto); +options-flow-direction (future, data-dependent); +skip-direction test | needs news classifier + source | - | - | 2026-06-19 |
| TUNE-18 | Breakout-kinetics confirmation | selection | candidate | confirm on breakout velocity/acceleration | needs velocity/accel logged | - | - | 2026-06-18 |
| TUNE-23 | Opening-range decisiveness filter | selection | candidate | strong body% / close near extreme | - | - | - | 2026-06-18 |
| TUNE-20 | VIX-regime conditioning | regime | candidate | pre-register ONE hypothesis; +overnight ES/NQ futures gap as day-level risk-on/off context (ONE primitive, NOT a 16-instrument basket) | data: VIX term structure | - | - | 2026-06-19 |
| TUNE-17 | Cost-aware capital rotation | capital | parked | premature until capital binding proven; +EOD-flatten TIMING sweep (3:30/3:45/3:50/3:55/3:58 by slippage/MFE-given-up/MAE-avoided/net + by-unrealized-R: losers earlier, winners later); +model EOD fills realistically (not close print); +index-rebalance-day awareness (huge MOC-flow days) | - | - | - | 2026-06-19 |
| TUNE-24 | Volatility-scaled / constant-risk sizing | sizing | candidate | equal $-risk per trade; no new data; +CONDITIONAL nonlinear-size guardrail (gate order size by %-of-volume IF conviction/>$20k sizing ever pursued; ties parked tranching) -- NOT active at current size | - | - | - | 2026-06-19 |
| TUNE-04 | Move-band tuning (2-9%) | universe | candidate | tune entry move-band (2-9%); +LULD halt-risk guardrail (skip extreme short-window-return / recent-halt names) -- LOW value, minor guard | - | - | - | 2026-06-19 |
| TUNE-05 | Dollar-volume floor ($20M/20d) | universe | candidate | tune dollar-volume floor ($20M/20d) | - | - | - | 2026-06-18 |
| TUNE-06 | Universe expansion beyond S&P 500 | universe | parked (conditional) | expand universe beyond S&P 500 | low-float mostly HTB | - | - | 2026-06-18 |
| TUNE-25 | Two-bar opening confirmation | timing | candidate | require the 2nd 5-min bar to confirm direction before entry; test ORB5 vs ORB10 vs ORB5+2nd-bar-confirm vs 2nd-bar-conflict-skip as a FALSE-BREAKOUT filter (cuts 9:35 whipsaws upstream of the exit defect) | own 5-min bars; missed-runner tradeoff (test vs immediate-fill, like TUNE-21) | H-TWO-BAR-OPEN-CONFIRMATION | two-bar | 2026-06-19 |
| TUNE-26 | SSR / Rule 201 short-execution | execution | candidate | log each short candidate's SSR state (down >10% from prior close = alt-uptick restriction); TAG short rejects by reason (SSR/HTB/locate/margin); measure short fill-quality & P&L by SSR state -- diagnostic (may resolve the open short-reject thread) + possible edge (skip SSR-restricted shorts) | return-from-prior-close (have it) | H-SSR-SHORT-EXECUTION | ssr | 2026-06-19 |
| GUARD-HTB | Hard-to-borrow exclusion | guardrail | implemented | exclude hard-to-borrow names from shorts | - | - | - | 2026-06-18 |
| GUARD-MARGIN | Per-symbol marginability | guardrail | shadow-active | per-symbol marginability (before-live gate) | TS API exposes no per-symbol margin | - | - | 2026-06-18 |
| GUARD-NOMART | No-martingale | guardrail | implemented | never average down a loser | - | - | - | 2026-06-18 |
| STRAT-C1 | Intraday PBD pairs/relative-value | strategy | parked | intraday pairs/relative-value | HTB-conflicted, gated behind base ORB | - | - | 2026-06-18 |
| STRAT-C2 | Noise-Area intraday index momentum | strategy | parked | noise-area intraday index momentum; +index OPEN-REVERSAL sub-variant (overnight->first-30m reversal; pre-register ONE direction); +0DTE/gamma-regime conditioning (IF sleeve revived; ONE direction; real signal needs paid options data) | - | - | - | 2026-06-19 |
| E1 | OpenBB read-only research-data layer | enabler | parked | read-only research-data layer; UNBLOCKS the Tier-1 data ladder (see INFRA NOTE) | pilot before depending; audit free-vs-paid + latency | - | - | 2026-06-19 |

## DO-NOT-BUILD (weeded composites — never re-propose)

Recorded so they are never re-proposed (weeded across all 10 research passes):

- opening-regime classifier · gap-regime 6-label · liquidity-event-state 10-label · no-trade bundled classifier · factor-intraday-timing · displayed-market-quality score · event-risk kill switch (duplicates SAFE_MODE) · strategy router · direction×magnitude classifier · volatility-state 6-label classifier · decision-gate 25-input · "Research OS" pipeline
- ALSO weeded: time-of-day-memory (Heston; weak/arbed) · benchmark-flow-pressure standalone (re-skins TUNE-03/15) · nonlinear-size-impact as ACTIVE (conditional-only, see TUNE-24) · order-flow/queue-imbalance (needs Level II we lack — parked) · listing-venue (negligible at our horizon)

REASON: multi-feature composite scorers that re-skin existing primitives = the data-mining / overfit trap. Test the FEEDING PRIMITIVES individually through the gauntlet, not the bundle.

## VALIDATION HARDENING (gauntlet upgrades — NOT edge tunes)

Candidate upgrades to `aq_validation` / the gauntlet (Passes 7/9/10), important now that ~26 tunes create real multiple-testing risk:

- Positive/negative controls (random side / ticker / shuffled-labels → NO edge; known effect → shows up)
- Probability calibration (score → realized win-rate by bucket; Brier/ECE; no score-sizing until calibrated)
- Multiple-testing correction across the variant family (FDR / Bonferroni; disclose #tested/#accepted) — directly relevant to the 8-variant V1 p=0.014 preview
- Deflated / probabilistic Sharpe (not raw Sharpe; non-normal intraday returns + many trials)
- PBO (probability of backtest overfitting; IS-vs-OOS rank)
- Reality-Check / SPA (White/Hansen data-snooping vs no-trade / ORB-baseline)
- Model Confidence Set (keep statistically-tied variants, pick the simplest)
- Simplicity penalty (prefer the simpler variant unless the complex one materially beats OOS)
- Fragility curves (perturb each param ±10%; require ROBUST, not FRAGILE)

NOTE: deflated-Sharpe / PBO come from the Bailey/Lopez de Prado ecosystem we flagged for cost-optimism — the METHODS are sound (overfit deflation, orthogonal to cost); keep our net-of-cost + broker-truth insistence ON TOP. Mild: add disproof-condition + min-sample + decision-rule fields to entries; adopt stricter min-edge thresholds in spirit (N>=100 single-stock / >=50 index, PF>1.15, not-one-ticker, not-one-month, walk-forward).

## INFRA NOTE — Tier-1 data ladder (ties to E1)

Tier-1 "must-have-next" data = NBBO/spread · trade-count · avg-trade-size · sector-ETF · SPY/QQQ context · earnings-calendar · halt/LULD · SSR-flag · listing-exchange. This is the FIRST data upgrade and it UNBLOCKS the data-dependent folds: **TUNE-13** (spread/exec), **TUNE-02** (sector leg), **TUNE-16** (earnings), **TUNE-26** (SSR). Tie to the **E1**/OpenBB enabler entry.
