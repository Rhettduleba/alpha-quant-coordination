# PROP-UNCONFIRMED-TIMESTOP-30M-2026-07-01 — 30-min time-stop on UNCONFIRMED trades only

**Status:** APPROVED by Rhett 2026-07-01 ("i want you to implement the 30 minute exit on all unconfirmed now"). DEPLOYED (Loop 220). SIM-only. Reversible instantly.

## Change
Two new constants in `risk_config.py` (WATCHED):
- `UNCONFIRMED_TIME_STOP_MIN = 30`
- `UNCONFIRMED_TIME_STOP_ENABLED = True`

New pre-check in `exit_bot_v2.py` (WATCHED), per open position, each cycle:
if the position is **still UNCONFIRMED** (favorable excursion has NEVER crossed +0.15×ATR, per the deployed
`candle_close_exit.chandelier_decision` confirm math — single-sourced, not re-implemented) **AND** ≥30 minutes have
elapsed since the **broker entry fill** (harvested from the `/orders` scan `exit_bot_v2` already runs: most-recent
FILLED `BUY`/`SELLSHORT` per symbol → restart-safe, broker truth), then flatten via the proven `flatten_symbol()`
with reason `TIME_EXIT_30M_UNCONFIRMED (age=Nm, unconfirmed)`.

## Guarantees (structural, regression-locked by REG-29)
- **Confirmed positions are UNTOUCHED** — they keep the 1.4×ATR chandelier + post-confirm candle-close + resting $-cap. The gate is `not _conf` from the deployed decision fn; REG-29 proves both sides (long+short) spare confirmed / leash unconfirmed.
- **Fires for EVERY open position, including Tape-Watcher-owned** — evaluated BEFORE the TW single-owner lease skip, so the rule can't be silently bypassed on TW-live days. No double-exit possible: `flatten_symbol` re-reads live qty and no-ops on flat.
- **Fail-safe** — unknown/missing entry time → never fires; any error in the block is caught and falls through to normal exit handling.
- **Does NOT burn a stop-out slot** — reason says `TIME_EXIT`, not `*STOP*`, so it doesn't count toward the per-symbol 2-stops/day breaker (a flat-and-move-on is not a protective stop-out). `record_realized_pl` still feeds the single-trade loss breaker.
- **Legacy percent-trail mode unaffected** — gated on `EXIT_MODE_CANDLE_CLOSE`.

## Evidence (verified study + 5-agent adversarial verification, 2026-07-01)
`strategy-research/l1_unconfirmed_leash.py` on 6/18–6/26 (N=138 round-trips, 39 unconfirmed, broker-truth nets):
- **30-min leash Δnet +$5,386** = bleed saved $5,836 + giveback −$450 (identity `Δnet = bleed + giveback`, reproduced to the cent).
- Cuts exactly **2** unconfirmed winners (CME +$55, MPWR +$156) — the ENTIRE unconfirmed-winner population.
- **Spares late-confirming winners structurally**: 59% of confirmed winners confirm after 30 min (median 38 min); the rule re-checks confirm state at the stop minute, not at entry ($5,944 of winner P&L protected vs an entry-time-only leash).
- **Generalizes to the live re-arm path**: 24/39 unconfirmed are re-arm, carrying 68% (+$3,688) of the benefit across ~15 names.
- Honest caveats stated to Rhett before his go: IN-SAMPLE, re-arm N=24 (<30 bar), only 1 unconfirmed winner on the re-arm path; sub-10-min variants are blind-window-inflated (30-min is the tightest defensible). Rhett chose to deploy now on SIM to gather live forward data rather than shadow first.

## Consumers swept (config-change rule)
- `exit_bot_v2.py` (the firer) · `exit_instrumentation.py` (+`entry_time`/`minutes_in_trade` fields in exit_decisions.jsonl)
- `validation/exit_reason_codes.py` (+`EXIT_TIME_STOP_UNCONFIRMED` code + TIME_EXIT/TIME_STOP rules + self-test 14/14)
- `strategy-research/system_facts.py` → SYSTEM_FACTS.md EXIT row (regenerated, L47) · advisor dashboard `system_validation_page.py` (+status line)
- `regression_suite.py` REG-29 (wiring + confirm-gate lock) — suite 27 pass / 0 FAIL
- `run_bot.py`/`bot_loop.py` confirmed NON-consumers (grep) → run_bot behavior unchanged; `exit_bot_v2` is a fresh subprocess each cycle → loads without a run_bot restart (proven: fresh process reads 30/True).

## Acceptance / owner tracking (daily EOD)
- Every `TIME_EXIT_30M_UNCONFIRMED` fire audited in the EOD debrief (classifier code `EXIT_TIME_STOP_UNCONFIRMED`; exit_decisions.jsonl carries entry_time + minutes_in_trade).
- Track: bleed saved vs winners cut vs giveback on live forward days; compare against the study's 27:1 save-to-cut ratio.
- PULL (set `UNCONFIRMED_TIME_STOP_ENABLED=False`) if it cuts confirmed winners (should be impossible — REG-29), or if forward data shows the unconfirmed-winner rate materially above the in-sample ~5%.

## Out of scope
Live blockers B3/B5/B2 stay SHADOW. 9:35 gate (PROP-935-GATE) unchanged. $500 cap + chandelier + candle-close unchanged.
