# EDGE_TUNES.md — canonical candidate-tune ledger (Planning Loop 118)

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
| TUNE-01 | Fade-vs-breakout split | selection | candidate | per-name mean-reversion + ownership-mix to choose fade vs breakout | data: institutional % | - | - | 2026-06-18 |
| TUNE-02 | RS-vs-market directional gate | direction | candidate | long only if name outperforms SPY/sector; residual-move dual use | data: RS (9:35 only today) | - | - | 2026-06-18 |
| TUNE-03 | RelVol threshold tuning | selection | implemented | in-play gate ON, day-RelVol>=1.5 | - | - | - | 2026-06-18 |
| TUNE-07 | Candidate-pool discipline (top-20) | selection | candidate | test top-20 vs wider pools | - | - | - | 2026-06-18 |
| TUNE-08 | Opening-range window (5 vs 15/30m) | timing | candidate (low-pri) | test 5-min OR vs 15/30-min | - | - | - | 2026-06-18 |
| TUNE-09 | Afternoon re-arm windows | timing | tested-inconclusive | per-window net expectancy (9:35 lost / re-arm won, N=2) | - | - | - | 2026-06-18 |
| TUNE-10 | Earned-loosening exit redesign | exit | shadow-active | V7 pre-registered, LOCKED until V0 gate | gating: live-exit instrumentation | PROP-EXIT-FALSE-STOPOUT | V7 | 2026-06-18 |
| TUNE-11 | Cancel resting stop on confirm | exit | folded into TUNE-10 | folded into TUNE-10 (confirm-swap = V2) | - | PROP-EXIT-FALSE-STOPOUT | V2_CONFIRM | 2026-06-18 |
| TUNE-12 | Stop-distance tuning (0.15 vs 1.0 ATR) | exit | shadow-active | V1 wide-init in harness | gating: V0 gate | PROP-EXIT-FALSE-STOPOUT | V1_WIDE | 2026-06-18 |
| TUNE-19 | VWAP-trailing exit | exit | candidate | V4, deferred | data: VWAP not logged | PROP-EXIT-FALSE-STOPOUT | V4_VWAP | 2026-06-18 |
| TUNE-08b | Two-adverse-closes exit | exit | shadow-active | V8 pre-registered, locked | gating: V0 gate | PROP-EXIT-FALSE-STOPOUT | V8 | 2026-06-18 |
| TUNE-13 | Entry collar width (5 vs 25-50bps) | execution | candidate | missed-runners vs slippage | - | - | - | 2026-06-18 |
| TUNE-21 | Fast-alpha / micro-pullback entry | execution | candidate (info-only) | micro-pullback entry after breakout | - | - | - | 2026-06-18 |
| TUNE-14 | Re-entry discipline (cap vs fresh-breakout gate) | reentry | shadow-active | R0-R3 tested in-sample, all perm-p insignificant (N=2) | - | PROP-REENTRY-DRAG | reentry | 2026-06-18 |
| TUNE-15 | VWAP-confirmation filter | selection | candidate | require VWAP-side confirmation on entry | data: vwap_status not wired | - | - | 2026-06-18 |
| TUNE-16 | Catalyst-quality filter | selection | candidate | gate on catalyst quality | needs news classifier + source | - | - | 2026-06-18 |
| TUNE-18 | Breakout-kinetics confirmation | selection | candidate | confirm on breakout velocity/acceleration | needs velocity/accel logged | - | - | 2026-06-18 |
| TUNE-23 | Opening-range decisiveness filter | selection | candidate | strong body% / close near extreme | - | - | - | 2026-06-18 |
| TUNE-20 | VIX-regime conditioning | regime | candidate | pre-register ONE hypothesis | data: VIX term structure | - | - | 2026-06-18 |
| TUNE-17 | Cost-aware capital rotation | capital | parked | premature until capital binding proven | - | - | - | 2026-06-18 |
| TUNE-24 | Volatility-scaled / constant-risk sizing | sizing | candidate | equal $-risk per trade; no new data | - | - | - | 2026-06-18 |
| TUNE-04 | Move-band tuning (2-9%) | universe | candidate | tune entry move-band (2-9%) | - | - | - | 2026-06-18 |
| TUNE-05 | Dollar-volume floor ($20M/20d) | universe | candidate | tune dollar-volume floor ($20M/20d) | - | - | - | 2026-06-18 |
| TUNE-06 | Universe expansion beyond S&P 500 | universe | parked (conditional) | expand universe beyond S&P 500 | low-float mostly HTB | - | - | 2026-06-18 |
| GUARD-HTB | Hard-to-borrow exclusion | guardrail | implemented | exclude hard-to-borrow names from shorts | - | - | - | 2026-06-18 |
| GUARD-MARGIN | Per-symbol marginability | guardrail | shadow-active | per-symbol marginability (before-live gate) | TS API exposes no per-symbol margin | - | - | 2026-06-18 |
| GUARD-NOMART | No-martingale | guardrail | implemented | never average down a loser | - | - | - | 2026-06-18 |
| STRAT-C1 | Intraday PBD pairs/relative-value | strategy | parked | intraday pairs/relative-value | HTB-conflicted, gated behind base ORB | - | - | 2026-06-18 |
| STRAT-C2 | Noise-Area intraday index momentum | strategy | parked | noise-area intraday index momentum | - | - | - | 2026-06-18 |
| E1 | OpenBB read-only research-data layer | enabler | parked | read-only research-data layer | pilot before depending; audit free-vs-paid + latency | - | - | 2026-06-18 |
