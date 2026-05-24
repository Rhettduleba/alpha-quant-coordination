# H4 spec — REVISED post-audit (standalone copy)

**Status:** STAGE 2 COMPLETE. Spec has been revised based on ChatGPT
GPT-5.5 audit findings (2026-05-24) with direct paper quotes. Currently
awaiting Stage 3 (Rhett approval) before Stage 4 (Claude Code writes code).

**This document is a derivative of `STRATEGY_LAB.md`.** Master record is
in the lab doc — any future changes belong there first and this file
should be regenerated.

**How to use this file:**
- For second-opinion review (e.g., second AI auditor): paste the audit
  task prompt first, then paste everything below the horizontal rule.
- For Rhett's Stage 3 review: read the spec below; if approved, tell
  Claude Code "approved, write code."

---

## H4 — Faithful Zarattini ORB on Stocks in Play

**Status:** STAGE 2 COMPLETE (external audit by ChatGPT GPT-5.5 on
2026-05-24 returned verified paper values + REVISE verdict; spec has
been revised below) — **awaiting Stage 3 (Rhett approval) before Claude
Code writes any code.**
**Date spec created:** 2026-05-24 · **Date Stage 2 audit completed:**
2026-05-24

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
**Spec values below were verified against the paper by ChatGPT GPT-5.5
on 2026-05-24, with direct paper quotes preserved in the AI commentary
section at the bottom.**

### Exact spec — REVISED post-audit 2026-05-24

Cite-markers:
- **[PAPER]** = verified from Zarattini & Aziz (2024) paper PDF via
  ChatGPT GPT-5.5 audit on 2026-05-24, with direct paper quotes
  attached in AI commentary section.
- **[QC]** = from the QuantConnect research article recreation (not the
  paper itself)
- **[OUR-ADD]** = project-specific addition (G1/G2/margin-universe) or
  deliberate deviation from paper. **Reviewers and code must treat
  these as our additions, not as paper-faithful.**

| Element | Value | Source |
|---|---|---|
| Universe — base | All equities listed on US exchanges (NYSE + NASDAQ) — "approximately 7,000 stocks" | [PAPER] verbatim |
| Universe filter — opening price | > $5 | [PAPER] |
| Universe filter — 14-day avg volume | ≥ **1,000,000 shares/day** (previous 14-day average) | [PAPER] — Claude Code had MISSED this filter in Stage 1 |
| Universe filter — 14-day ATR | > $0.50 (previous 14-day ATR) | [PAPER] |
| Universe filter — Relative Volume | ≥ 100% (current-day first-5-min volume ≥ prior-14-day avg first-5-min volume) | [PAPER] |
| Universe filter — exclude leveraged ETFs (TQQQ, SOXL, SQQQ, etc.); listed ≥ 1 year | Excluded | **[OUR-ADD]** — required by our margin-universe rule, NOT in paper |
| Daily ranking metric | Relative Volume = current-day first-5-min volume ÷ prior-14-day average first-5-min volume | [PAPER] |
| Tradeable set per day | Top **20** by Relative Volume | [PAPER] |
| Opening range duration | First **5 minutes** of regular trading hours (9:30–9:35 ET) | [PAPER] |
| Direction filter | First 5-min OR bar bullish (close > open) → LONG breakout only. Bearish (close < open) → SHORT breakout only. Doji (close = open) → no trade. | [PAPER] verbatim |
| Long entry | Stop order at OR high. Fills when price breaks above. | [PAPER] |
| Short entry | Stop order at OR low. Fills when price breaks below. | [PAPER] |
| Stop loss multiplier | **0.10 × 14-day ATR** from entry price | [PAPER] verbatim — verified by audit |
| Stop loss formula | Long stop = entry − (0.10 × 14-day ATR). Short stop = entry + (0.10 × 14-day ATR). | [PAPER] |
| Profit target | None — hold to market close | [PAPER] |
| Exit time (paper) | 4:00 PM ET — "If the stop loss was not reached intraday, we closed the position at the end of the trading session (i.e., 4:00 pm ET)." | [PAPER] verbatim |
| Exit time (lab override, G1) | **3:50 PM ET** — 10 minutes earlier than the paper, for project G1 safety. | **[OUR-ADD]** — DEVIATION FROM PAPER, clearly labeled. |
| Position sizing — risk basis | Risk is computed against the **capital allocated to that position**, NOT total equity | [PAPER] verbatim: "the loss on the capital allocated to that position would not exceed 1%" |
| Position sizing — allocation slice | Equal-weight: equity ÷ 20 per position | [PAPER] (top-20 + equal-weight) / [QC] recreation pattern |
| Position sizing — max loss per position | 1% of allocation slice = 0.05% of total equity per position | [PAPER] |
| Position sizing — share formula | shares = (allocation_slice × 0.01) ÷ (0.10 × ATR), capped by leverage | derived from [PAPER] |
| Max concurrent positions | 20 | [PAPER] (top-20) |
| Max leverage (account-wide) | **4×** total deployed not to exceed | [PAPER] mentioned + matches Rhett's TradeStation 4× intraday margin |
| Daily loss cap (G2) | **$2,000** — if intraday P&L ≤ −$2,000, halt new entries, liquidate, halt for the day | **[OUR-ADD]** required by project; NOT in paper |
| Brokerage model | QC TradeStation, Margin account | **[OUR-ADD]** project standard |
| Slippage | `ConstantSlippageModel(0.0005)` = 0.05% per fill | **[OUR-ADD]** project standard |
| Backtest train window | 2016-01-01 to 2021-12-31 | **[OUR-ADD]** project standard |
| Backtest holdout (run later) | 2022-01-01 to present, **run once** | **[OUR-ADD]** project standard |
| Starting cash | $100,000 | **[OUR-ADD]** project standard ($300k actual scaled down for the lab) |

### Constraints applied (vs mandatory rules) — REQUIRED for H4+
| Constraint | Applied? | Note |
|---|---|---|
| G1 — EOD flatten by 3:50 PM | **YES** | Will be coded; 10 min earlier than paper's 4:00 PM (labeled deviation) |
| G2 — $2k daily loss cap | **YES** | Will be coded; not in paper, project requirement |
| Intraday-only | **YES** | Per paper, intraday-only by design |
| Margin-eligible universe | **YES** | Will exclude leveraged ETFs and require ≥1yr listed; not in paper, project requirement |

### Code reference
**TO BE BUILT in Stage 4 — after Stage 3 approval.**

### Test runs
None yet (pre-code).

### Audit trail (ChatGPT GPT-5.5, 2026-05-24)

The Stage 2 audit by ChatGPT GPT-5.5 provided direct paper quotes for
each questioned spec element. Full quotes preserved in the master
`STRATEGY_LAB.md` H4 entry's AI commentary section.

**Audit verdict: REVISE before Stage 3** — all six findings now
incorporated above.
