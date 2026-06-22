# HANDOFF → PLANNING CLAUDE — Incident: 140 weekend "phantom" order rejections

**From:** Claude Code (VPS) · **When:** 2026-06-22 Mon ~9:55 AM ET · **Trigger:** Rhett saw a massive number of rejected trades in the TS blotter (`TS 9 50 6 22.xlsx`).

## TL;DR
The 140 rejections are **weekend phantom orders**, not a failure of today's live session. The bot's **re-arm (multiscan) path is gated on holidays + time-of-day window but NOT on trading-day/weekend**, so on Sat 6/20 + Sun 6/21 it fired the hourly re-arm windows (10:35–14:35) and placed Day-duration StopLimit entry orders. TradeStation rejected every one with *"Only GTC/GTC+/GTD/GTD+ orders when markets are closed."* **Zero P&L / position impact** (all rejected, no fills, SIM). Today's real 9:35 session is healthy (5 filled, 3 open protected positions). **This is a pre-existing latent bug, NOT a regression from the Loop-121 strategy change.** Main real risk = **API hygiene** (weekend order/quote spam could throttle the TS key).

## Evidence (TS API `/brokerage/accounts/SIM1623888M/orders`, authoritative)
- 154 total orders: **140 REJ**, 10 ACK, 4 FLL.
- All 140 REJ: `RejectReason = "Only GTC/GTC+/GTD/GTD+ orders when markets are closed"`, `OrderType=StopLimit`, `Duration=DAY`.
- Timing (ET, from `OpenedDateTime`): **Sat 6/20 @ 10:35/11:35/12:35/13:35/14:35 (14 each = 70)** + **Sun 6/21 same windows (70)**. Exactly hourly on the :35 = the re-arm windows.
- Today's REAL orders all worked: 4 FLL @ 09:35–09:36, 10 ACK @ 09:35–09:47 (market open → accepted).
- Logged correctly: `broker_orders_unified.csv` has all 140 (70 on 6/20, 70 on 6/21). **No logging gap** (an earlier suspicion; disproven).
- Pre-existing: 6/07 (Sun) also shows weekend rejections (4). This weekend was larger only because run_bot ran continuously through both full weekend days (kept alive by the Sun verification restarts).

## Root cause (code-confirmed)
`tradestation-bot/orb_multiscan.py :: run_multiscan()`:
- line ~219: skips **holidays** (`market_hours.holiday_reason`).
- line ~224: skips if not in a re-arm **time window** (`current_window(now)`).
- **MISSING: a weekday / `is_regular_trading_day` gate.** Weekends are not "holidays," and the re-arm clock windows (10:35–14:35) exist on weekends, so `run_bot` (continuous, supervised) called `orb_multiscan --arm` each weekend hour and placed orders.
- Contrast: the 9:35 primary scan in `orb_runner.py` IS weekend-gated, which is why only the re-arm path leaked.

## Impact
- **P&L / positions: NONE** — every order rejected; no fills; SIM account.
- **API hygiene (the real concern):** ~140 order placements + the associated weekend quote scans hammer the TS API off-hours. Per CLAUDE.md rule 4, excessive API use risks key throttling/disablement; this is also a plausible contributor to Sunday's transient `TS_AUTH_FAIL` 500.
- **Noise:** 140 rejected orders clutter the blotter and alarmed Rhett on day 1.

## Secondary finding
CSHV `broker_order_rejections_recent` is **off-hours → SKIP**, so it did NOT alert on 140 weekend rejections — the detector was asleep exactly when the bug fired. A rejection BURST should be caught regardless of hours.

## Proposed fix (needs Planning + governance — `orb_multiscan.py` is a WATCHED strategy file)
1. **Primary:** add a trading-day gate at the top of `run_multiscan()` (mirror the 9:35 scan):
   `if not market_hours.is_regular_trading_day(now): return {"status": "non_trading_day"}`
   (fail-safe: only ARM on real trading days). Same gate belongs on any other order-placing path that currently checks only holiday+window.
2. **Defense in depth:** gate `run_bot`'s order-placing steps on `is_regular_trading_day` so nothing can place orders on a non-trading day even if a sub-path misses its own gate.
3. **Detector:** make CSHV `broker_order_rejections_recent` fire on a rejection burst even off-hours (or run weekends), so a recurrence alerts immediately.

## Governance / what I did NOT change
- I changed **nothing** — `orb_multiscan.py` is a WATCHED strategy-surface file and it's mid-session on day 1 of the Loop-121 change (freeze). This needs a proposal under `outputs/proposals/` + `manual_approvals.yaml` + human approval before deploy. The bug is **dormant until next weekend** (market open now → re-arm works correctly), so there is time to do it right. Recommend deploying the fix before Sat 6/27.

## Current live state (healthy)
3 open positions — ACN −162 (short, BuyToCover stop 136.5), FIX +8 (Sell stop 1885.16), ULTA +42 (Sell stop 445.36); 6 working entry orders; exit_bot_v2 monitoring OK; position recon OK; CSHV 0 FAIL.
