# NEWS-SENTIMENT ANONYMIZATION TEST (Glasserman-Lin distraction effect) -- read-only, shadow
_Same model (claude-sonnet-4-6, temp 0) scores each headline NAMED vs name/ticker-MASKED. n=30 mega-cap headlines (MU/NVDA/AAPL). Move = same-session open->close % (DERIVED, lower-fidelity)._

## DOES MASKING CHANGE THE READ?
- **Label changed by masking: 1/30 (3%)**; hard POS<->NEG polarity flips: **0/30 (0%)**.
- Mean |Δscore| named vs masked: **0.02** (scale -1..1).
- **NOISE FLOOR (same NAMED headline scored twice): self-disagreement 4/30 (13%), mean |Δscore| 0.05.** => the masking effect (1/30, 0.02) is AT/BELOW the model's own run-to-run noise -- INDISTINGUISHABLE from noise on this sample.
- label distribution NAMED: {'NEU': 10, 'NEG': 8, 'POS': 12} | MASKED: {'NEU': 9, 'NEG': 8, 'POS': 13}

## DOES MASKING ALIGN BETTER WITH WHAT THE STOCK DID? (mega-cap)
- NAMED  sign-match vs actual session move: **5/20** (25%)
- MASKED sign-match vs actual session move: **6/21** (29%)
- **Directional: MASKED aligns BETTER with the actual move.**
- **CONFOUND:** those joinable items collapse to only **3 distinct ticker-day outcomes** (AAPL/2026-06-26 +2.29%, MU/2026-06-26 -1.40%, NVDA/2026-06-26 -0.73%) -- the alignment % has ~3 degrees of freedom, not 20. Treat it as anecdote, not a rate.

## PER-ITEM (flips marked *)
| tk | cat | date | move% | NAMED | MASKED | flip |
|---|---|---|---|---|---|---|
| AAPL | earnings | 2026-06-26 | +2.29 | NEU +0.00 | NEU +0.00 |  |
| AAPL | sector | 2026-06-26 | +2.29 | NEG -0.45 | NEG -0.45 |  |
| AAPL | earnings | 2026-06-26 | +2.29 | NEG -0.45 | NEG -0.45 |  |
| AAPL | earnings | 2026-06-26 | +2.29 | NEU -0.10 | NEU -0.10 |  |
| AAPL | macro | 2026-06-26 | +2.29 | NEG -0.60 | NEG -0.60 |  |
| AAPL | sector | 2026-06-26 | +2.29 | NEG -0.55 | NEG -0.55 |  |
| AAPL | earnings | 2026-06-26 | +2.29 | POS +0.60 | POS +0.60 |  |
| AAPL | macro | 2026-06-26 | +2.29 | NEU +0.10 | NEU +0.10 |  |
| AAPL | earnings | 2026-06-26 | +2.29 | NEU +0.10 | POS +0.35 | * |
| AAPL | earnings | 2026-06-26 | +2.29 | NEU +0.10 | NEU +0.10 |  |
| MU | earnings | 2026-06-26 | -1.40 | NEU +0.00 | NEU -0.10 |  |
| MU | sector | 2026-06-26 | -1.40 | POS +0.82 | POS +0.82 |  |
| MU | earnings | 2026-06-26 | -1.40 | POS +0.72 | POS +0.72 |  |
| MU | earnings | 2026-06-26 | -1.40 | NEU -0.10 | NEU -0.10 |  |
| MU | macro | 2026-06-26 | -1.40 | NEG -0.55 | NEG -0.55 |  |
| MU | earnings | 2026-06-26 | -1.40 | POS +0.35 | POS +0.35 |  |
| MU | sector | 2026-06-26 | -1.40 | POS +0.92 | POS +0.92 |  |
| MU | analyst | 2026-06-26 | -1.40 | POS +0.55 | POS +0.40 |  |
| MU | analyst | 2026-06-26 | -1.40 | POS +0.78 | POS +0.75 |  |
| MU | earnings | 2026-06-26 | -1.40 | NEU +0.10 | NEU +0.05 |  |
| NVDA | m&a | 2026-06-26 | -0.73 | NEG -0.65 | NEG -0.65 |  |
| NVDA | fda | 2026-06-26 | -0.73 | POS +0.65 | POS +0.65 |  |
| NVDA | sector | 2026-06-26 | -0.73 | NEU +0.00 | NEU +0.00 |  |
| NVDA | sector | 2026-06-26 | -0.73 | POS +0.82 | POS +0.82 |  |
| NVDA | m&a | 2026-06-26 | -0.73 | NEG -0.60 | NEG -0.60 |  |
| NVDA | earnings | 2026-06-26 | -0.73 | POS +0.82 | POS +0.82 |  |
| NVDA | earnings | 2026-06-26 | -0.73 | NEG -0.45 | NEG -0.45 |  |
| NVDA | earnings | 2026-06-26 | -0.73 | NEU +0.05 | NEU +0.05 |  |
| NVDA | sector | 2026-06-26 | -0.73 | POS +0.72 | POS +0.72 |  |
| NVDA | m&a | 2026-06-26 | -0.73 | POS +0.60 | POS +0.60 |  |

## VERDICT + RECOMMENDATION
- **On our shadow data the distraction effect is WEAK-TO-ABSENT:** masking changed 1/30 reads (0 polarity flip) -- **at/below the model's own 4/30 run-to-run noise floor**, i.e. indistinguishable from noise -- and did NOT improve outcome alignment (named 5/20 vs masked 6/21, only 3 ticker-day outcomes).
- **Do NOT fold masking in as a *proven* accuracy win** -- this test did not reproduce one. BUT masking is cheap, harmless, and both the Columbia result and the (weak) directional lean here point the same way, so adopting **'mask name/ticker before LLM sentiment scoring' as a PRECAUTIONARY default** in any future news/LLM-reader is reasonable -- labeled research-motivated, not locally-proven.
- A real test needs: larger N, news time-joined to the correct FORWARD session (not a handful of same-day outcomes), and ideally a day where mega-caps moved BOTH directions. Re-run when news_shadow has accumulated more trading days.

## CAVEATS
- Small N, mega-cap-only, in-sample; LLM temp 0 but still stochastic across model versions.
- Outcome = same-session open->close move (DERIVED from 1-min bars); headline publish vs session timing is approximate (publish date's session). Not a tradeable result -- a DIRECTIONAL design check.
- Masking strips name/ticker + obvious aliases (products/execs); residual identifiability possible.
- SHADOW: no orders, no watched file, no trading impact.