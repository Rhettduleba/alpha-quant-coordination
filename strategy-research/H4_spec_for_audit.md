# H4 spec — standalone copy for external-AI audit

**This document is a derivative of `STRATEGY_LAB.md`.** It contains the H4
entry only, extracted so external AIs can be given a clean copy to audit
without anyone manually selecting lines from the master document. The
master record remains `STRATEGY_LAB.md` — any changes to H4 belong there,
and this file should be regenerated if the master changes.

**How to use this file:**
1. In a fresh ChatGPT (or other) chat, paste the H4 audit-task prompt
   first (from Rhett's chat with Claude Code, dated 2026-05-24).
2. Wait for ChatGPT to acknowledge.
3. Paste **everything below the horizontal rule** as the second message.
4. ChatGPT will return a paste-ready audit block; send it back to
   Claude Code to add to the master document.

---

## H4 — Faithful Zarattini ORB on Stocks in Play

**Status:** STAGE 1 (Exact Spec) — **awaiting external-AI spec audit (Stage 2)
before Claude Code writes any code.**
**Date spec created:** 2026-05-24

### Hypothesis (one falsifiable sentence + why it might be true)
> "On a broad universe of liquid U.S. stocks, the 20 stocks per day with
> highest first-5-minute relative volume are 'in play' on a catalyst, and a
> 5-minute opening-range breakout (long if the OR bar closed up, short if it
> closed down) generates positive expectancy when stopped with an ATR-based
> stop and held to market close."

Why it might be true: documented in Zarattini & Aziz (2024). Reported
Sharpe ~2.81 over 2016-2023 in the paper; QuantConnect's recreation
reports Sharpe ~2.396 for 2016 specifically.

### Source — direct citations

**Primary:** Zarattini, Carlo & Aziz, Andrew. "A Profitable Day Trading
Strategy For The U.S. Equity Market." SSRN paper 4729284 (2024).
Direct PDF text NOT fetched by Claude Code this session (SSRN 403'd
WebFetch). Spec below is built from the **QuantConnect research article
recreation** of the paper, with verbatim quotes from that article. **A
Stage 2 reviewer with access to the actual paper PDF should verify each
spec line against the paper before approval.**

**Secondary (the source actually quoted below):** QuantConnect Research
article, *"Opening Range Breakout for Stocks in Play"*, URL:
`https://www.quantconnect.com/research/18444/opening-range-breakout-for-stocks-in-play/`. Fetched by Claude Code on 2026-05-24.

### Exact spec (cite-marker per line)

Each spec line is marked with:
- **[QC]** = direct quote or close paraphrase from the QuantConnect article
- **[INFER]** = Claude Code's inference, needs Stage 2 verification
- **[OUR-ADD]** = required by our project's mandatory rules (G1/G2/etc.)

| Element | Value | Source |
|---|---|---|
| Universe size | "1,000 most liquid US Equities" | [QC] verbatim |
| Universe filter — price | "> $5/share" | [QC] verbatim |
| Universe filter — ATR | "ATR > $0.50" | [QC] verbatim (ATR period unspecified in quote; likely 14-day) |
| Universe filter — exchange | NYSE / NASDAQ listed | [INFER] standard for "liquid US Equities" |
| Universe filter — margin-eligible | Exclude leveraged ETFs (TQQQ, SOXL, SQQQ, etc.); listed ≥ 1 year | [OUR-ADD] required by our margin-universe rule |
| Daily ranking metric | Current-day first-5-min volume ÷ prior-14-day average first-5-min volume (= "relative volume") | [QC] verbatim |
| Tradeable set per day | Top **20** stocks by relative volume | [QC] verbatim |
| Opening range duration | First **5 minutes** of regular trading hours (9:30–9:35 ET) | [QC] verbatim |
| Direction filter | If OR bar's close > OR bar's open → look for LONG breakout only. If close < open → look for SHORT breakout only. If close = open → no trade. | [QC] verbatim |
| Long entry | Stop order at OR high. Fills when price breaks above. | [QC] verbatim |
| Short entry | Stop order at OR low. Fills when price breaks below. | [QC] verbatim |
| Stop loss formula | Entry price ± (14-day ATR × **multiplier**) | [QC] verbatim ("stop loss as a function of the entry price and the 14-day ATR") |
| Stop loss multiplier exact value | **UNKNOWN — Stage 2 must verify from paper.** Claude Code's guess based on standard ORB practice: 0.1× ATR (very tight). Could also be 1× ATR. Materially affects results. | [INFER] needs paper |
| Profit target | **None** — hold to market close | [QC] verbatim ("exit the position at close with a profit") |
| Holding period | Intraday only | [QC] |
| Exit time | Market close — paper exact time UNCLEAR. Our project default: 3:50 PM ET | [OUR-ADD] G1 |
| Position sizing | "Trade quantity set so that if stop loss is hit, we lose 1% of the portfolio value allocated to the asset" with "equal-weight cap" | [QC] verbatim |
| Risk per trade (derived) | 1% of equity (allocated to asset) per trade | [INFER] from quote — exact phrasing ambiguous |
| Equal-weight cap | 1/20 of portfolio per position = 5% notional cap | [INFER] from "equal-weight cap" given top-20 list |
| Max concurrent positions | 20 | [INFER] from top-20 |
| Daily loss cap (G2) | **$2,000** — if intraday P&L ≤ −$2,000, stop new entries, liquidate open positions, halt for the day | [OUR-ADD] required |
| EOD flatten (G1) | All positions liquidated by 3:50 PM ET | [OUR-ADD] required |
| Brokerage model | QC TradeStation, Margin account | [OUR-ADD] project standard |
| Slippage | `ConstantSlippageModel(0.0005)` = 0.05% per fill | [OUR-ADD] project standard |
| Backtest train window | 2016-01-01 to 2021-12-31 | [OUR-ADD] project standard |
| Backtest holdout (run later) | 2022-01-01 to present, **run once** | [OUR-ADD] project standard |
| Starting cash | $100,000 | [OUR-ADD] project standard |

### Constraints applied (vs mandatory rules) — REQUIRED for H4+
| Constraint | Applied? | Note |
|---|---|---|
| G1 — EOD flatten by 3:50 PM | **YES** | Will be coded |
| G2 — $2k daily loss cap | **YES** | Will be coded |
| Intraday-only | **YES** | Per paper, intraday-only by design |
| Margin-eligible universe | **YES** | Will exclude leveraged ETFs and require ≥1yr listed |

### Code reference
**TO BE BUILT in Stage 4 — after Stage 2 audit and Stage 3 approval.**

### Test runs
None yet (pre-code).

### AI commentary
- **Claude Code [2026-05-24]:** Spec built from the QuantConnect recreation,
  not the actual paper PDF (SSRN blocked WebFetch). **The single biggest
  open question is the ATR stop multiplier** — paper specifies a function
  of ATR but the QC quote doesn't give the exact multiplier. My H3 used
  1.0× ATR; standard ORB practice often uses 0.1× ATR. Difference is
  10×. A Stage 2 reviewer with paper access MUST resolve this before
  Stage 4 coding. Also worth verifying: exact wording of position
  sizing (does "1% of portfolio value allocated to the asset" mean 1%
  of equity or 1% of the allocation slice?) and the EOD flatten time
  (paper unclear; we default to 3:50 PM per G1).

### Decision
**Pending Stage 2 (external-AI spec audit) and Stage 3 (Rhett approval).**
