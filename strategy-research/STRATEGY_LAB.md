# Alpha Quant Strategy Lab — Multi-AI Test Log

**Purpose:** the single canonical record of every trading strategy tested for
this project. Designed for review by multiple AI tools — Claude Code, Codex,
Claude desktop, ChatGPT, browser Claude — each of which has different blind
spots. Cross-checking each other's reasoning is the protection against any
single AI's bad assumptions (especially Claude Code's track record of
"translating faithfully" while drifting from spec).

---

## How to use this document

### For repo-aware AIs (Claude Code, Codex, Cursor)
Read this entire file directly. Update the relevant entry's status / commentary
section when you have something to contribute. Append-only — never delete prior
analysis, even if wrong (the wrong analysis is itself useful evidence).

### For paste-based AIs (Claude desktop, ChatGPT, browser Claude)
Rhett will paste **one entry at a time** for review. Your job:
1. **Audit the "Exact spec" section against the cited source.** This is the
   single most important check. If the source is a paper, verify each spec
   line matches the paper. Flag any deviation, no matter how small.
2. **Audit the code reference against the spec.** Does the code actually
   implement what the spec says?
3. Add your commentary to the entry's "AI commentary" section and give it
   back to Rhett to paste into the doc.

### The cardinal rule
**The Exact Spec section is the source of truth.** If code or test diverges
from spec, the code/test is wrong, not the spec. If the spec is wrong, the
spec gets edited first, then the code, then we re-run.

---

## Open meta-issues across all strategies

These are problems that affect multiple strategies and need to be resolved
*before* trusting any future backtest result.

### M1 — Framework calibration (CRITICAL, NOT YET DONE)
We have not yet verified that our QC framework (TradeStation brokerage model,
slippage settings, sizing logic, fee model) produces correct results on a
known-good baseline. Until we do, every backtest result is suspect.

**Required test:** Buy SPY on START date, hold until END date, no other
activity. Expected result for 2016-01-01 → 2021-12-31: roughly +90% (the
actual market return). If our framework returns anything materially different,
we have a configuration bug.

**Status:** Not yet run. **Should be run before any further strategy test.**

### M2 — Slippage assumption may be too harsh
We've been using `ConstantSlippageModel(0.0005)` = 0.05% per fill. For
marketable limit orders on mega-caps that's plausibly 3-5× the real number.
Compound across 10,000 trades and a strategy that would be flat ends up
−40%. Worth re-running H1/H2 with `0.0001` (0.01%) as the realistic-retail
slippage assumption.

### M3 — Brokerage model commission/borrow costs unaudited
TradeStation is commission-free for US stocks since 2019, but the QC
brokerage model may include phantom commissions or short-borrow costs that
don't reflect reality. Need to inspect QC's TradeStation model source or
test by comparing fees against TradeStation's actual fee schedule.

### M4 — Position sizing creates death-spiral asymmetry
Our sizing scales positions DOWN as equity drops (correct from a risk
standpoint), but combined with steady small losses it creates an asymptote
toward zero rather than a natural stop. Real traders stop trading at a max
daily loss or max drawdown. We should add a global circuit breaker:
`if equity < STARTING_CASH * 0.8: stop trading for the day`. This is
both more realistic and prevents the −99% style results we keep seeing.

---

## Entry template — copy this when starting a new strategy

```markdown
## H<N> — <Strategy name>

**Status:** [PROPOSED / SPEC LOCKED / CODED / TESTED / PASSED / FAILED]
**Date created:** YYYY-MM-DD
**Hypothesis (one falsifiable sentence + why it might be true):**
> [...]

**Source:** [paper citation with link, or "original idea"]

### Exact spec (every parameter, every rule — leave NOTHING to defaults)
- Universe: [...]
- Universe filter rules: [price, volume, etc., with exact thresholds]
- Opening range / signal window: [exact times]
- Direction filter: [gap, regime, news, etc. — what determines long vs short]
- Entry rule: [exact trigger]
- Stop rule: [exact placement formula]
- Profit target rule: [exact, or "none — held to EOD"]
- Exit time: [hard time-based exit]
- Sizing: [exact formula, including risk % and any caps]
- Position limits: [max concurrent, max per sector, etc.]
- Daily circuit breaker: [if applicable]
- Backtest period (train): [dates]
- Backtest period (holdout, run later): [dates]
- Slippage model: [exact value]
- Brokerage model: [QC name]

### Code reference
[file path in repo]

[paste-friendly code block here for non-repo AIs to review]

### Test runs
| Date run | Slippage | Window | Net P&L | Sharpe | Profit factor | Max DD | Notes |
|---|---|---|---|---|---|---|---|

### AI commentary (append-only, signed)
- **Claude Code [YYYY-MM-DD]:** [...]
- **Codex [YYYY-MM-DD]:** [...]
- **Claude desktop [YYYY-MM-DD]:** [...] (pasted in by Rhett)
- **ChatGPT [YYYY-MM-DD]:** [...] (pasted in by Rhett)

### Decision
[Continue / kill / variant / blocked-on-X]

### Lessons learned
[What this entry taught us — even if the strategy failed]
```

