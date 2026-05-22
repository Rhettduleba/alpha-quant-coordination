# Alpha Quant — Verified Strategy Specification

*Extracted directly from the bot's source code on May 22, 2026. This is the source of truth for the QuantConnect backtest translation. Every constant below was read from the actual files — `entry_signals.py`, `bot_loop.py`, `short_bot.py`, `exit_bot_v2.py`, `symbol_universe.py`, `market_hours.py`, `run_bot.py`, `risk_config.py` — not paraphrased from memory.*

**Why this document exists:** the browser-Claude QuantConnect handoff described the strategy from memory and got it materially wrong (see §11). Build the QC algorithm from THIS spec, not that handoff.

---

## 1. What the bot is

An intraday momentum day-trader. It scans a symbol universe, scores each symbol, takes the best long and the best short, manages exits with tiered trailing stops, and flattens everything before the close. It holds nothing overnight.

Long entries and short entries are **two separate programs** (`bot_loop.py`, `short_bot.py`) that run independently and concurrently. Exits are a third program (`exit_bot_v2.py`). All three are relaunched every **15 seconds** by `run_bot.py` (`LOOP_SECONDS = 15`).

## 2. The cycle

Every 15 seconds, for the long side and (separately) the short side:

1. Skip entirely if outside regular trading hours (9:30 AM–4:00 PM ET).
2. Skip new entries if a daily shutdown is active (set when the daily loss limit was hit earlier today).
3. Skip new entries after the **entry cutoff: 3:50 PM ET** (`ENTRY_CUTOFF_HOUR/MINUTE = 15:50`).
4. Daily loss guard — if today's P&L ≤ −$10,000, trigger shutdown for the rest of the day.
5. Skip if 4 positions are already open, or total exposure ≥ $100,000.
6. Compute the volatility regime (§5).
7. Scan the universe, score every symbol, rank, place at most ONE order this cycle (§6).

Exits run on their own 15-second cycle (§7). A forced flatten of all positions happens at **3:50 PM ET** (`FORCED_FLATTEN = 15:50`).

> **Backtest cadence:** evaluate once per 1-minute bar. The live bot runs every ~15 s, but 1-minute bars are the finest historical data available — the backtest will see fewer decision points than the live bot. Document this as a known fidelity limitation.

## 3. Universe

- The bot scans whatever the Research Brain publishes in `advisor_universe_latest.json` — currently **~150 scored symbols** — falling back to a hardcoded 34-symbol `CORE_UNIVERSE` if that file is missing/invalid.
- For the backtest: use the current ~150-symbol list (it can be extracted from the live file). **Note the survivorship caveat** — that list is today's universe; applying it to 2021–2025 history is survivorship-biased. Acceptable for a first pass if disclosed.

## 4. Entry scoring (the REAL formulas — from `entry_signals.py`)

Composite score, range 0.0–1.0. Weights: **momentum 0.35, volume 0.25, spread quality 0.20, price action 0.20.**
A symbol is a valid candidate only if **composite ≥ 0.40 AND all hard filters pass.**

