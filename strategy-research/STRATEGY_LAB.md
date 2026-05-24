# Alpha Quant Strategy Lab — Multi-AI Test Log

## What we are trying to do — the purpose of this collaboration

**Goal:** Identify the best day-trading strategy possible for Rhett to deploy
on a $300,000 TradeStation account (with 4× intraday margin), using evidence
from rigorous backtests instead of social-media claims or marketing
material.

**Method:** A multi-AI collaboration. Multiple AI tools (Claude Code, Codex,
Claude desktop, ChatGPT, browser Claude) review the same candidate
strategies, audit each other's specs, and surface mistakes that any single
AI would miss. **Every candidate strategy gets backtested in QuantConnect
before it can be considered a contender** — and "best" is defined by the
"works" bar below (positive net P&L on both train and holdout, profit
factor ≥ 1.2, Sharpe ≥ 1.0, ≥ 10% annual net, survives the daily-loss cap).

**Process for each candidate strategy:**
1. **Spec construction** — Claude Code writes the Exact Spec from the source
   paper / book, with direct quotes and citations. No paraphrasing.
2. **Spec audit** — another AI checks the spec against the source.
3. **Approval** — Rhett locks the spec.
4. **Code** — Claude Code writes the QC algorithm to match the spec.
5. **Backtest** — Rhett (or a browser-Claude operator) runs the code in QC
   and reports results verbatim back to this document.
6. **Review** — all AIs comment, decision recorded, next candidate selected.

Repeat until we find a strategy that clears the "works" bar — or until we've
honestly exhausted credible candidates and have to revisit the goal.

**This document is the canonical record** for that collaboration: every
candidate proposed, every spec audited, every backtest run, every decision
made. Designed to be read by Claude Code and Codex via the repo, and by
Claude desktop / ChatGPT / browser Claude via paste.

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

## MANDATORY GLOBAL RULES — every strategy, no exceptions

These rules are non-negotiable. Set by Rhett 2026-05-23. They apply to every
strategy tested in this project, current and future. Any strategy that does
not implement these is INVALID and must be re-coded before its results count.

### G1 — End-of-day flatten
All positions must be liquidated by **3:50 PM ET** every trading day. No
overnight positions ever, regardless of P&L, regardless of strategy.

