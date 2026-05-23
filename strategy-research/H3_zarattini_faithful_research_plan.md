# Strategy Research — Hypothesis H3: Faithful Zarattini Stocks-in-Play ORB

**Sub-project:** Rebuild Alpha Quant's strategy layer on evidence.
**Created:** May 23, 2026 · **Lab:** QuantConnect
**Status:** PLAN + v1 CODE WRITTEN — awaiting train-period backtest.

Shared methodology (cost model, train/test discipline, success criteria) is in
`ORB_H1_research_plan.md`. Rhett's goal/risk constraints are also recorded there.
This doc covers only what is specific to H3.

---

## Why H3

The strategy hypothesis underlying H1 (ORB on stocks in play) is from the
Zarattini & Aziz SSRN paper *"A Profitable Day Trading Strategy For The U.S.
Equity Market"* (2024), which reports Sharpe ~2.81 over 2016–2023. **H1 was a
stripped-down test of that strategy class — not a faithful test of the paper.**
The differences are material (small fixed universe, weak "in play" filter,
OR-edge stops vs. ATR stops, 15-min vs. 5-min OR). H1 failing therefore does
not invalidate the strategy class; H3 is the actual test.

Rhett also (correctly) pushed back on:
- Backtesting only 36 mega-caps — the entire edge of "stocks in play" is *daily
  ranking against a broad universe*, which cannot be tested with 36 stocks.
- Not analysing the short side in bear markets — H3 will report long vs short
  P&L separately so the bear-market short claim is testable.

---

## Hypothesis H3 — what the paper claims, faithfully

> **On a broad U.S. equity universe (~1,000 liquid names), each day rank stocks
> by abnormal first-5-minute opening volume; trade the top 20 with a 5-minute
> opening-range breakout, ATR-based stops, and ATR-based position sizing; flat
> by end of day.**

Edge rationale: stocks with abnormal opening volume reflect overnight news /
institutional flow / catalysts. The opening-range break confirms direction.
The breadth of the universe and the daily ranking are *what makes the edge*,
not the breakout rule alone.

---

## Strategy — minimal faithful v1

| Element | Rule |
|---|---|
| Universe selection (daily) | Coarse: U.S. equities with fundamentals, price > $5, dollar volume > $10M. Take top 1,000 by dollar volume. |
| Per-symbol filters | ATR(14, daily) must be ready (effectively ~14 days of warm-up after a symbol enters the universe). |
| Opening range | First **5 minutes** (9:30–9:35 ET): track high, low, and cumulative volume per symbol. |
| Ranking | At 9:35 finalize. Compute relative volume = today's 5-min OR volume ÷ 14-day average of 5-min OR volume per symbol. Take **top 20** by relative volume. |
| Entry | After 9:35, for top-20 symbols not yet entered: long on break above OR-high, short on break below OR-low. One entry per symbol per day. No entries after 3:00 PM. |
| Stop | **ATR-based**: long stop = entry − 1.0 × ATR(14); short stop = entry + 1.0 × ATR(14). |
| Exit | Stop or forced flatten at 3:50 PM ET. Nothing overnight. |
| Sizing | Risk-based: shares = (1% × equity) ÷ (1.0 × ATR). Capped at 15% of equity notional per position. |
| Limits | Max 10 concurrent positions; total exposure capped at 1× equity (no leverage for the edge test — we add leverage only if the bare strategy has edge). |

Five real knobs: relative-volume rank cutoff (top 20), OR length (5 min),
ATR period (14), ATR stop multiple (1.0), risk per trade (1%). Nothing else.

---

## Cost model, train/test split, success criteria

Identical to the H1/H2 plans (see `ORB_H1_research_plan.md`):
- Train 2016-01-01 → 2021-12-31. **Holdout 2022 → present, locked, run once.**
- Run A: `SLIPPAGE = 0.0005`. Run B: `SLIPPAGE = 0.0`.
- Pass = positive expectancy **net of the 0.05% cost model**, profit factor
  ≥ ~1.2, sane equity curve, survives stress tests.
- The holdout now contains the **2022 bear market** — that's deliberate. A
  strategy that depends on a bull tape and dies in 2022 is not a strategy.

## What H3 additionally must report (per Rhett's questions)

- **Long P&L vs Short P&L, year by year.** If the short side doesn't
  contribute in 2022, that's a real problem to surface.
- **Worst-day distribution** (vs the $500/day reference). At research sizing
  the strategy will likely exceed $500/day swings; that's expected and will be
  resolved by sizing down later, not by tuning the strategy now.
- **Trade-count by year.** Should be in the hundreds-to-low-thousands per
  year — far more than H2 (a few hundred over six years), far less than the
  original Alpha Quant strategy (~150/day).

## Realistic expectations (calibration, not pessimism)

The paper reports Sharpe ~2.81. Public retail implementations of public
strategies almost never replicate those numbers, for three reasons documented
this session:
- Retail execution slippage that institutional backtests do not model
- ~50% post-publication alpha decay (McLean & Pontiff 2016 on 97 anomalies)
- Regime/microstructure changes between the paper's window and now

**Target to judge H3 against in our hands: Sharpe ≥ 1.0, 10–15% net annual.**
If H3 clears that — we've found something genuinely good. If it clears the
paper's 2.8 Sharpe — fantastic, but don't budget for it.

---

## Status log

| Date | Entry |
|---|---|
| 2026-05-23 | H3 plan + v1 QC code written. Code: `strategy-research/h3_zarattini_orb_backtest.py`. Next: run the train period in QC (Run A + Run B), send results back. |

*(append-only — newest at the bottom)*
