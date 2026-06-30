# TradeStation Margin & the 4×-Marginable Universe — Findings
*2026-06-30, Claude Code. For the live plan: $100k margin account, day-trade only (flat by EOD), only symbols leverageable 4×.*

## 1. What the account actually is (broker truth, SIM1623888M)
`/brokerage/accounts/SIM1623888M/balances` returns:
- `AccountType: Margin` ✓
- `BuyingPower 3,739,154` on `Equity 986,367` → **~4× day-trade buying power** (the SIM is over-funded vs the $100k live plan).
- `OvernightBuyingPower 1,774,975` → **~2×** (Reg-T overnight).
- `BalanceDetail.RequiredMargin 35,820` on `CostOfPositions 139,294` → **~25.7%** maintenance on current positions → consistent with a 25% (4×) day-trade rate.
- `DayTrades: 33`, `DayTradeExcess 934,980`.

**Implication for live:** a $100k margin account → **~$400k intraday buying power** (4×), ~$200k overnight (2×). This matches the project's existing `$400k DEPLOY_BASE` assumption. Day-trade-flat means we never use the 2× overnight tier.

## 2. The rules (TS published; note the 2026 rule change)
- **FINRA amended Rule 4210 effective 2026-06-04:** the **Pattern Day Trader framework and the $25,000 minimum are GONE**, replaced by an "Intraday Margin" standard. Now any margin account with **≥ $2,000 equity gets up to 4× Margin Excess intraday**; below $2,000 → 1×. Overnight = 2×. ($100k is far above the threshold → full 4×.)
- **Standard day-trade requirement = 25% of position value = 4× leverage** for ordinary marginable equities.
- **"TradeStation may impose a higher margin requirement and/or restrict trading to less than 4× for certain securities."** Those are the names we must EXCLUDE to keep a pure-4× universe.

## 3. Which symbols are NOT 4× (the exclusions)
- **Special Margin Requirements list** — symbols set higher than the 25% day-trade rate (e.g., **50% → 2×, 75% → 1.33×**) due to low liquidity / volatility / risk. TS publishes this in the HUB: `my.tradestation.com/lists/borrow-special-margin` (login-only).
- **Leveraged / inverse ETFs** (TQQQ, SQQQ, SOXL, SOXS, SPXL, SPXS, TNA, TZA, UVXY, UPRO, etc.) — increased requirements per FINRA Notice 09-53; typically on the special-margin list.
- **Hard-To-Borrow / halted** — already blocked both sides in `htb_filter` (and HTB names often carry special margin too).
- **Low-priced** (<$5; our universe floor is already $20, so this is covered).

## 4. The blocker: the TS API does NOT expose per-symbol margin
Verified three ways today:
- `/marketdata/symbols/{sym}` → only AssetType, Exchange, price/qty format. **No margin field.** (Also returns `AssetType: STOCK` for TQQQ — so AssetType can't even identify leveraged ETFs.)
- `/marketdata/quotes` `MarketFlags` → only `IsHardToBorrow / IsHalted / IsDelayed / IsBats`. **No margin/marginability flag.**
- `/orderexecution/orderconfirm` (dry-run preview) → only `EstimatedCost` (notional) + commission for standard names, leveraged ETFs, AND shorts. **No initial/maintenance margin returned.**

**Conclusion:** there is no API endpoint that says "this symbol is 4× / 2× / 1.33×." The Special Margin list is HUB-only (and not credential-fetchable by the bot under our no-credentials rule).

## 5. Recommended design — a DERIVED 4×-marginable universe (proposal, gated)
Since margin isn't in the API, build the 4× universe from signals we CAN get + maintained config lists:
1. **Common stock or non-leveraged ETF**, price **≥ $20**, liquid (existing `MIN_PRICE` / `MIN_VOLUME`). 
2. **Exclude HTB / halted** — already live (both sides).
3. **Exclude a maintained leveraged/inverse-ETF list** — config data (a few hundred well-known tickers), refreshed periodically.
4. **Exclude the TS Special Margin list** — Rhett (or a periodic manual export) pulls `my.tradestation.com/lists/borrow-special-margin` from the HUB; we load it as a dated config exclusion (watchlist-style, like the borrow list). This is the only fully-authoritative non-4× source, and it's manual by necessity.
5. **(Optional belt-and-suspenders) live margin sanity check** at order time: `RequiredMargin / notional ≈ 0.25` for 4× — but since order-confirm doesn't return margin, this can only be validated post-fill from balances, as a monitor not a gate.

This is a **WATCHED-path change** (universe / `symbol_universe.py` + the entry filters), so it goes through a proposal + your approval before it's wired in — not edited inline. The HTB-both-sides backstop is already live today.

## 6. Open question for Rhett (one)
Do you want the leveraged-ETF + Special-Margin exclusion to be (a) a hard universe filter (names never enter the candidate set), or (b) a final pre-arm gate (candidates can rank but are dropped before an order)? Recommendation: **(a) hard universe filter** — cleanest, and it keeps the ranking honest (no 2× names crowding the top-20 the way HTB names did this morning).
