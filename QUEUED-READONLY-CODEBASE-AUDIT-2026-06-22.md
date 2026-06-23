# QUEUED — READ-ONLY CODEBASE AUDIT (Planning handoff 2026-06-22 ~6:20 PM)
**STATUS: GATED / NOT STARTED. Do NOT run until Planning releases it.**

## RELEASE TRIGGER (ALL must hold; verified NOT met as of 2026-06-23 AM)
1. The Loop-123 exit/re-entry forward test has RESOLVED (5-day kill-window passed → change PROMOTED or REVERTED).
2. We are BETWEEN experiments (no live-path change under measurement).
- **Current state (why it's idle):** 6/22 was NON-CLEAN (OOM) → consecutive_clean=0; 6/23 is the day-1 attempt. Forward-test window 0/5, IN-PROGRESS → trigger NOT met. Planning will release.

## PURPOSE
Senior-engineer READ-ONLY audit that SURFACES risk (safety/lifecycle gaps + silent-coupling). It does NOT
change anything and does NOT refactor for scale. Replaces the generic "rebuild for millions / clean-arch
refactor" framing (wrong target for a single-box ~50-trade/day SIM bot; would break the freeze + money path).

## HARD CONSTRAINTS
- READ-ONLY. No edits/refactors/rewrites/new structure. Touch watched strategy files (risk_config, bot_loop,
  exit_bot_v2, candle_close_exit, advisor_filter_engine, symbol_universe, orb_runner, orb_multiscan,
  short_bot) only to READ. No scale/throughput optimization. Output = findings report routed to Planning;
  propose nothing for live deploy; recommend NO watched-file change as an action (write obvious fixes up as
  findings, do not implement).

## SCOPE (ranked by why we care)
1. **SYNTHETIC-EXIT SAFETY (highest):** trace entry → arm → fill → synthetic exit (exit_bot_v2) → EOD
   flatten. Enumerate every path where an OPEN position becomes UNMANAGED (exit_bot_v2 dies/stalls/loses
   tracking) and what protects it then. Map the cancel-on-disconnect / emergency-exit gap.
2. **SILENT-COUPLING HOTSPOTS:** every place ONE knob/constant/state drives TWO behaviors (known example:
   EXIT_SL_FRAC drove sizing AND stop). List each + the two behaviors coupled.
3. **LIFECYCLE / ORDER-PATH FRAGILITY:** duplicate/fragile submit/partial-fill/reject/restart/reconcile
   logic. Confirm known scars closed + no siblings: deploy-book terminal-order phantom, heartbeat-path
   orphan, restart resetting reliability_state, double-logged journal rows. Flag naked-retry /
   non-idempotent submit / state-reset-on-restart.
4. **BROKER-TRUTH INTEGRITY:** any surface deriving P&L/positions/exposure from something other than the
   canonical source (round_trips_net / broker_orders_unified) — per-symbol-collapse / gross-vs-net class.
5. **LATENT PERF DEBT — NON-TRADING ONLY:** 140MB trade_journal.csv (_exit_reasons ~3.5s/call), dashboard
   chart-init load, synchronous git/IO on hot paths. Report; do NOT touch the trading loop.

## OUTPUT (one artifact)
`reports/codebase_audit_READONLY_<date>.md`, each finding: id · area(1-5) · what · why-it-matters ·
RISK-TO-REAL-MONEY(high/med/low) · is-it-a-watched-file · suggested-follow-up (as a PROPOSAL, not an action)
· evidence(file:line/log). Map each high/med finding to the STPA hazard register (H1-H14) + Phase-3/4 safety
bucket (EXTEND, don't spawn a parallel list). Rank by risk-to-real-money; lead with synthetic-exit/lifecycle.

## ACCEPTANCE
- Zero files modified (git clean except the report); zero watched files touched.
- Every finding cites evidence (RULE #0).
- Routed to Planning; nothing queued for live deploy; no watched-file change recommended-as-action.
- High/med findings cross-referenced to hazard register + Phase-3/4 bucket.

## NOTE
Between-experiments before-live hardening. Feeds the Phase-3/4 safety + governance work
(emergency-exit/cancel-on-disconnect, idempotency, restart-in-SAFE_MODE, live-BP sizing, hazard-to-test
matrix). Does not authorize any of them on its own.