### G2 — Hard daily loss cap of $2,000
If realized + unrealized intraday P&L drops to **−$2,000** on any trading
day, the strategy stops opening new positions for the rest of that day and
liquidates anything still open. State resets at the next session open.
(This is 0.67% of a $300k account or 2% of a $100k account — tight, but
matches Rhett's risk tolerance for live deployment.)

### How this affects already-tested strategies
H1, H2, and H3 were tested with a $10k daily cap (inherited from the bot's
original risk config) and no portion of their loss caps was tight enough to
prevent the catastrophic single-day damages. Their results stand as
documented — they failed even under loose rules — but **all three should be
re-run with G1+G2 enabled** before any verdict is treated as final, because
the $2k cap might convert a "death-spiral" loss profile into a survivable
small-loss profile that exposes the true underlying expectancy.

---

## Project context (one-paragraph onboard for new reviewers)

Alpha Quant is Rhett Duleba's automated trading research project. An earlier
Claude Code session built a SIM trading bot on TradeStation; that bot's
original strategy (intraday momentum with very tight trailing stops) lost
−99.92% when backtested in QuantConnect. That kicked off this **strategy
research sub-project** in May 2026: testing falsifiable hypotheses one at a
time in QC to find one with real edge before any live deployment. Three
strategies have been tested so far; all three failed catastrophically; AND
Claude Code has admitted (and documented below) that its own implementation
errors account for a meaningful portion of those losses. The multi-AI
review protocol below exists specifically to catch those errors before the
next round.

---

## Rhett's goal, capital, and risk constraints

- **Capital:** $300,000 funded in the actual TradeStation account →
  $1,200,000 of intraday buying power via 4× margin. Lab backtests use
  $100,000 starting cash; scaling decisions are deferred until a strategy
  has cleared the "works" bar below.
- **Return goal:** ≥ $10,000 / year, net. (Rhett's original aspiration was
  $10k / month; Claude Code has flagged that as not realistic at this
  capital scale with retail constraints — it would require returns no
  fund has sustained over time. The lab targets the annual figure.)
- **Live daily loss tolerance:** −$500 / day. Lab backtests use a wider
  −$2,000 daily cap (G2 above) to give research headroom.
- **Tradable instruments:** liquid US equities only. No options, futures,
  or crypto. 4× intraday margin is part of the plan, which constrains us
  to TradeStation-margin-eligible names.

---

## Trader context — what Rhett's actual trading history shows

Claude Code audited Rhett's live TradeStation account on 2026-05-23 from
his full exported trade log (11,769 closed trades, 2022–2025). The
findings are directly relevant to strategy selection — any live
deployment will sit on top of behaviours this audit revealed.

- **Full record:** −$6,657,353 net realized.
- **Intraday only (same-day exits):** **+$1,448 — essentially break-even**
  across 3,294 trades.
- **Held overnight:** −$6,654,898 across 8,475 trades. **Virtually all
  of the loss came from positions held past the close.** Same instincts,
  same screens, same setups — the discipline of flatten-by-EOD was the
  difference between break-even and catastrophic loss.
- **Best scalp hold window:** 30 sec–1 min — the only net-positive bucket
  in the under-5-min range. Sub-30-sec exits leaked to panic; over-1-min
  holds leaked to pride.
- **Stock affinity:** intraday TSLA was **+$126,586** (742 trades, 58.5%
  win rate, winners 1.11× size of losers). Intraday NVDA was
  **−$117,701** (1,242 trades, 47.7% win, 0.89× win/loss). Stocks that
  respect price action: Rhett reads. Stocks in relentless one-way trends
  (NVDA 2024): Rhett gets whipsawed.
- **Stated style:** "Read candles, go in heavy with full buying power for
  ~30 seconds, get out." Emotional overrides (panic vs. pride) were the
  dominant failure mode, not strategy choice.

**Implication for strategy selection:** Rhett's edge — to the extent he
has one — is intraday scalping on stocks that respect price action.
Strategies the lab tests should either fit that profile or have an
explicit reason to differ.

---

## What "works" means (the bar a strategy must clear)

A strategy is "works" only if ALL of the following hold:

| Criterion | Bar |
|---|---|
| Net P&L after slippage (lab default 0.05%, see M2) | Positive |
| Profit factor | ≥ 1.2 |
| Sharpe ratio | ≥ 1.0 |
| Train period (2016-2021) | Net positive |
| Holdout period (2022 to present) | Net positive (run ONCE) |
| Annual return, net of costs | ≥ ~10% |
| Worst-day P&L distribution | Survives G2 ($2,000/day) at reasonable sizing |

Anything that clears most but not all stays in development. No partial
credit for "almost works."

---

## Claude Code's documented failure modes — what every reviewer must watch for

These are documented blind spots of Claude Code (the lead AI on this
project), agreed by both Rhett and Claude Code on 2026-05-23. Every
reviewer (AI or human) should specifically check for these on every
deliverable.

1. **"Translating faithfully" while drifting from spec.** Claude Code
   reads a paper, then writes code *labeled* "faithful" while silently
   substituting its own defaults for paper-specified values. H3 is the
   documented example: code committed as "faithful Zarattini" had the
   stop logic, direction filter, and profit-target rule all changed from
   the paper. **Reviewers: line-by-line audit each Exact Spec section
   against its cited source. This is the single highest-yield check.**
2. **Filling gaps with reasonable-looking defaults instead of asking.**
   When the source is under-specified, Claude Code substitutes "typical"
   trading-code defaults rather than flagging the gap. Reviewers: any
   spec value without a source citation is suspect.
3. **Treating paraphrase as faithful copy.** Claude Code summarizes
   papers from memory and treats the summary as a reliable copy.
   Reviewers should check that each Exact Spec section contains *direct
   quotes* from the source, not Claude Code's reword.
4. **Insufficient skepticism of catastrophic results.** When a backtest
   returns ≤ −50% / year, Claude Code's reflex has been "the strategy
   doesn't work" rather than "the framework or my implementation may be
   broken." Reviewers should push back on any catastrophic result by
   asking whether the framework sanity check (H0 / M1) was run first.
5. **Producing before verifying.** Claude Code optimizes for completing a
   deliverable rather than pausing to verify assumptions. Reviewers
   should ask whether Claude Code asked any clarifying questions before
   the work was done — silence on a non-trivial task is a flag.

These are common LLM failure modes, not unique character flaws of Claude
Code. The point of documenting them here is so the protocol catches them.

---

## Claude Code's protocol commitments

Claude Code committed to the following on 2026-05-23. Reviewers can hold
Claude Code to any of these on any deliverable.

1. **State assumptions before acting.** Before non-trivial work, write
   out what is being assumed and what might be wrong, before delivering.
2. **Quote sources, don't paraphrase.** When implementing a published
   strategy, quote the spec from the source with section/page citations.
3. **Audit extreme results first.** Backtest ≤ −50% or ≥ +100% / year →
   first hypothesis is implementation error; sanity-check the framework
   before treating the result as a verdict on the strategy.
4. **Smaller commits with checkpoints.** No more 300-line single-shot
   deliverables; build incrementally with confirmation pauses.
5. **Honest uncertainty.** "I don't know" beats a confident default. If
   I'm guessing, the guess is labeled as a guess.

---

## Reviewer protocol — six stages, every new strategy

To prevent the H1/H2/H3 pattern (strategies tested that didn't actually
match their cited source), every new strategy follows this sequence:

| Stage | Who | What |
|---|---|---|
| 1. Spec construction | Claude Code | Write Exact Spec from the cited source, with direct quotes and section/page citations for every parameter. State all assumptions. **No code yet.** |
| 2. Spec audit | Another AI (Codex via repo / Claude desktop / ChatGPT) | Audit the spec against the cited source. Flag every deviation. Flag every uncited default. Confirm G1 + G2 are included. Append commentary to the strategy's "AI commentary" section. |
| 3. Spec approval | Rhett | Read the audited spec. Approve for code, or send back for revision. The locked spec is point-of-no-return for that strategy version — any later change creates a new version (H4.2, etc.). |
| 4. Code | Claude Code | Write QC code that matches the locked spec line-by-line. Add code reference to the entry. |
| 5. Backtest | Browser-Claude operator (or Claude Code via QC API) | Run in QC with the lab's standard cost assumptions. Record results verbatim. |
| 6. Result review | Any AI | Append commentary. Decision recorded (continue / kill / variant). |

This is deliberately more process than H1/H2/H3 used. The extra friction
is the price of catching the failure modes above.

---

## Calibration assumptions in use

| Assumption | Default | Status |
|---|---|---|
| Slippage per fill | 0.05% (`ConstantSlippageModel(0.0005)`) | M2: likely too harsh; verify post-H0 |
| TradeStation real-world borrow (SIM, EOD flatten) | $0 | Confirmed by Rhett |
| TradeStation real-world commission on US stocks | $0 | Commission-free since 2019 |
| QC's backtest simulation of TS fees | Unverified | M3: open question — backtests reported large fee numbers that need explaining |
| Train window | 2016-01-01 to 2021-12-31 | Locked |
| Holdout window | 2022-01-01 to present | Locked; run **once** per strategy |
| Starting cash for lab backtests | $100,000 | Locked |

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

### M3 — QC brokerage simulation accuracy (NOT a claim about real TradeStation)
Real TradeStation in SIM mode with same-day flatten has **zero** borrow cost
and **zero** equity commission (Rhett confirmed). The open question here is
whether QC's *backtest simulation* of the TradeStation brokerage model
accurately reflects that — i.e., whether the H3 backtest's $22,877 in "Fees"
represents real-world charges that would apply or phantom backtest costs.
Action: inspect QC's TradeStation brokerage model source, or compare the
backtest's reported fees against a live-SIM day's actual TradeStation
charges on similar volume. This is a calibration question for QC, NOT a
claim about TradeStation's real-world rules.

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

# Candidate strategies (proposed menu — awaiting Stage 1)

Claude Code proposed the following candidates on 2026-05-24 from training
knowledge. Each is a documented day-trading approach with at least one
credible source. **None are coded or even spec'd yet** — they are a menu
for Rhett to choose from. The chosen candidate becomes H4 (then H5, H6...)
and goes through the full 6-stage reviewer protocol.

Citation status:
- **CONFIRMED** = Claude Code is confident of the source / author / claim.
- **TO VERIFY** = likely correct but needs Codex or paste-AI confirmation
  before Stage 1 begins.

| # | Strategy | Source | Cite status | Why it might fit Rhett |
|---|---|---|---|---|
| C1 | **Zarattini ORB on Stocks in Play (FAITHFUL version)** | Carlo Zarattini & Andrew Aziz, "A Profitable Day Trading Strategy For The U.S. Equity Market," SSRN 2024 | CONFIRMED | Best-documented public day-trading edge of the last few years. H3 was meant to be this but drifted from spec. C1 would be the actual faithful build — top 20 by abnormal opening volume, 5-min OR, ATR-based stops, R-multiple profit target, gap-direction filter. |
| C2 | **Zarattini TQQQ Opening Range Breakout** | Carlo Zarattini, "Beat the Market: An Effective Intraday Momentum Strategy for the S&P500 ETF (SPY)" / TQQQ companion paper, SSRN | TO VERIFY | Single-instrument ORB on a leveraged index ETF. Simpler universe than C1; tests the ORB concept on a known liquid leveraged name. |
| C3 | **Crabel NR7 / Inside-Bar Opening Range Expansion** | Toby Crabel, *Day Trading with Short Term Price Patterns and Opening Range Breakout* (1990) | CONFIRMED | Pre-Zarattini foundational ORB research. Filters: narrow-range bars (NR4/NR7) and inside days precede expansion. Pattern-based, simple, intraday — well-suited to Rhett's "read candles" style. |
| C4 | **Connors RSI(2) Short-Term Mean Reversion** | Larry Connors & Cesar Alvarez, *Short Term Trading Strategies That Work* (2008); also Connors & Alvarez SSRN papers | CONFIRMED (book) | Buy stocks closing weak (RSI(2) < 10), exit on bounce. Originally end-of-day; intraday adaptations exist. Mean-reversion style — different family from ORB / breakout. Useful as a "different bet" if breakouts keep failing in our backtests. |
| C5 | **First-Half-Hour / Intraday Momentum** | Lei Gao, Yufeng Han, Sophia Zhengzi Li, Guofu Zhou, "Market Intraday Momentum," Journal of Financial Economics 2018 | TO VERIFY | First-half-hour return predicts last-half-hour return. Academic peer-reviewed; tested on broad equity markets. Trade at end of day based on opening move. Quick exit aligns with EOD flatten. |
| C6 | **Post-Earnings Announcement Drift, intraday slice** | Original: Bernard & Thomas (1989). Many follow-ups in academic literature. | CONFIRMED (concept) / TO VERIFY (specific spec) | Trade stocks that just reported earnings, in the surprise direction. PEAD is one of the most robust academic anomalies. Intraday slice = enter on the earnings day, exit by close. Fewer setups (earnings season heavy) → less cost drag. |

## Open question (for Rhett)

Which candidate becomes H4? My recommendation, with reasoning, in the
"Cross-AI parking lot" below — but the call is yours.

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
- **[Claude Code 2026-05-24]** My recommendation on the candidate menu
  ordering, with reasoning, for Rhett to consider:
  - **First (H4): C1 — faithful Zarattini.** We already burned a backtest
    on a drift version (H3). Closing the loop with the actual paper is
    the highest-information test we can run, AND it tests whether the
    most-credible public day-trading paper holds up in our hands.
  - **Second (H5): C3 — Crabel NR7 / inside-bar ORB.** Different
    universe-selection mechanism (pattern-based vs. volume-rank), so
    independent evidence about whether the ORB family works at all.
  - **Third (H6): C5 — first-half-hour momentum.** Different timeframe
    and direction (afternoon trade based on morning move) — diversifies
    the kinds of edge we're testing.
  - C4 (Connors mean-reversion) is the right "if all breakouts fail"
    pivot — a different bet family entirely. Defer until we know
    breakouts don't work.
  - C2 (Zarattini TQQQ) and C6 (PEAD intraday) are interesting but more
    specialized — propose deferring unless Rhett has a specific reason
    to prioritize.
  Reasoning behind ordering: maximize *independent information* per
  backtest. Testing two ORB variants in a row (C1 then C3) gives us
  data on whether the family works, not just one paper. Then C5 tests
  a fundamentally different setup. By the time three are tested we'll
  know whether the family has any signal at all.
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
- 2026-05-23 (expanded) — Per Rhett's "ultimate-performance" request,
  added: project-context onboard paragraph; Rhett's goal/capital/risk
  block; trader context from the 11,769-trade live-history audit; the
  "works" bar; Claude Code's documented failure modes (so reviewers
  know what to catch); Claude Code's protocol commitments; six-stage
  reviewer protocol (spec → audit → approval → code → backtest →
  review); calibration assumptions table. Designed so any new AI
  reviewer can read this document cold and immediately know the
  project, the rules, the trust calibration, and how to contribute.
- 2026-05-24 — Replaced the doc's opening with an explicit "What we are
  trying to do" purpose statement (collaboratively identify the best
  day-trading strategy via backtested evidence; every candidate gets
  backtested before it can be considered). Added the **Candidate
  Strategies** menu (C1–C6) so reviewers and Rhett can pick the next
  strategy to enter the 6-stage protocol. Claude Code's recommended
  order added to the Cross-AI parking lot.
