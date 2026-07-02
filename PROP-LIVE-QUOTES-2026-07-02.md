# PROP-LIVE-QUOTES-2026-07-02 — Live MARKET-DATA feed for quotes only (orders stay SIM)

**Status:** DRAFT — awaiting Rhett's explicit approval in `config/manual_approvals.yaml`. INACTIVE until approved. Rhett asked me to draft it (2026-07-02).

## The problem this solves
The Tape Watcher (live tick-level exit owner) streams quotes from the **SIM** market-data feed (`sim-api.tradestation.com/v3/marketdata/stream/quotes`). That feed is **coalesced** — it pushes a quote only when a field changes, and on quiet mid-caps that's every 15–30s between trade prints (AAPL smoke test: **1 quote in 10.3s**). So the TW cannot get a genuinely dense, every-print tick path no matter how well we tune it. Even the SIM-feed fixes (mid-price feed, etc.) are capped by the feed's coarseness. The **only** way to genuinely dense tick-level exit precision — and a real tape for the exit backtester — is the **live** market-data feed.

## The change (narrow, data-plane only)
Switch **ONLY the market-data (quote/bar) reads** to the live host `api.tradestation.com`, while **every order, position, balance, and account call stays on `sim-api.tradestation.com` (SIM1623888M)**. No order ever touches live. This does NOT change what account we trade — it changes where we read *prices* from.

## Hard guardrails (non-negotiable — this is what makes it safe)
1. **Config split by call type, enforced in code:** a `MARKET_DATA_BASE` (live) distinct from `BROKER_BASE` (SIM). Order/position/account/balance calls are HARD-WIRED to `BROKER_BASE`; a code guard + a regression test asserts no order path can ever resolve to the live host. If the split can't be proven, the feature stays off.
2. **SIM-only trading guards untouched:** the account still must start with `SIM`; the bot's safety stop, `environment: SIM_ONLY`, and `live_allowed: false` are unchanged. This proposal touches the DATA source, not the trading environment.
3. **Requires a live market-data entitlement** on the TradeStation account (real-time quotes subscription). Confirm before activating.
4. **Fail-safe to SIM data:** if the live market-data feed errors/times out, fall back to the SIM feed automatically — never block trading on a data-source outage.
5. **Separate token/scope** if live market data needs its own auth scope; never widen the order token's scope.

## Why it's worth it
- **Genuinely tick-level exits** — the TW finally sees the exact print that crosses the chandelier level, delivering the precision it's claimed to have (today it's ~a duplicate of the 30s poller).
- **A real tape for the backtester** — a dense every-trade price path (vs the SIM feed's coalesced quote-changes), which is the difference between a trustworthy exit backtest and a coarse one.

## Acceptance / rollout (before it goes live)
1. The code split proven: a test that every order/position/account URL resolves to the SIM host and every quote/bar URL to the live host; zero crossover.
2. Shadow-run the TW on the live feed (`fire=False`) alongside the SIM-feed owner for ≥1 full session; confirm denser ticks + diff the exit timing.
3. Fail-safe verified: kill the live feed mid-session in a test → the bot falls back to SIM data, keeps trading.
4. Then flip the market-data host with Rhett's recorded approval; orders remain SIM throughout.

## Out of scope
No change to the trading account, order routing, risk config, strategy, or the SIM-only trading guards. Quotes/bars only.
