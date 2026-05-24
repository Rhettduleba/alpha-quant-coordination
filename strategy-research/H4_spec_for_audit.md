# H4 spec — STAGE 3 APPROVED (standalone copy)

**Status:** STAGE 3 APPROVED 2026-05-24 by Rhett. Stage 4 code being
written by Claude Code (`h4_zarattini_orb.py`).

**This document is a derivative of `STRATEGY_LAB.md`.** Master record is
in the lab doc — any future changes belong there first and this file
should be regenerated.

**How to use this file:**
- For second-opinion review (e.g., second AI auditor): paste the audit
  task prompt first, then paste everything below the horizontal rule.
- For final implementation reference: Claude Code's QC code must match
  every row in the spec table below.

---

## H4 — Faithful Zarattini ORB on Stocks in Play

**Status:** STAGE 3 APPROVED 2026-05-24 — Claude Code is writing Stage 4
code. Audit history below remains for reference.
**Date spec created:** 2026-05-24 · **Date Stage 2 audit completed:** 2026-05-24
· **Date Stage 3 approved:** 2026-05-24

### Hypothesis (one falsifiable sentence + why it might be true)
> "On a broad universe of liquid U.S. stocks, the 20 stocks per day with
> highest first-5-minute relative volume are 'in play' on a catalyst, and a
> 5-minute opening-range breakout (long if the OR bar closed up, short if it
> closed down) generates positive expectancy when stopped with an ATR-based
> stop and held to market close."

Why it might be true: documented in Zarattini & Aziz (2024). Reported
Sharpe ~2.81 over 2016-2023.

### Source — direct citations

**Primary:** Zarattini, Carlo & Aziz, Andrew. "A Profitable Day Trading
Strategy For The U.S. Equity Market." SSRN paper 4729284 (2024).
**Spec values below were verified against the paper by three independent
audits on 2026-05-24:** ChatGPT GPT-5.5, Base44, and Claude Opus 4.7
(the latter with direct paper-PDF citations from wealth-lab.com mirror).
Full audit text preserved in the master `STRATEGY_LAB.md` H4 entry.

### Exact spec — STAGE 3 APPROVED 2026-05-24

Cite-markers:
- **[PAPER]** = verified from Zarattini & Aziz (2024) paper PDF.
- **[QC-IMPL-CHOICE]** = from the QuantConnect research article
  recreation, used by us where the paper's wording leaves an open
  interpretation.
- **[OUR-ADD]** = project-specific addition (G1/G2/margin-universe,
  TradeStation broker, conservative price floor) or deliberate
  deviation from paper. **Reviewers and code must treat these as our
  additions, not as paper-faithful.**

