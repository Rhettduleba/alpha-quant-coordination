# Strategy Research — Hypothesis H2: Intraday Gap Continuation

**Sub-project:** Rebuild Alpha Quant's strategy layer on evidence.
**Created:** May 22, 2026 · **Lab:** QuantConnect
**Status:** H2 TESTED — **FAILED** the train-period net-of-costs gate (near miss; real small gross edge present). See status log.

Shared methodology — goal & risk constraints, cost model, train/test split,
success criteria, how AI is used — is in `ORB_H1_research_plan.md`. This file
covers only what is specific to H2.

---

## Why H2 (what H1 taught us)

H1 (Opening Range Breakout) failed: ~zero gross edge across ~10,000 trades,
killed by transaction costs. Two strategies have now died the same way (the
original Alpha Quant strategy and H1). H2 is designed to attack that root cause
directly: **trade rarely, only on a genuine catalyst**, so cost drag stops being
the killer. Rhett chose to stay intraday.

---

## Hypothesis H2

> **On liquid US large-cap stocks, when a stock gaps sharply at the open (≥4%
> versus the prior close — a sign of a real overnight catalyst such as earnings
> or news) AND holds that gap through the first 15 minutes, the move tends to
> continue in the gap direction through the rest of the session.**

**Edge rationale:** this is the intraday slice of *post-earnings-announcement
drift* — one of the most robustly documented anomalies in finance. Investors
digest a large overnight surprise gradually, so price drifts in the surprise
direction. Crucially, large gaps are uncommon — so this strategy trades a
handful of times per week, not hundreds per day, which structurally removes the
cost problem that killed H1.

---

## The strategy — minimal v1

| Element | Rule |
|---|---|
| Universe | The same 36 liquid large-cap stocks used in H1 (comparability). |
| Catalyst filter | Overnight gap = (today's open − prior close) / prior close. Trade only if **\|gap\| ≥ 4%**. |
| Confirmation | At 9:45 ET, the stock must still be holding the gap: price ≥ open for an up-gap, price ≤ open for a down-gap. |
| Entry | One decision per stock per day, made at 9:45. Enter in the gap direction. If more than 5 stocks qualify, take the biggest gaps first (max 5 positions). No entries after 3:00 PM. |
| Stop | Opposite end of the first-15-minute range (long → 15-min low; short → 15-min high). If continuation fails and price breaks back through that range, exit. |
| Exit | Stop, or forced flatten at 3:50 PM ET. Nothing held overnight. |
| Sizing | Risk-based: risk 1% of equity per trade; capped at 25% of equity notional per position. |

Three knobs only: gap threshold (4%), stop reference (first-15-min range),
risk per trade (1%). Everything else is structural — no tuning.

---

## Cost model, train/test split, success criteria

Identical to the H1 plan (see `ORB_H1_research_plan.md`):
- Train 2016-01-01 → 2021-12-31. Holdout 2022 → present, locked, run once.
- Run A: `SLIPPAGE = 0.0005`. Run B: `SLIPPAGE = 0.0`.
- Pass = positive expectancy **net of the 0.05% cost model**, profit factor
  ≥ ~1.2, a sane equity curve, survives stress tests, and a holdout result
  consistent with train.

**H2-specific caveat:** because big gaps are rare, H2 will produce far fewer
trades than H1 — likely a few hundred over 6 years, not 10,000. Fewer trades is
good for costs but means **weaker statistical significance**. If the trade count
is small, a positive result is suggestive, not conclusive, and a later version
would widen the universe to gather more setups before trusting it.

---

## Status log

| Date | Entry |
|---|---|
| 2026-05-22 | H2 (gap continuation) plan + v1 QC code written, after H1 failed the train gate. Code: `strategy-research/h2_gap_continuation_backtest.py`. Next: run the train period in QC (Run A + Run B), send results back. |
| 2026-05-22 | H2 Run A errored in QC: `'GapContinuation_H2' object has no attribute '_reset_day'`. Verified the committed file defines and calls `_reset_day` consistently and H1 used the same pattern fine — so the code was altered in transit (browser-Claude transcription), not a code bug. Fixed defensively (H2 v2): removed the `_reset_day` helper method, inlined its 5 lines into `initialize` and the day-rollover. Class now has only `initialize` / `on_data` / `on_end_of_algorithm` — no helper-method name a paste error can mismatch. Re-handoff issued. |
| 2026-05-22 | **H2 RESULT — train period 2016–2021 (QC project H2-GapCont-v2).** Run A (0.05% slippage): −5.7%, end equity $94,269, win rate 42%, P/L ratio 1.27, expectancy −0.038, 608 orders, max DD 20.1%. Run B (0% slippage): +1.5%, end equity $101,546, win rate 44%, P/L ratio 1.32, expectancy +0.016, 608 orders, max DD 16.1%. **Verdict: H2 FAILS the net-of-costs gate** (Run A expectancy negative). BUT — a real, small *gross* edge exists (Run B positive, where H1 was zero). The catalyst filter is doing genuine work; H2 trades ~16× less than H1, cost drag fell from 68pp to 7pp. 2020 COVID is in the data; long AND short setups are coded; the strategy LOST during COVID despite short-side access (a finding — gap-down "continuations" in 2020 evidently didn't continue cleanly enough, or stops were knocked out by volatility). Holdout NOT run (didn't pass train). Cumulative: 3 strategies (Alpha Quant −99.9%, H1 −72%, H2 −5.7%); trend is clearly improving as the signal becomes more selective, but no winner yet. Next: Rhett's call — pull long/short breakdown from QC (diagnostic), design H3, or change direction. |
| 2026-05-22 | Rhett chose a multi-stage path: **(1)** diagnose H2 by pulling its long-side vs short-side P&L from the existing QC report (no new backtest); **(2)** then H3a — stricter catalyst (gap threshold 5–6%); **(3)** then H3b — profit-target exit variant of H2. Stage 1 handoff issued — read the existing H2-GapCont-v2 results, not a re-run. |

*(append-only — newest at the bottom)*
