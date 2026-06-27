# EXECUTION-COST / IMPLEMENTATION-SHORTFALL LEDGER  (read-only, broker-truth; n=285 entries)
_All references REAL/broker-logged (coverage ~99-100%) except SPREAD = UNATTRIBUTED (no quote-at-fill).
_Adverse = positive cost. Net of cost is the only real number._

## 1) HEADLINE
- **Entry implementation shortfall (decision->fill): avg 0.82 bps (0.03 cents/share), median 0.86 bps.**
- Commission: avg 1.49 bps/trade · Fees: avg 0.0 bps/trade · total commission+fees = $669.85 ($669.85 comm + $0.00 fee).
- **Realized GROSS per trade: avg -1.06 bps** (post-slippage, pre-commission) · **NET per trade: avg -4.04 bps** (post-commission).
- **COST WATERFALL (avg bps/trade):** signal/paper gross ~-0.24 -> minus entry slippage 0.82 -> realized gross -1.06 -> minus commission+fees 1.49 -> NET -4.04.
  _(paper gross = realized gross + entry slippage added back; EXIT-side slippage not isolated -- see caveats.)_
- **TOTALS (285 round-trips):** realized gross **$187** -> NET **$-1,153** (commission+fees $670 entry-leg); total entry slippage $431.

## 2) COST DECOMPOSITION (avg per trade)
| component | avg cents/share | avg bps | real vs approx |
|---|---|---|---|
| delay (decision->arrival) | 0.06 | 2.52 | REAL |
| execution (arrival->fill) | -0.03 | -1.7 | REAL (incl. spread, unisolated) |
| = entry IS (decision->fill) | 0.03 | 0.82 | REAL |
| collar/limit slip (intended->fill) | 0.03 | 0.82 | REAL |
| commission | -- | 1.49 | REAL (broker) |
| fees | -- | 0.0 | REAL (broker) |
| spread (half-spread isolated) | -- | -- | **UNATTRIBUTED** (no quote-at-fill logged) |
- avg delay time decision->fill: -0.04s (median 0.0s)

## 3) SPLITS — where is cost worst?
## SPLIT by entry path (9:35 vs re-arm)
| group | n | avg IS bps | avg comm bps | avg net$ | avg gross$ |
|---|---|---|---|---|---|
| 9:35 | 111 | 0.85 | 1.12 | -33.32 | -29.12 |
| re-arm | 174 | 0.79 | 1.72 | 14.63 | 19.65 |

## SPLIT by side
| group | n | avg IS bps | avg comm bps | avg net$ | avg gross$ |
|---|---|---|---|---|---|
| long | 131 | 0.76 | 1.61 | -17.08 | -11.69 |
| short | 154 | 0.86 | 1.39 | 7.04 | 11.16 |

## SPLIT by session segment
| group | n | avg IS bps | avg comm bps | avg net$ | avg gross$ |
|---|---|---|---|---|---|
| close | 25 | 0.74 | 2.1 | 32.45 | 37.19 |
| midday | 147 | 0.8 | 1.68 | 18.1 | 23.22 |
| open | 113 | 0.85 | 1.11 | -40.92 | -36.78 |

## SPLIT by win/loss
| group | n | avg IS bps | avg comm bps |
|---|---|---|---|
| loss | 123 | 1.24 | 1.65 |
| win | 162 | 0.5 | 1.36 |

## 4) TIE-OUT vs daily_review / eod_debrief (broker-actual cost)
- **Full broker-CSV commission+fees (every filled order, entry+exit): $1,339.71**
- eod_debrief / daily_review round_trips commission+fees (both legs): $1,339.73
- **TIE-OUT: MATCH (within $1)**
- This ledger's ENTRY-leg-only commission+fees = $669.85 (~half of the full $1,339.71, as expected -- the other half is exit-leg commission).

## CAVEATS / fidelity
- decision/arrival/intended/fill + commission/fees = REAL broker-logged. Spread = UNATTRIBUTED.
- EXIT-side implementation shortfall is NOT computed (exit 'decision' price = the chandelier/candle trigger level, not cleanly logged) — the headline cost is ENTRY IS + commission/fees; exit slippage is a known unmeasured residual sitting inside realized gross.
- 0/285 entries did not join a round-trip (gross/net N/A for those).