| Element | Value | Source |
|---|---|---|
| Universe — base | All equities listed on US exchanges (NYSE + NASDAQ) — "approximately 7,000 stocks" | [PAPER] verbatim |
| Universe filter — opening price | **> $7** (paper says >$5; lab uses $7 as a conservative marginability buffer) | [PAPER] + **[OUR-ADD deviation]** — Stage 3 decision 2026-05-24 |
| Universe filter — 14-day avg volume | ≥ **1,000,000 shares/day** (previous 14-day average) | [PAPER] |
| Universe filter — 14-day ATR | > $0.50 (previous 14-day ATR, Wilder) | [PAPER] |
| Universe filter — Relative Volume | ≥ 100% (current-day first-5-min volume ≥ prior-14-day avg first-5-min volume) | [PAPER] |
| Universe filter — exclude leveraged ETFs (TQQQ, SOXL, SQQQ, etc.); listed ≥ 1 year | Excluded | **[OUR-ADD]** — required by our margin-universe rule, NOT in paper |
| Survivorship-bias-free universe | Required — paper p.6 | [PAPER] — Stage 4 must verify QC's universe includes delisted stocks |
| Daily ranking metric | Relative Volume = current-day first-5-min volume ÷ prior-14-day average first-5-min volume | [PAPER] |
| Tradeable set per day | Top **20** by Relative Volume | [PAPER] |
| Opening range duration | First **5 minutes** of regular trading hours (9:30–9:35 ET) | [PAPER] |
| Direction filter | First 5-min OR bar bullish (close > open) → LONG breakout only. Bearish (close < open) → SHORT breakout only. Doji (close = open) → no trade. | [PAPER] verbatim |
| Long entry | Stop order at OR high. Fills when price breaks above. | [PAPER] |
| Short entry | Stop order at OR low. Fills when price breaks below. | [PAPER] |
| Stop loss multiplier | **0.10 × 14-day ATR** from entry price | [PAPER] verbatim — paper p.6, p.8, p.15 |
| Stop loss formula | Long stop = entry − (0.10 × 14-day ATR). Short stop = entry + (0.10 × 14-day ATR). | [PAPER] |
| Profit target | None — hold to market close | [PAPER] |
| Exit time (paper) | 4:00 PM ET — "If the stop loss was not reached intraday, we closed the position at the end of the trading session (i.e., 4:00 pm ET)." | [PAPER] verbatim |
| Exit time (lab override, G1) | **3:50 PM ET** — 10 minutes earlier than the paper, for project G1 safety. | **[OUR-ADD]** — DEVIATION FROM PAPER, clearly labeled. |
| Position sizing — risk basis | Risk is computed against the **capital allocated to that position**, NOT total equity | [PAPER] verbatim: "the loss on the capital allocated to that position would not exceed 1%" |
| Position sizing — allocation slice | **Equal-weight: equity ÷ 20 per position = $5,000 (at $100k equity)**. Stage 3 decision: QC-recreation interpretation chosen because Claude-Opus's alternative $20k-slice reading produces 20×$200=$4,000 worst-case daily loss, breaching G2 ($2k cap). | **[QC-IMPL-CHOICE / OUR-ADD]** — Stage 3 decision 2026-05-24 |
| Position sizing — max loss per position | 1% of allocation slice = **$50** = 0.05% of total equity per position. 20×$50 = $1,000 worst-case daily loss, under G2. | derived [QC-IMPL-CHOICE / OUR-ADD] |
| Position sizing — share formula | shares = (allocation_slice × 0.01) ÷ (0.10 × ATR), capped by account leverage AND per-position leverage cap (safeguard) | derived from [PAPER] formula with [QC-IMPL-CHOICE] slice |
| Max concurrent positions | 20 | [PAPER] (top-20) |
| Max leverage (account-wide) | **4×** total deployed not to exceed (FINRA intraday) | [PAPER] p.9 |
| Per-position leverage cap (safeguard) | A single position cannot consume > (4× / 20) ≈ 0.2× equity of buying power on its own — prevents one tight-ATR high-price ticker from eating the entire leverage budget | **[OUR-ADD safeguard]** — Stage 3 decision 2026-05-24 |
| Daily loss cap (G2) | **$2,000** — if intraday P&L ≤ −$2,000, halt new entries, liquidate, halt for the day | **[OUR-ADD]** required by project; NOT in paper |
| Brokerage model | QC TradeStation, Margin account | **[OUR-ADD]** project standard |
| Slippage | `ConstantSlippageModel(0.00025)` = **0.025% (2.5 bps) per fill** — Stage 3 decision: Rhett's live TS fill experience on liquid (ADV≥1M) names supports 2.5 bps. Sensitivity re-run at 5 bps will follow base run as a diagnostic. | **[OUR-ADD]** — Stage 3 decision 2026-05-24 |
| Commission (paper) | $0.0035/share (Interactive Brokers Pro Tiered, EOY 2023 fee schedule) | [PAPER] p.9 |
| Commission (lab) | **$0** (TradeStation commission-free for stocks since 2019). Our backtest will be more optimistic than paper's by the commission amount per share — labeled, not hidden. | **[OUR-ADD]** — Stage 3 decision 2026-05-24 |
| Data adjustment (paper) | UNADJUSTED intraday data (p.7: "intraday data remained unadjusted for stock splits or dividends") | [PAPER] |
| Data adjustment (lab) | QC default = ADJUSTED. Stage 4 code will verify the effect on intraday OR calculations on split days; likely fine for within-day, may distort 14-day ATR/volume on split days. | **[OUR-ADD / VERIFY in Stage 4]** |
| Diagnostic logging (safeguard) | Daily log: universe-candidate count, top-20 selected, breakouts triggered, stop-outs, held-to-close. So result anomalies can be debugged, not guessed. | **[OUR-ADD safeguard]** — Stage 3 decision 2026-05-24 |
| Backtest train window | 2016-01-01 to 2021-12-31 | **[OUR-ADD]** project standard |
| Backtest holdout (run later) | 2022-01-01 to present, **run once** | **[OUR-ADD]** project standard |
| Starting cash | $100,000 | **[OUR-ADD]** project standard ($300k actual scaled down for the lab) |

### Constraints applied (vs mandatory rules) — REQUIRED for H4+
| Constraint | Applied? | Note |
|---|---|---|
| G1 — EOD flatten by 3:50 PM | **YES** | 10 min earlier than paper's 4:00 PM (labeled deviation) |
| G2 — $2k daily loss cap | **YES** | Not in paper, project requirement |
| Intraday-only | **YES** | Per paper, intraday-only by design |
| Margin-eligible universe | **YES** | Excludes leveraged ETFs; requires ≥1yr listed; $7 price floor |

### Code reference
`strategy-research/h4_zarattini_orb.py` — being written in Stage 4.

### Test runs
None yet — Stage 4 in progress, Stage 5 (backtest) is next.

### Stage 3 final auditor decisions (Claude Code, 2026-05-24)

Per Rhett's audit-protocol clarification (external AIs propose+audit;
Claude Code is final auditor and recommender), the open interpretive
questions from the three audits were resolved as follows:

1. **Position sizing slice = $5k / $50 risk per position** — G2-mandated.
   Alternative $20k slice yields worst-case −$4k/day, breaching the $2k cap.
2. **Universe = strict ~7,000 paper-faithful** — top-1500 cap would muddle
   the paper-faithfulness test; ~2hr backtests are acceptable.
3. **Commission = TradeStation $0** — our actual broker reality; paper's
   edge survived $0.0035/share so $0 only helps; labeled [OUR-ADD deviation].
4. **Price floor = $7** — one notch above paper's $5 for marginability buffer;
   labeled [OUR-ADD deviation]. Catches the most fragile names without
   materially changing strategy character.
5. **Slippage = 2.5 bps** — Rhett's live TS fill experience overrides Claude
   Code's theoretical 5 bps pessimism. Sensitivity re-run at 5 bps will
   follow the base run as a diagnostic.

Safeguards added beyond spec: diagnostic logging + per-position leverage cap.

Pre-committed interpretation guard: if H4 lands at Sharpe ~1.5 vs paper's
2.81, slippage friction on tight 0.10×ATR stops with 20 round-trips/day is
the most likely cause — direction matters more than absolute Sharpe.
