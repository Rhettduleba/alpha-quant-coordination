# Strategy Research — Hypothesis H1: Opening Range Breakout

**Sub-project:** Rebuild Alpha Quant's strategy layer on evidence.
**Created:** May 22, 2026 · **Owner:** Rhett · **Lab:** QuantConnect
**Status:** PLAN + v1 CODE WRITTEN — awaiting first train-period backtest.

---

## Why this sub-project exists

A QuantConnect price-replay of Alpha Quant's *current* strategy returned −99.92%
over 2021–2025. The current strategy has no stated edge and parameters that were
never validated (a 0.08% trailing stop, tighter than the cost of trading). It is
being treated as **one dead hypothesis**. This sub-project restarts the strategy
layer the disciplined way: one falsifiable hypothesis at a time, tested honestly
in QuantConnect, killed fast if it shows no edge.

The bot's infrastructure (execution, risk floors, the QC backtester, the Research
Brain universe) is sound and is kept. Only the **strategy logic** is being rebuilt.

---

## Goal & risk constraints (Rhett, stated 2026-05-22)

- **Capital:** $100,000 — fixed; this is the entire account.
- **Target:** make ~$10,000 (≈10% on capital).
- **Daily risk limit:** lose no more than **$500 in any single day** (0.5% of
  capital), at least until the account is up.
- **Implication for this research:** the $500/day limit is ~20× tighter than the
  live bot's current $10,000 daily guard. Any strategy validated here must be
  sized and judged against ~$500/day — and a strategy with frequent days worse
  than −0.5% is not viable under this constraint regardless of total return.
  Backtests must therefore report the **distribution of daily P&L** (worst days,
  count of days beyond −$500), not just the headline return.

---

## Hypothesis H1

> **On liquid US large-cap stocks that open with elevated relative volume
> ("stocks in play"), a breakout above the first 15-minute range continues in
> the breakout direction often enough to be profitable net of realistic costs
> (and the mirror for downside breakouts).**

**Why it might be true (the edge rationale):** the opening 15 minutes establish a
reference range. When a stock that is *already* trading on unusual volume — a sign
of news or institutional flow — breaks that range, the move tends to reflect
genuine repricing that continues intraday, rather than noise. Random low-volume
stocks just chop. The "in play" filter is what separates signal from noise.

This is a documented, researched family of strategies (it appears in QC's own
research library; cf. Zarattini & Aziz, *Can Day Trading Really Be Profitable?*,
2023). We are not inventing it — we are testing whether it survives **in our
hands, net of costs**, before trusting anything.

---

## The strategy — minimal v1 (deliberately few parameters)

| Element | Rule |
|---|---|
| Universe | ~36 fixed liquid large-cap stocks (see code). *Known limitation: not point-in-time → mild survivorship bias; acceptable for v1, revisit later.* |
| Opening range (OR) | High / low of 9:30–9:45 ET (first 15 minutes). |
| "In play" filter | OR-window volume > **1.5×** the stock's own trailing 14-day average OR-window volume. |
| Entry | First bar after 9:45 where price breaks the OR: above OR-high → long; below OR-low → short. One entry per symbol per day. No entries after 3:00 PM. |
| Stop | Opposite end of the OR (long → OR-low; short → OR-high). |
| Exit | Stop, or forced flatten at 3:50 PM ET. Nothing held overnight. |
| Sizing | **Risk-based:** risk 1% of equity per trade → shares = (1% × equity) ÷ OR-width. Capped at 25% of equity notional per position. |
| Limits | Max 5 concurrent positions. |

Three real knobs only: OR length (15 min), in-play multiple (1.5×), risk-per-trade (1%).
Everything else is structural. This is intentional — a minimal raw idea, no tuning yet.

---

## Cost model

A strategy is only real if it clears costs. The backtest applies:
- **Slippage:** `ConstantSlippageModel(0.0005)` = 0.05% per fill (breakout fills can slip).
- **Commissions:** the QC TradeStation brokerage model (≈$0 for US stocks).
- **Diagnostic A/B:** every test is also run with `SLIPPAGE = 0.0`. If edge exists at
  0.0 but vanishes at 0.05%, the "edge" was never real.

Structural advantage over the old strategy: ORB takes **at most one trade per symbol
per day**, not hundreds — so cost drag is a fraction of the churn strategy's.

---

## Train / test split — the discipline (non-negotiable)

- **Train (develop here):** 2016-01-01 → 2021-12-31 (6 years).
- **Holdout (locked):** 2022-01-01 → 2025-12-31 (4 years). **Run exactly once, at the end.**
- Do **not** tune parameters by looking at holdout results. If H1 is tuned on train
  and then collapses on holdout, H1 is dead — that is the test working, not a failure.
- Later: walk-forward across the train period for robustness.

---

## Success criteria — what "H1 has edge" means

H1 passes only if, on the **train** period:
1. Positive average P&L per trade, **net of the 0.05% cost model**.
2. Profit factor ≥ ~1.2 and a sane equity curve (not one lucky month).
3. Enough trades for significance (hundreds+).
4. The edge survives the stress checks (costs ×2; holds up across 2016–21 sub-periods).

…and then, on the **holdout**, the result is *directionally consistent* with train
(not a collapse). Only an H1 that clears both gets escalated. If it fails, it is
recorded as dead and we move to H2.

---

## Method / phases

1. **Run A** — train period, `SLIPPAGE = 0.0005`. (← next step)
2. **Run B** — train period, `SLIPPAGE = 0.0`. Compare: is the edge cost-driven?
3. If A shows no edge → **H1 is dead.** Log it, move to H2. Do not tune.
4. If A shows edge → stress tests (costs ×2, sub-period splits, symbol subsets).
5. If it survives → **one** holdout run (2022–2025).
6. If holdout confirms → propose it through the normal Alpha Quant gate
   (proposal → human approval → SIM → live). It does **not** touch the live bot
   before that.

---

## How AI is used here

Claude Code does the labour: writes/maintains the QC code, runs the analysis,
summarises results, proposes the next hypothesis. Claude does **not** get to
decide an idea "works" — the out-of-sample gate and the kill decisions are fixed
rules, not judgement calls. Overfitting is the enemy; the discipline above is the
defence.

---

## Status log

| Date | Entry |
|---|---|
| 2026-05-22 | Sub-project created. H1 (ORB) plan written. v1 QC code written: `strategy-research/orb_h1_backtest.py`. Next: Rhett pastes it into QC, runs the train period (Run A), sends results back. |
| 2026-05-22 | Recorded Rhett's goal/constraints (see section above). Handoff prepared for browser Claude to run Run A + Run B in QC. Awaiting results. |

*(append-only — newest at the bottom)*
