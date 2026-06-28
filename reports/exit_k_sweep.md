# EXIT ATR-MULTIPLE (K) SWEEP 0.5->2.0 -- 1-min TW replay, READ-ONLY, GROSS
_One variable (K = chandelier+resting multiple); structure held (confirm @0.15xATR + candle-close trail). n=282 equities-ORB trades replayed; 0 skipped (no ATR/bars). 1-min fidelity. In-sample -> ranks candidates, does NOT promote a number._

## PROVENANCE OF K=1.4 (Step 0)
- **Hand-picked, NOT fit to our data.** Loop 121 (PROP-EXIT-CANDLE-1.4ATR, 2026-06-18): chosen to replace the 0.15xATR phase-1 + 1.0xATR catastrophe with 'a single WIDE 1.4xATR chandelier' to fix confirmed false-stop-outs (candle_close_exit.py:55-59). The tuning lineage (EDGE_TUNES TUNE-12) compared 0.15 vs 1.0; **1.4 itself was never grid-searched on our trades** -- inherited/hand-picked, same trusted-by-design pattern. THIS sweep is the first fit.

## THE SWEEP CURVE (the trade-off, not just the argmax)
| K | total gross | expectancy | win% | PF | avg win | avg loss | max loss | winners KILLED | catastrophes CAPPED |
|---|---|---|---|---|---|---|---|---|---|
| 0.5 | -4 | -0.0 | 64% | 1.00 | +135 | -237 | -721 | 32 | 25 |
| 0.6 | +541 | +1.9 | 67% | 1.02 | +133 | -268 | -888 | 22 | 19 |
| 0.7 | +4,974 | +17.6 | 72% | 1.23 | +131 | -269 | -1,019 | 10 | 15 |
| 0.8 | +5,382 | +19.1 | 73% | 1.25 | +129 | -275 | -898 | 7 | 9 |
| 0.9 | +5,750 | +20.4 | 73% | 1.28 | +129 | -279 | -1,000 | 5 | 6 |
| 1.0 | +7,494 | +26.6 | 74% | 1.38 | +128 | -271 | -1,115 | 2 | 5 |
| 1.1 | +7,784 | +27.6 | 75% | 1.40 | +128 | -271 | -1,229 | 1 | 5 |
| 1.2 | +8,133 | +28.8 | 75% | 1.43 | +128 | -271 | -1,344 | 0 | 4 |
| 1.3 | +7,766 | +27.5 | 75% | 1.40 | +128 | -276 | -1,458 | 0 | 4 |
| 1.4 **<-LIVE** | +7,488 | +26.6 | 75% | 1.38 | +128 | -280 | -1,572 | 0 | 3 |
| 1.5 | +7,220 | +25.6 | 75% | 1.36 | +128 | -284 | -1,687 | 0 | 3 |
| 1.6 | +8,177 | +29.0 | 75% | 1.43 | +128 | -270 | -1,290 | 0 | 3 |
| 1.8 | +7,871 | +27.9 | 75% | 1.41 | +128 | -274 | -1,342 | 0 | 2 |
| 2.0 | +7,698 | +27.3 | 75% | 1.40 | +128 | -277 | -1,499 | 0 | 0 |

## THE BIG FINDING -- it's the TIMING, not the multiple
- **Same structure + same K=1.4, but exited on 1-MIN bars instead of the bot's ~5-7min poll = $+7,488 gross. The bot's ACTUAL broker gross over these same 282 trades was $+461.** The ~$+7,027 gap is the EXECUTION-LAG cost (late exits + the re-arm 0%-resting-coverage gap), NOT the K multiple. (Replay is OPTIMISTIC -- fills exactly at the chandelier level / candle close, no exit slippage -- so this is an UPPER BOUND on recoverable $, but the direction is unambiguous.) The exit fix points at TIMING/COVERAGE (foundation-map #4/#8), not at re-tuning K.

## THE ANSWER (on K specifically)
- **K=1.4 is NOT the problem -- the multiple is fine.** At proper 1-min timing the whole range K>=1.0 is a FLAT plateau: totals $+7,220..$+8,177 (spread only $957 across K=1.0->2.0), expectancy ~$26-29/trade, win 75%, PF ~1.4. 1.4 sits comfortably in it, near-optimal.
- **The confident, directional finding: do NOT go tighter than ~1.0.** Below 1.0 winners get clipped fast -- K=0.5 kills 32 winners and collapses to $-4 (breakeven); K=0.7 still kills 10. The handoff's prior ('1.4 sits at the tight whipsaw edge') is NOT supported -- the whipsaw edge is below 1.0, and 1.4 is safely above it.
- **Do NOT promote the nominal argmax (K=1.6, +$690 over 1.4 = $+2.4/trade).** That edge is WITHIN the 1-min fidelity noise (the plateau is flat and max-loss is non-monotonic across 1.4/1.5/1.6 -- a tell of single-trade/intrabar noise). 1.0-2.0 are statistically indistinguishable at 1-min.

## MU / SINGLE-TRADE DOMINANCE (recurring trap)
- At K=1.4 the MU trades contribute $-1,395 (-19% of total). At best-balance K=1.6: $-399 (-5%).
- MU worst single-trade loss by K: K0.5=$-543, K1.0=$-1,115, K1.4=$-1,572, K2.0=$-577 -- shows whether tightening caps the MU-class catastrophe.

## FIDELITY + CAVEATS
- **1-MINUTE bars** (not tick). Stop level during bar t uses water through bar t-1 (no intrabar look-ahead); bar t's high/low tests it. Within a bar, high-vs-low print order is unresolved -> adjacent K differing by a hair are INDISTINGUISHABLE; rank by the curve shape, not a 1-cell win. TW live tick (proving Mon) would sharpen the close calls.
- **In-sample** (282 trades, post-5/26). This RANKS K for an OOS forward test; it does NOT promote a number. GROSS only (no fees). Replays the chandelier STRUCTURE only -- not a different exit family.
- Replay starts at the broker entry fill + ATR-as-of date; bars filtered to >= entry time. EOD flatten = last bar close. Skipped trades lacked ATR/bars (throttle or thin name).
- No orders, no watched file, no exit change. Freeze intact.