---

# Strategies tested

## H0 — Buy-and-hold SPY (framework sanity check)

**Status:** PROPOSED — NOT YET RUN. **This must be run before any other
strategy is trusted.**
**Date created:** 2026-05-23
**Hypothesis:**
> Our QC framework, configured identically to how we test active strategies,
> should reproduce the actual market return on a passive buy-and-hold SPY
> position over 2016-2021 (~+90%). If it doesn't, our framework is
> miscalibrated and every prior backtest result is suspect.

**Source:** Sanity check — not a real strategy.

### Exact spec
- Universe: SPY only
- Entry rule: Buy SPY at first minute of START date, full equity ($100,000 → ~$250 worth at first close).
- Stop rule: None.
- Exit rule: Liquidate at last minute of END date.
- Sizing: 100% of equity.
- Slippage model: ConstantSlippageModel(0.0005)
- Brokerage model: TradeStation, Margin
- Backtest period: 2016-01-01 to 2021-12-31

### Code reference
**TO BE BUILT.**

### Expected result
- Net return: +85% to +95% (the actual S&P 500 total return over that window)
- If we get something materially different (+50%, −20%, etc.) — STOP and fix
  the framework before testing any other strategy.

### AI commentary
- **Claude Code [2026-05-23]:** I should have proposed this before H1. Failing
  to baseline-test the framework before testing strategies is the single
  biggest process error in my work on this project. Until H0 passes, every
  prior result is suspect.

---

## H1 — Opening Range Breakout (small universe)

**Status:** FAILED — but result may be invalid pending H0 framework check.
**Date tested:** 2026-05-22
**Hypothesis:** On 36 large-cap stocks, a 15-min opening-range breakout
generates positive expectancy.

**Source:** Loosely inspired by Zarattini & Aziz (2024). **NOTE: H1 was NOT a
faithful test of the Zarattini paper.** See lessons learned.

### Exact spec
- Universe: 36 fixed large-caps (AAPL, MSFT, NVDA, etc.)
- Opening range: First 15 minutes (9:30-9:45)
- "In play" filter: today's OR volume > 1.5 × 14-day avg
- Entry: Break above OR_high (long) or below OR_low (short)
- Stop: Opposite end of opening range
- Profit target: None
- Exit: Stop or EOD flatten at 3:50 PM
- Sizing: 1% of equity risked per trade, capped at 25% notional
- Position limits: 5 concurrent max
- Slippage: 0.05%
- Brokerage: TradeStation, Margin
- Backtest period: 2016-01-01 to 2021-12-31

### Code reference
`strategy-research/orb_h1_backtest.py`

### Test runs
| Date | Slippage | Net P&L | Win rate | Profit factor | Max DD |
|---|---|---|---|---|---|
| 2026-05-22 | 0.05% | **−72.2%** | 43% | 1.10 | 73% |
| 2026-05-22 | 0.0% | −3.8% | 46% | 1.15 | 31% |

### AI commentary
- **Claude Code [2026-05-22]:** Initially recorded this as "ORB failed."
  That was over-stated. H1 used a static volume threshold (1.5×) instead of
  the paper's daily ranking against a broad universe — and that's the entire
  edge in "stocks in play." H1 is properly characterized as "a simplified
  ORB-on-large-caps failed," not "Zarattini's strategy failed." Also: per
  M2, the 0.05% slippage is probably too harsh. The 0% run was nearly
  break-even, suggesting cost drag is doing most of the killing.

### Lessons learned
- Don't strip the universe-selection mechanism out of a "stocks in play"
  strategy — it IS the strategy.
- Run with realistic AND zero slippage to separate cost drag from edge
  absence. (We did this for H2 and H3 — good practice going forward.)

---

## H2 — Gap Continuation

**Status:** FAILED (near miss) — result may be invalid pending H0.
**Date tested:** 2026-05-22
**Hypothesis:** Stocks gapping ≥4% at the open and holding the gap through
the first 15 minutes continue in the gap direction through the session.

