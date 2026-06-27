# GATE-EFFECT ANALYSIS — is the in-play gate helping or hurting? (read-only, GROSS, gate window 6/15-6/26)
_Counterfactual on never-traded names = DERIVED (ORB-break + live chandelier on 1-min bars), NOT broker-truth._

## 1) GATE-REJECTED (counterfactual) vs GATE-PASSED (broker-truth) on the 9:35 path
- **REJECTED (counterfactual, sample 260 of 867 feasible; 140 broke out & sim'd; sim VALIDATED -- QCOM/MU within ~5% of broker truth):** total $+6741, avg **$+48.2/trade**, win 81%, PF 1.98, median $+63.3.
- **PASSED (BROKER-TRUTH, the 9:35 names that actually traded, n=111):** total $-3233, avg **$-29.1/trade**, win 53%, PF 0.66.
- **READ: the gate REJECTED names that would have grossed MORE than the names it kept -- evidence it ANTI-SELECTS** (rejected = DERIVED sim, passed = broker-truth -> DIRECTIONAL, fidelities differ).
  rejected counterfactual by reject-reason: DAY_RELVOL_LOW=$+56.0/n73, INDEX_ETF_EXCLUDED=$-172.8/n1, MOVE_EXHAUSTED=$+139.4/n6, MOVE_TOO_SMALL=$+33.2/n60

## 2) Would the WINNING re-arm names survive the 9:35 gate?
- winning re-arm round-trips evaluated against the 9:35 gate's QUALITY criteria (RelVol/move/dir; liquidity floor bypassed -- $-vol not logged on re-arm): n=89 (would SURVIVE 29, would be BLOCKED 60, no-features 14).
- **gross on the BLOCKED winners: $+8,143** across 60; block reasons: {'DAY_RELVOL_LOW': 37, 'MOVE_EXHAUSTED': 19, 'MOVE_TOO_SMALL': 4}. If most winners would be blocked, the gate rejects the SAME kind of name that wins ungated -- evidence the gate (not just timing) is the problem.

## 3) 9:35 traded gross by name-type (gate-passed) — loss in fade-prone large-caps?
| mcap bucket | n | total gross | avg/trade | win% | PF |
|---|---|---|---|---|---|
| UNKNOWN | 1 | +199 | +198.7 | 100% | inf |
| large | 47 | -1112 | -23.7 | 51% | 0.73 |
| mega | 11 | -2521 | -229.2 | 27% | 0.18 |
| mid | 2 | -551 | -275.7 | 0% | 0.0 |
| unknown | 50 | +753 | +15.1 | 62% | 1.43 |

## 4) CLEAN time-of-day gross (NO gate lens) — timing alone
| entry time | n | total gross | avg/trade | win% | PF |
|---|---|---|---|---|---|
| 09:35 | 111 | -3233 | -29.1 | 53% | 0.66 |
| 10:35 win | 57 | +2342 | +41.1 | 70% | 1.61 |
| 11:35 win | 35 | +56 | +1.6 | 60% | 1.02 |
| 12:35 win | 34 | -59 | -1.7 | 47% | 0.98 |
| 13:35 win | 23 | +151 | +6.6 | 57% | 1.12 |
| 14:35 win | 24 | +280 | +11.7 | 50% | 1.32 |
| 18:35 win | 1 | +650 | +650.0 | 100% | inf |

## CAVEATS
- Counterfactual gross = DERIVED (1-min-bar ORB-break + live chandelier), NOT broker-truth; the fidelity check shows passed-sim vs passed-broker-truth differ -> treat task-1 as DIRECTIONAL.
- SAMPLED (rejected 260/867, passed 200/245); gate window 6/15-6/26 (gate live 6/16); INPUT_MISSING + DIR_MISMATCH rejections excluded (data-fail / structurally untradeable).
- In-sample, small N per bucket, multiple comparisons -> HYPOTHESIS test, not a gate change.