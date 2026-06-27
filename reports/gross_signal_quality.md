# GROSS SIGNAL-QUALITY BREAKDOWN  (read-only, broker-truth; GROSS ONLY, no fees; n=285)
_The flat-average question: is +$187 gross 'no edge', or a positive slice + a losing slice?_

## ALL TRADES
- total gross **$+187** · avg **$+0.7/trade** (-0.11 bps) · median $+39.9 · win 57% · PF 1.01 · tails: MESU26 +$650 / MU $-1668

## 1) 9:35 path vs re-arm path
| group | n | total$ | avg$/trade | avg bps | win% | PF | median$ | big win / big loss |
|---|---|---|---|---|---|---|---|---|
| **9:35** | 111 | -3233 | -29.1 | -15.54 | 53% | 0.66 | +22.7 | QCOM +$433 / MU $-1668 |
| **re-arm** | 174 | +3420 | +19.7 | 9.74 | 59% | 1.3 | +58.2 | MESU26 +$650 / MESU26 $-862 |

## 2) Long vs short
| group | n | total$ | avg$/trade | avg bps | win% | PF | median$ | big win / big loss |
|---|---|---|---|---|---|---|---|---|
| **long** | 131 | -1532 | -11.7 | -7.33 | 53% | 0.87 | +36.6 | MESU26 +$650 / MU $-1668 |
| **short** | 154 | +1719 | +11.2 | 6.04 | 60% | 1.18 | +45.0 | QCOM +$433 / DELL $-658 |

## 3) Confirmed vs unconfirmed (0.15xATR, from exit_decisions.jsonl)
| group | n | total$ | avg$/trade | avg bps | win% | PF | median$ | big win / big loss |
|---|---|---|---|---|---|---|---|---|
| **confirmed** | 85 | +11453 | +134.7 | 70.75 | 98% | 229.15 | +117.5 | QCOM +$433 / PFG $-27 |
| **unconfirmed** | 53 | -11935 | -225.2 | -120.45 | 6% | 0.02 | -144.5 | MPWR +$158 / MU $-1668 |
| **unknown** | 147 | +669 | +4.5 | 2.31 | 52% | 1.08 | +9.4 | MESU26 +$650 / MESU26 $-862 |
> **LOOK-AHEAD WARNING:** 'confirmed' is decided AFTER entry (e.g. QCOM 6/25 first confirmed 09:41, ~6 min after its ~09:35 entry). The 98%-vs-6% split is therefore largely TAUTOLOGICAL ('trades that went favorably won') and is NOT an entry filter -- you don't know confirm state at entry. It is the EXIT lever (cut unconfirmed bleeders early = the gauntlet thesis), not a tradeable entry edge.

## 4a) Session segment
| group | n | total$ | avg$/trade | avg bps | win% | PF | median$ | big win / big loss |
|---|---|---|---|---|---|---|---|---|
| **open** | 113 | -4156 | -36.8 | -17.44 | 52% | 0.6 | +21.1 | QCOM +$433 / MU $-1668 |
| **midday** | 147 | +3414 | +23.2 | 11.01 | 61% | 1.36 | +67.3 | HOOD +$417 / BB $-620 |
| **close** | 25 | +930 | +37.2 | 12.85 | 52% | 2.06 | +7.4 | MESU26 +$650 / ACN $-201 |

## 4b) By hour (re-arm windows pay which hour?)
| group | n | total$ | avg$/trade | avg bps | win% | PF | median$ | big win / big loss |
|---|---|---|---|---|---|---|---|---|
| **09:00** | 111 | -3233 | -29.1 | -15.54 | 53% | 0.66 | +22.7 | QCOM +$433 / MU $-1668 |
| **10:00** | 57 | +2342 | +41.1 | 21.28 | 70% | 1.61 | +90.7 | HOOD +$417 / MESU26 $-862 |
| **11:00** | 35 | +56 | +1.6 | 4.65 | 60% | 1.02 | +67.3 | MSTR +$255 / NFLX $-476 |
| **12:00** | 34 | -59 | -1.7 | -1.01 | 47% | 0.98 | -10.1 | MRNA +$391 / COHR $-314 |
| **13:00** | 23 | +151 | +6.6 | 1.36 | 57% | 1.12 | +17.6 | CVNA +$345 / MSTR $-264 |
| **14:00** | 24 | +280 | +11.7 | 5.98 | 50% | 1.32 | +1.1 | VRT +$201 / ACN $-201 |
| **18:00** | 1 | +650 | +650.0 | 177.8 | 100% | inf | +650.0 | MESU26 +$650 / MESU26 $650 |

## 5) Extension at entry (over-extended gap-tops lose gross?)
| group | n | total$ | avg$/trade | avg bps | win% | PF | median$ | big win / big loss |
|---|---|---|---|---|---|---|---|---|
| **<5% (normal)** | 108 | -3949 | -36.6 | -17.44 | 53% | 0.6 | +11.4 | QCOM +$433 / MU $-1668 |
| **5-12% (extended)** | 80 | +2808 | +35.1 | 14.7 | 64% | 1.54 | +81.6 | HOOD +$417 / NFLX $-476 |
| **>=12% (gap-top)** | 12 | +800 | +66.7 | 33.64 | 75% | 1.79 | +168.6 | SMCI +$394 / BB $-620 |
| **unknown** | 85 | +529 | +6.2 | 3.21 | 53% | 1.11 | +21.1 | MESU26 +$650 / MESU26 $-862 |
> **INCONCLUSIVE for the L2 exhaustion thesis.** Gap = |entry_px - prior_close|/prior_close, i.e. gap vs the IMMEDIATE prior day -- this UNDERSTATES multi-day extension (MU 6/25 shows +3.4% because the 6/24 close had already absorbed the earnings move; the '17-19%' was vs an earlier base). And the >=12% bucket is only n=12. So this does NOT cleanly test 'over-extended gap-tops lose' -- needs a multi-day-extension field. Do not read the >=12%-wins row as refuting L2.

## COVERAGE / CAVEATS
- confirmed/unconfirmed known for 138/285 trades (rest unmatched in exit_decisions.jsonl).
- extension known for 200/285 (rest not in candidate log / move_pct null).
- **IN-SAMPLE, small N per slice, multiple pre-declared splits -> any strong slice is a HYPOTHESIS to test OUT-OF-SAMPLE, not a proven edge.** GROSS only (no commission/fees). 6/25 kill day included.