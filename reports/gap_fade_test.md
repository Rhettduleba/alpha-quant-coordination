# GAP-FADE TEST on the gated 9:35 trades (read-only, GROSS only, broker-truth gross)
_Gap = logged 9:35 scan price vs prior-session close (deterministic, no fetch). n=111 (9:35 equities); 52 have logged gaps (gate-era 6/15+)._

## 1) Of the gated 9:35 LOSERS
- losers: **52** of 111 (total loss $-9441).
- **gapped overnight (|gap|>=1%): 25 = 48%**
- **entered WITH the gap: 25 = 48%**
- early-noise-then-fade %: **DEFERRED** -- the 1-min-bar fetch throttles non-deterministically (classification flipped run-to-run); this run uses the DETERMINISTIC logged gap (price vs prior_close) and skips the bar-based early-shape. Intrabar fade read needs a reliable tick/bar source.

## 2) Gross by bucket (the pattern test)
| bucket | n | total gross | avg/trade | win% | PF |
|---|---|---|---|---|---|
| **gap-up & long** | 19 | -2188 | -115.1 | 47% | 0.31 |
| **gap-down & short** | 33 | -1134 | -34.4 | 55% | 0.7 |
| **other/unknown** | 59 | +89 | +1.5 | 54% | 1.04 |

## 2b) Gross by gap-class x side
| gap-class | side | n | total | avg/trade | win% | PF |
|---|---|---|---|---|---|---|
| gap-down | short | 33 | -1134 | -34.4 | 55% | 0.7 |
| gap-up | long | 19 | -2188 | -115.1 | 47% | 0.31 |
| unknown | long | 29 | +588 | +20.3 | 59% | 1.53 |
| unknown | short | 30 | -500 | -16.7 | 50% | 0.64 |

## 3) Cross-check: are the LONG losses the gap-up-and-went-long names?
- long trades: n=48, total $-1599, avg $-33.3, PF 0.62.
- long LOSERS: 22; of those **10 (45%) were GAP-UP** (entered long INTO a gap-up). Their gross: $-3158.
- ALL gap-up & long (win+lose): n=19, avg $-115.1/trade, win 47%, PF 0.31.

## SYNTHESIS
- The 9:35 GATE forces DIRECTION-MATCH (long needs up / short needs down) -> EVERY gated entry that gapped is BY CONSTRUCTION a WITH-gap entry. With-gap n=52 avg $-63.9/trade; AGAINST-gap n=0 (the gate structurally can't make these). So the gate MANDATES the with-gap pattern that loses -- it can't avoid it without changing the direction rule.
- gap-up&long (the worst bucket) is **76% the single MU 6/25 trade** ($-1668 of $-2188); EX-MU the bucket is only mildly negative. So the catastrophic read is one-trade (MU); the residual gap-fade drag is real but mild.
- **VERDICT: Rhett's gap-fade theory is DIRECTIONALLY SUPPORTED** (with-gap entries lose; the gate forces with-gap; long-into-gap-up is the worst + ~45% of long losers) **but MU-dominated** -- a hypothesis pointing the fix at gap-handling (don't chase gap-direction / fade large gaps), to OOS-test.

## CAVEATS
- COVERAGE: 52/111 classified (gate-era 6/15-6/26; pre-6/15 9:35 trades have NO logged candidate row -> no gap, excluded). The classified set is the gate-era population (the right one).
- gap-up&long is 76% one trade (MU) -> the bucket's PF is not robust.
- Early-shape (noise-then-fade) DEFERRED -- 1-min-bar fetch throttles non-deterministically.
- Gap = 9:35 price vs IMMEDIATE prior-session close (understates multi-day moves).
- In-sample, small N per bucket, GROSS only (no fees). HYPOTHESIS test, not a gate/strategy change.