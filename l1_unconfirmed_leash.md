# Lever 1 -- Unconfirmed-Trade Early-Invalidation Leash (READ-ONLY shadow sim)

_Generated 2026-07-01 19:17:18 | days: 2026-06-18, 2026-06-22, 2026-06-23, 2026-06-24, 2026-06-25, 2026-06-26_

**What L1 is:** apply a tight early-invalidation leash to UNCONFIRMED trades ONLY (favorable excursion never crossed +0.15xATR -> `confirmed` never True). Confirmed trades keep the deployed 1.4xATR chandelier, UNTOUCHED. By construction L1 cannot touch a confirmed winner; the only real risk is cutting an *unconfirmed* winner.

## Cohort

- Round-trips in sample: **138**
- Confirmed (untouched by L1): **70**
- Unconfirmed (L1 cohort): **39** (clean-fail 35 / poll-near-miss 4)
- Confirm-state NOT-AVAILABLE (occ>1 poll-ambiguity, never altered): **29** (of which occ-ambiguous 29)
- Days with deterministic pinned bars (C_ncloses eligible): **3** (pins are deterministic only for dates >= 2026-06-24)

## Variant ranking (by Δnet, net-of-cost, vs broker truth)

Δnet = Σ net_cf − Σ net_actual over the confirm=NO cohort. 3-sided: bleed-reduction (good) − winner-to-loser conversion (bad) − giveback (chandelier would've done better). N = confirm=NO trades the rule actually fired on.

| Variant | N fired | Δnet | bleed-reduction | winner->loser ($ / #) | giveback | confirmed altered |
|---|---:|---:|---:|---:|---:|---:|
| A_time_3m | 36 | $9,365.99 | $9,573.94 | $-207.95 / 2 | $-207.95 | 0 |
| A_time_5m | 36 | $8,841.48 | $9,072.43 | $-207.95 / 2 | $-230.95 | 0 |
| A_time_10m | 36 | $7,709.13 | $7,917.08 | $-207.95 / 2 | $-207.95 | 0 |
| A_time_15m | 36 | $7,027.28 | $7,235.23 | $-207.95 / 2 | $-207.95 | 0 |
| A_time_20m | 35 | $6,494.50 | $6,702.45 | $-207.95 / 2 | $-207.95 | 0 |
| A_time_30m | 33 | $5,385.98 | $5,835.55 | $-197.30 / 2 | $-449.57 | 0 |
| C_ncloses_2 ⚠N<30 | 26 | $4,872.34 | $5,649.75 | $-553.53 / 2 | $-777.41 | 0 |
| C_ncloses_3 ⚠N<30 | 26 | $3,703.65 | $4,554.93 | $-600.06 / 2 | $-851.28 | 0 |
| A_time_60m | 33 | $3,083.34 | $4,082.99 | $-342.80 / 2 | $-999.65 | 0 |
| A_time_45m | 33 | $2,930.70 | $4,022.75 | $-159.50 / 2 | $-1,092.05 | 0 |
| A_time_120m | 32 | $2,344.94 | $3,259.70 | $-430.63 / 2 | $-914.76 | 0 |
| A_time_90m | 32 | $1,596.62 | $2,915.54 | $-492.73 / 2 | $-1,318.92 | 0 |
| B_mae_0.5atr ⚠N<30 | 14 | $1,347.56 | $2,054.00 | $0.00 / 0 | $-706.44 | 0 |
| B_mae_0.75atr ⚠N<30 | 8 | $654.81 | $1,009.42 | $0.00 / 0 | $-354.61 | 0 |
| B_mae_1.0atr ⚠N<30 | 4 | $180.65 | $417.93 | $0.00 / 0 | $-237.28 | 0 |
| B_mae_1.25atr ⚠N<30 | 2 | $86.55 | $187.73 | $0.00 / 0 | $-101.18 | 0 |

## Segment split (confirm=NO: clean-fail vs poll-near-miss)

| Variant | clean-fail Δnet (n) | poll-near-miss Δnet (n) |
|---|---:|---:|
| A_time_3m | $8,253.14 (35) | $1,112.85 (4) |
| A_time_5m | $7,807.80 (35) | $1,033.68 (4) |
| A_time_10m | $6,751.13 (35) | $958.00 (4) |
| A_time_15m | $5,920.01 (35) | $1,107.27 (4) |
| A_time_20m | $5,507.52 (35) | $986.98 (4) |
| A_time_30m | $4,609.71 (35) | $776.27 (4) |
| C_ncloses_2 | $4,330.44 (24) | $541.90 (2) |
| C_ncloses_3 | $3,140.77 (24) | $562.88 (2) |
| A_time_60m | $2,432.91 (35) | $650.43 (4) |
| A_time_45m | $2,209.46 (35) | $721.24 (4) |
| A_time_120m | $1,799.21 (35) | $545.73 (4) |
| A_time_90m | $1,106.21 (35) | $490.41 (4) |
| B_mae_0.5atr | $1,183.97 (35) | $163.59 (4) |
| B_mae_0.75atr | $654.81 (35) | $0.00 (4) |
| B_mae_1.0atr | $180.65 (35) | $0.00 (4) |
| B_mae_1.25atr | $86.55 (35) | $0.00 (4) |

## Headline counterfactuals (MU / DELL / PENN, 6/25)

_Best time-variant: **A_time_3m** | Best MAE-variant: **B_mae_0.5atr**_

| Name | side | confirmed | actual net | best-time net_cf (fired) | best-MAE net_cf (fired) |
|---|---|---|---:|---:|---:|
| MU (2026-06-25) | long | False | $-1,670.30 | $-50.15 (Y) | $-643.85 (Y) |
| DELL (2026-06-25) | short | False | $-660.16 | $-245.53 (Y) | $-850.38 (Y) |
| PENN (2026-06-25) | long | False | $-463.23 | $-15.09 (Y) | $-398.55 (Y) |

_Sanity target: MU 6/25 (unconfirmed long, actual −$1,670) should die around −$300 to −$600 under a tight leash, not −$1,670._

## Controls & reconciliation

- **Unchanged-trade reconciliation to broker truth:** 102 unchanged nets checked against round_trips_net; mismatches: **0** (PASS).
- **MUST-NOT-CUT control:** confirmed/NA trades altered across all variants: **0** (PASS -- L1 touched 0 confirmed trades).

## Provenance map

- **Broker truth (actual net, entry/exit px, qty, commission, fee):** eod_debrief.round_trips_net (BROKER_EXPORT).
- **Confirm state, confirm time, ATR, confirm_level, polled price path (time + MAE leashes):** exit_decisions.jsonl polls (derived-from-polls).
- **N-adverse-closes (C_ncloses):** pinned 1-min bars outputs/validation/shadow_pin/{date}.json (derived-from-bars); NOT-AVAILABLE for dates < 2026-06-24.
- **occ>1 round-trips:** polled series cannot be split per occurrence -> confirm state NOT-AVAILABLE; these trades are counted but NEVER altered.
- No live API calls. No order placement. No live-path writes.

## VERDICT

The best variant by Δnet is **A_time_3m** (Δnet $9,365.99 over 39 unconfirmed trades, fired on 36). It reduces unconfirmed-loser bleed by $9,573.94 while converting 2 unconfirmed winner(s) to losers for $-207.95 and giving back $-207.95 vs the chandelier. MU 6/25 (the headline unconfirmed long) goes from $-1,670.30 actual to ~$-50.15 under A_time_3m / ~$-643.85 under B_mae_0.5atr (near the −$300..−$600 sanity band). Directionally, L1 DOES materially cut the unconfirmed bleed and the winner-conversion cost is small relative to the bleed saved -- it spares confirmed winners by construction (0 altered).