### Exact spec
- Universe: Same 36 large-caps
- Catalyst filter: |overnight gap| ≥ 4%
- Confirmation: at 9:45, price still on gap side of day's open
- Entry: One decision per stock per day at 9:45
- Stop: Opposite end of first-15-min range
- Profit target: None
- Exit: Stop or EOD flatten 3:50 PM
- Sizing: 1% risk per trade, 25% notional cap
- Position limits: 5 concurrent
- Slippage: 0.05%
- Backtest period: 2016-2021

### Code reference
`strategy-research/h2_gap_continuation_backtest.py`

### Test runs
| Date | Slippage | Net P&L | Win rate | Profit factor |
|---|---|---|---|---|
| 2026-05-22 | 0.05% | **−5.7%** | 42% | 1.27 |
| 2026-05-22 | 0.0% | **+1.5%** | 44% | 1.32 |

### AI commentary
- **Claude Code [2026-05-22]:** H2 is the closest thing to a positive result
  we've seen. Run B (zero slippage) is positive; Run A is barely negative.
  Catalyst selection (4% gap) was working — strategy had real but small gross
  edge. Killed by transaction costs in Run A. This contradicts the
  "everything fails" narrative — H2 had genuine signal. Worth revisiting
  with smaller slippage assumption (per M2) and possibly larger catalyst
  threshold (5-6%) to thin trade count.

### Lessons learned
- A strong catalyst filter (4% gap) generates a real, small signal.
- The line between "barely fails" and "passes" is the slippage assumption.
  Our pessimistic 0.05% may be misleading us about the strategy class.

---

## H3 — "Zarattini Stocks-in-Play" (Claude Code's drift version)

**Status:** FAILED catastrophically (−99.97%) — but the implementation
was NOT faithful to the published paper. See lessons learned.
**Date tested:** 2026-05-23

### What I claimed it was
"Faithful Zarattini & Aziz (2024) ORB on stocks in play."

### What it actually was
- Universe: ~1000 stocks by daily dollar volume — ✓ (matches paper)
- Top 20 by abnormal first-5-min volume — ✓ (matches paper)
- 5-min opening range — ✓ (matches paper)
- Stop: **1.0 × ATR(14) daily** — ✗ paper uses OR-opposite-side
- Direction: **either side of OR break** — ✗ paper uses gap-direction
  bias (gap up → only long; gap down → only short)
- Profit target: **none** — ✗ paper uses R-multiple target
- Sizing: 1% risk by ATR — partially matches paper

### Code reference
`strategy-research/h3_zarattini_orb_backtest.py`

### Test runs
| Date | Slippage | Net P&L | Notes |
|---|---|---|---|
| 2026-05-23 | 0.05% | −99.97% | Account wiped to $32 by 2019 |

### AI commentary
- **Claude Code [2026-05-23]:** I labeled this "faithful Zarattini" and
  committed it to the repo. It wasn't. I substituted my own choices for
  three of the paper's key mechanisms (stop logic, direction filter,
  profit target). Each one alone could flip a winning strategy to losing.
  Together they produced −99.97%. **The result is real, but the result is
  about MY implementation, not the paper's strategy.** I owe a properly
  faithful test (provisional H4) and a documented audit of my deviations
  against the paper before that test.

### Lessons learned
- When implementing a published strategy, transcribe the paper line-by-line
  into the spec section BEFORE writing any code. Do not fill in details
  from my own "reasonable defaults."
- When a result returns −99%+, my first hypothesis must be "implementation
  error" not "strategy doesn't work." Three catastrophic results in a row
  is a signal that I'm the variable.
- The "Exact spec" section in this template exists specifically to catch
  the H3-style drift. Future strategies: a paste-based AI should audit the
  spec against the source paper BEFORE Claude Code writes any code.

---

# Cross-AI parking lot

(Open questions/observations that don't belong to any single strategy.
Any AI can append here.)

- **[Claude Code 2026-05-23]** Should we test a buy-and-hold benchmark
  besides SPY? E.g., a momentum-factor ETF like MTUM, or a sector-rotation
  ETF, to verify our framework on stocks that move differently than the
  index.
- **[Claude Code 2026-05-23]** The Zarattini paper has multiple variants.
  Before we re-implement, we should agree on WHICH variant we're testing,
  cite the section/page, and lock the spec.
- **[OPEN]** Has anyone audited QC's TradeStation brokerage model source
  code to see what it actually charges?

---

# Document changelog

- 2026-05-23 — Created by Claude Code at Rhett's direction after three
  consecutive catastrophic strategy results revealed systematic process
  errors. Initial entries for H0 (sanity check), H1, H2, H3.
