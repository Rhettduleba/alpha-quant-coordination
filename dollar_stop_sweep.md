# DOLLAR-CAP STOP SWEEP $100->$500 -- 1-min replay, READ-ONLY (Rhett 2026-06-30)
_One variable: the per-trade $ loss cap (resting stop = min(1.4xATR, $cap/qty)). MAE$-based replay on 1-min bars. n=320 equities-ORB round-trips post-5/26; 0 skipped (no bars). $500 = LIVE (== actual, since every trade already ran the $500 cap). In-sample -> RANKS, does not promote._

## PROVENANCE OF $500
- **Hand-picked, NOT swept.** Loop 187 (2026-06-30) enabled DOLLAR_STOP_CAP=$500 to bound per-trade loss after the 6/29 -$3,493 day; the LEVEL ($500) was a round number, never grid-searched. THIS is the first fit.

## THE SWEEP CURVE (the trade-off, not just the argmax)
| $ cap | NET total | GROSS total | expectancy | win% | PF | avg loss | max loss | trades hit cap | **winners KILLED** | losers capped |
|---|---|---|---|---|---|---|---|---|---|---|
| $100 | -18,645 | -17,087 | -58.3 | 21% | 0.26 | -100 | -211 | 215 | **116** | 99 |
| $200 | -19,521 | -17,962 | -61.0 | 38% | 0.42 | -168 | -242 | 133 | **64** | 69 |
| $300 | -15,153 | -13,595 | -47.4 | 48% | 0.55 | -200 | -507 | 73 | **31** | 42 |
| $400 | -11,015 | -9,456 | -34.4 | 52% | 0.65 | -208 | -507 | 43 | **16** | 27 |
| $500 **<-LIVE** | -4,726 | -3,167 | -14.8 | 56% | 0.83 | -193 | -527 | 20 | **4** | 16 |

**Baseline:** actual NET over the same 320 trades (live $500 cap) = $-3,469.98; 184 were winners.

## WINNERS THE TIGHTER CAPS WOULD HAVE KILLED (vs the live $500)
- **$400 cap:** kills 16 winners ($1,698 of real wins given up vs $500). Worst-hit: MSTR +$365(MAE $461), ACN +$364(MAE $421), MSTR +$255(MAE $423), UPST +$219(MAE $436), LRCX +$144(MAE $417)
- **$300 cap:** kills 31 winners ($4,149 of real wins given up vs $500). Worst-hit: QCOM +$431(MAE $343), SMCI +$383(MAE $313), MSTR +$365(MAE $461), ACN +$364(MAE $421), MSTR +$255(MAE $423)
- **$200 cap:** kills 64 winners ($8,173 of real wins given up vs $500). Worst-hit: QCOM +$431(MAE $343), SMCI +$383(MAE $313), MSTR +$365(MAE $461), ACN +$364(MAE $421), SNDK +$345(MAE $289)
- **$100 cap:** kills 116 winners ($15,758 of real wins given up vs $500). Worst-hit: QCOM +$431(MAE $343), HOOD +$413(MAE $133), MRNA +$384(MAE $176), SMCI +$383(MAE $313), MSTR +$365(MAE $461)

## READ
- Highest NET total in-sample: **$500** ($-4,726); live $500 = $-4,726. Tighter caps trade smaller losses for killed winners -- read the winners-KILLED column, that is the cost.
- 1-min fidelity + optimistic fills: tighter-cap losses are a best case, so winners-killed is if anything understated. In-sample -> ranks for an OOS test, does NOT promote a number.