Inputs are a quote snapshot: `last` price, `net_change_pct` (% change vs **prior day's close**), day `volume`, `spread` (ask−bid), day `open`, prior-day `close`.

**Momentum (long):** `clamp(net_change_pct / 2.5, 0, 1)`; `0` if `net_change_pct ≤ 0`.
**Momentum (short):** `clamp(abs(net_change_pct) / 2.5, 0, 1)`; `0` if `net_change_pct ≥ 0`.

**Volume:** `ratio = volume / min_volume`. If `ratio ≥ 3` → `1.0`; if `ratio ≥ 1` → `(ratio − 1) / 2`; else `0`.

**Spread quality:** if `spread ≤ 0` → `1.0`; if `spread ≥ max_spread` → `0`; else `1 − (spread / max_spread)`.

**Price action (long):** start `0.5`. If `last > open`: `+clamp(((last−open)/open*100) / 2, 0, 0.3)`. Elif `last < open`: `−0.2`. If `last > prev_close`: `+0.2`. Clamp to `[0,1]`.
**Price action (short):** start `0.5`. If `last < open`: `+clamp(((open−last)/open*100) / 2, 0, 0.3)`. Elif `last > open`: `−0.2`. If `last < prev_close`: `+0.2`. Clamp to `[0,1]`.

### Hard filters — LONG (`bot_loop.py` values)
- `last ≥ $20`
- `net_change_pct ≥ 0.25%` *(this is a hard filter — the browser handoff omitted it)*
- `volume ≥ 500,000`
- `spread ≤ $0.25`

### Hard filters — SHORT (`short_bot.py` values — note: stricter than long)
- `last ≥ $20`
- `net_change_pct ≤ −0.60%`
- `volume ≥ 1,000,000`
- `spread ≤ $0.15`
- price below the day's open by ≥ `0.20%`
- price below prior close by ≥ `0.20%`

## 5. Volatility regime (the "VIX proxy" — browser handoff omitted this entirely)

Each cycle, compute SPY's intraday range: `(SPY_high − SPY_low) / SPY_prev_close × 100`.
- `≥ 4.0%` → **EXTREME**: block ALL new entries (long and short) this cycle.
- `≥ 2.5%` → **HIGH**: tighten filters — `max_spread × 0.7`, `min_volume × 1.5`, and the min-change bar ×1.5.
- else → **NORMAL**: filters as in §4.

The backtest needs SPY minute bars to compute this.

## 6. Candidate selection & position sizing

- Score every eligible symbol; drop any already held, with a working order, or inside a 15-minute re-entry cooldown.
- Rank passing candidates by composite score, descending.
- Walk the ranked list; for each, check the **sector cap** (max 2 open positions per sector group; ETFs `SPY`/`QQQ`/`IWM` and "OTHER" are exempt) and exposure. Place the first one that passes. **One order per cycle per side.**
- **Sizing:** `MAX_POSITION_DOLLARS = STRATEGY_CAPITAL × 0.25`, where `STRATEGY_CAPITAL` is account equity capped at $100,000. Long quantity = `int(MAX_POSITION_DOLLARS // limit_price)`. Short quantity = `int(MAX_POSITION_DOLLARS // last)`.
- **Order price:** long limit = `round(last + 0.10, 2)`; short limit = `round(last − 0.10, 2)`. Order type: DAY limit.
- Sector groups (`symbol_universe.py`): MEGA_TECH, SEMIS, GROWTH_TECH, FINANCE, HEALTHCARE, CONSUMER, ENERGY, INDUSTRIAL, plus per-ETF categories. For brain-universe symbols not in the hardcoded map, the sector comes from the universe file.

## 7. Exit engine (the REAL logic — from `exit_bot_v2.py`; browser handoff implemented NONE of this)

Every 15 s, for each open position. While a position is held, track the running **high** (longs) / **low** (shorts) of observed price.

`profit_pct` (long) = `(last − avg) / avg × 100`. (short: `(avg − last) / avg × 100`.)

**Hard stop:** long exits if `last ≤ avg × (1 − 0.50/100)`; short exits if `last ≥ avg × (1 + 0.50/100)`.

**Tiered trailing stop** (long; mirror for short):
- `profit_pct ≥ 1.50%` → trail = `high × (1 − 0.03/100)`  *(TIER3)*
- `profit_pct ≥ 0.75%` → trail = `high × (1 − 0.05/100)`  *(TIER2)*
- `profit_pct ≥ 0.20%` → trail = `high × (1 − 0.08/100)`  *(TIER1)*
- else → no trailing stop active

**Breakeven lock:** once `profit_pct ≥ 0.40%`, `breakeven_stop = avg × (1 + 0.05/100)`.

**Exit check order (long):** exit if `last ≤ hard_stop`; else if breakeven active and `last ≤ breakeven_stop`; else if trail active and `last ≤ trail_stop`. (Short: mirror with `≥`.)

These stops are *tiny* (0.5% hard, 0.03–0.08% trail). The strategy's character lives here as much as in the entry.

**EOD:** all positions flattened at 3:50 PM ET regardless.

> **Backtest modeling note:** track the running high/low from 1-minute bar values. Using the bar *high/low* vs. the bar *close* changes when stops trigger — pick one, document it, and ideally test sensitivity to it.

## 8. Risk floors

| Constant | Value |
|---|---|
| Daily max loss (full halt for the day) | $10,000 |
| Max open positions | 4 (long + short combined) |
| Max position size | 25% of equity |
| Max total exposure | $100,000 |
| Re-entry cooldown per symbol | 15 minutes |
| Starting capital for the backtest | $100,000 |

## 9. Explicitly OUT of the backtest

- **The advisor.** The live bot also consults a Claude-driven advisor that can block symbols / shrink size. The advisor did not exist over 2021–2025 and simulating it is impractical. The backtest tests the **bare mechanical strategy**, with no advisor overlay. State this on every result.
- The brain's daily universe re-selection — use one fixed universe for the whole backtest.

## 10. Fidelity gaps to disclose on every backtest result

1. **Spread is not in historical bars.** The bot scores and filters on bid-ask spread; minute bars are OHLCV only. The backtest must approximate spread (e.g. a fixed assumption) or drop that filter — either way it tests a slightly different bot. Apply a conservative slippage model to compensate.
2. **Fill modeling.** The bot places limit orders; the backtest must assume whether/at what price they fill.
3. **Intra-bar path unknown.** With 1-minute bars you don't know whether the high or low came first — affects which stop triggers.
4. **SIM ≠ live.** This is, at best, SIM-grade truth; not a live-fill guarantee.
5. **Survivorship** in the fixed universe (§3).

## 11. Corrections vs. the browser-Claude QC handoff

| Browser-Claude handoff said | Verified reality |
|---|---|
| Momentum = multi-timeframe rate-of-change scaled by volatility | `net_change_pct / 2.5`, clamped. Single input. |
| Volume = vs. recent average | vs. a **fixed** threshold (500k long / 1M short) |
| Price action = position in recent high-low range | vs. the day's **open** and **prior close** |
| Min composite score `0.55` | **`0.40`** |
| Scan every 15 minutes | Every **15 seconds** |
| Hard filters list | **Omitted** the `net_change_pct` filter; omitted all short-side thresholds |
| Exits: "trailing + hard stop" — code implemented neither | Tiered trailing (0.08/0.05/0.03%) + breakeven lock (0.40% trigger) + 0.50% hard stop |
| (no mention) | **Omitted the volatility-regime gate entirely** |
| EOD flatten / cutoff 3:50–3:55 PM | Both are **3:50 PM ET** |

---

*Honest baseline this backtest must be checked against: 593 closed trades, −$2,282 net over 22 SIM trading days (broker truth). Edge is unproven.*
