# TAPE WATCHER — SHADOW REPORT 2026-06-25  (v1, SHADOW ONLY; replay = 1-min-bar proxy)
_generated 2026-06-27 12:37:27 · broker truth = eod_debrief.round_trips_net · TW would-do = tw_shadow.jsonl · NO orders sent_

**Exit params TW used (read from code):** resting **1.4×ATR** (`orb_runner.py:RESTING_SL_FRAC`), confirm **0.15×ATR**, chandelier **1.4×ATR**, mode `candle_1.4atr_chandelier`, exit fn = `candle_close_exit.chandelier_decision (the live function, reused verbatim)`.

## 1) COVERAGE — would TW put a stop on EVERY entry?
- **TW: 23/23 = 100%** of entries get a protective stop at fill (9:35 cohort 7/7, re-arm 16/16).
- **LIVE today (broker truth, re-derived): 107/282 = 37.9%** — 9:35 ~96% / re-arm 0%.
- **Would-place latency:** min 0s / median 0s / max 0s — vs the live **~7–8 min** median (placed at fill, not in a later pass).

## 2) TICK COMPLETENESS
- **N/A in replay** — this run is a 1-min-bar proxy, not the live tick stream. Tick completeness (no-gap continuous stream vs broker-truth bars) is measured only in `--live`. **Flagged: live-tape proof is still owed (needs a trading session).**

## 3) EXIT RECONCILIATION — TW would-fire vs broker actual
| sym | side | occ | conf | broker exit | TW would-fire | Δ time | TW reason | note |
|---|---|---|---|---|---|---|---|---|
| DELL | short | 1 | — | 404.85 @ 15:50 | _held to EOD/none_ | — | — | TW held (would EOD-flatten) |
| QCOM | short | 1 | Y | 209.09 @ 09:45 | 209.1 @ 09:46 | +1m | CANDLE_CLOSE_REVERSAL |  |
| PENN | long | 1 | Y | 21.15 @ 15:50 | 21.64 @ 09:42 | -368m | CANDLE_CLOSE_REVERSAL | ✓ cut bleeder earlier |
| MU | long | 1 | N | 1141.81 @ 09:55 | 1146.07 @ 09:55 | -0m | CHANDELIER_STOP | ✓ cut bleeder earlier |
| LUV | long | 1 | Y | 52.45 @ 09:53 | 52.39 @ 09:54 | +1m | CANDLE_CLOSE_REVERSAL |  |
| CME | short | 1 | — | 225.34 @ 15:50 | _held to EOD/none_ | — | — | TW held (would EOD-flatten) |
| SWK | long | 1 | Y | 91.56 @ 09:44 | 91.93 @ 09:45 | +1m | CANDLE_CLOSE_REVERSAL |  |
| TECH | long | 1 | Y | 70.67 @ 15:33 | 70.67 @ 15:34 | +1m | CANDLE_CLOSE_REVERSAL |  |
| PNR | long | 1 | — | 75.9 @ 15:50 | _held to EOD/none_ | — | — | TW held (would EOD-flatten) |
| BB | long | 1 | — | 10.31 @ 15:50 | _held to EOD/none_ | — | — | TW held (would EOD-flatten) |
| GLW | long | 1 | — | 225.03 @ 15:50 | _held to EOD/none_ | — | — | TW held (would EOD-flatten) |
| SNDK | long | 1 | Y | 2205.65 @ 10:54 | 2213.0 @ 10:55 | +1m | CANDLE_CLOSE_REVERSAL |  |
| AAPL | short | 1 | Y | 277.89 @ 11:01 | 277.81 @ 11:02 | +1m | CANDLE_CLOSE_REVERSAL |  |
| FLEX | long | 1 | Y | 165.25 @ 12:18 | 165.6 @ 12:19 | +1m | CANDLE_CLOSE_REVERSAL |  |
| PLTR | short | 1 | Y | 107.17 @ 11:00 | 107.17 @ 11:01 | +1m | CANDLE_CLOSE_REVERSAL |  |
| ALB | short | 1 | — | 141.13 @ 15:50 | _held to EOD/none_ | — | — | TW held (would EOD-flatten) |
| RVTY | long | 1 | Y | 113.14 @ 11:59 | 113.02 @ 11:49 | -10m | CANDLE_CLOSE_REVERSAL | ⚠ CLIP? (TW earlier, less $ on a winner) |
| NOW | short | 1 | Y | 89.84 @ 15:29 | 89.75 @ 15:30 | +1m | CANDLE_CLOSE_REVERSAL |  |
| MSTR | short | 1 | Y | 85.74 @ 12:44 | 85.62 @ 12:45 | +1m | CANDLE_CLOSE_REVERSAL |  |
| AMAT | long | 1 | Y | 654.68 @ 13:15 | 654.4 @ 13:16 | +1m | CANDLE_CLOSE_REVERSAL |  |
| TER | long | 1 | Y | 466.56 @ 14:27 | 465.85 @ 14:22 | -6m | CANDLE_CLOSE_REVERSAL | ⚠ CLIP? (TW earlier, less $ on a winner) |
| MSFT | short | 1 | Y | 349.46 @ 13:50 | 349.6 @ 13:51 | +1m | CANDLE_CLOSE_REVERSAL |  |
| TJX | short | 1 | Y | 157.25 @ 15:26 | 157.07 @ 15:27 | +1m | CANDLE_CLOSE_REVERSAL |  |

**Summary:** TW fired EARLIER on **3**, later on **13**, held-to-EOD on **6**. Bleeders cut earlier: **2**. Possible winner-clips (must-not-cut watch): **2**.
> Prices are a 1-min-bar proxy → treat Δ$ as DIRECTIONAL, not to the cent. The MU 6/25 case (unconfirmed long, CHANDELIER_STOP) is the key bleeder-protection example; confirmed winners flagged above need the must-not-cut review before any live cutover.

## 4) STABILITY
- replay run: deterministic, no stream. Live uptime/reconnect/CPU-mem = **owed in `--live`** (disconnects logged: 0).

## VERDICT (v1 shadow)
- Coverage **100%** vs live 37.9% ✓ · would-place latency **~0s** vs ~7 min ✓ · exit logic = the live function, reused verbatim ✓.
- **Still owed before any live talk:** live-tape proof (tick completeness + stability across a real session), and the must-not-cut review of any flagged winner-clips. SHADOW ONLY; zero orders sent.