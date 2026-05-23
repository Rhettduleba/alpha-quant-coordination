# ============================================================================
# Strategy Research — Hypothesis H3: Faithful Zarattini Stocks-in-Play ORB
# QuantConnect / LEAN (Python).  Plan: H3_zarattini_faithful_research_plan.md
# ----------------------------------------------------------------------------
# Faithful test of the Zarattini & Aziz (2024) strategy:
#   * Broad universe (~1000 liquid US stocks), filtered daily
#   * Rank by abnormal first-5-min volume; trade top 20
#   * 5-min opening-range break in the direction of the break
#   * ATR(14) stops and ATR-based sizing
#   * Flat by 3:50 PM ET, never overnight
#
# RESEARCH BACKTEST ONLY -- not the Alpha Quant bot, not live trading.
#
# HOW TO RUN:
#   Run A: paste as-is (SLIPPAGE = 0.0005), backtest.
#   Run B: set SLIPPAGE = 0.0, backtest again.
#   Train window is 2016-2021. Do NOT touch the 2022+ holdout until the
#   research plan says to.
# ============================================================================

from AlgorithmImports import *
from collections import deque

# --- Train window. Holdout 2022-01-01..present is run later, once. ---
START = (2016, 1, 1)
END   = (2021, 12, 31)
STARTING_CASH = 100_000

# --- Knobs ---
SLIPPAGE          = 0.0005    # 0.05% per fill. Run B: set to 0.0.
RISK_PCT          = 0.01      # risk 1% of equity per trade
ATR_PERIOD        = 14        # daily ATR(14)
ATR_STOP_MULT     = 1.0       # stop distance = 1.0 x ATR
OR_END            = (9, 35)   # opening range = 9:30 .. 9:35 (5 minutes)
ENTRY_CUTOFF      = (15, 0)   # no new entries at/after 3:00 PM
FLATTEN_TIME      = (15, 50)  # flatten everything at 3:50 PM
TOP_N             = 20        # trade top N by relative opening volume
MAX_POSITIONS     = 10        # concurrent position cap
MAX_POSITION_PCT  = 0.15      # per-position notional cap
VOLUME_LOOKBACK   = 14        # days of 5-min-OR-volume history for ranking
MIN_REL_VOL       = 1.0       # only consider stocks with relvol >= this

# Universe (daily coarse filter)
UNIVERSE_SIZE     = 1000
MIN_PRICE         = 5.0
MIN_DOLLAR_VOL    = 10_000_000


class ZarattiniORB_H3(QCAlgorithm):

    def initialize(self):
        self.set_start_date(*START)
        self.set_end_date(*END)
        self.set_cash(STARTING_CASH)
        self.set_brokerage_model(BrokerageName.TRADE_STATION, AccountType.MARGIN)
        self.set_warm_up(timedelta(days=25))

        self.universe_settings.resolution = Resolution.MINUTE
        self.add_universe(self.coarse_selector)
        self.set_security_initializer(self.sec_init)

        # per-symbol state
        self.atr_inds    = {}    # symbol -> AverageTrueRange indicator
        self.vol_history = {}    # symbol -> deque of last N days' 5-min OR volume

        # per-day state
        self.current_day      = None
        self.day_open         = {}
        self.or_high          = {}
        self.or_low           = {}
        self.or_volume        = {}
        self.day_decided      = False
        self.tradeable_today  = set()    # top-N symbols by relvol today
        self.entered_today    = set()
        self.stop_price       = {}

        # bookkeeping
        self.last_close = {}
        self.trades = 0

    def sec_init(self, security):
        security.set_slippage_model(ConstantSlippageModel(SLIPPAGE))

    def coarse_selector(self, coarse):
        filtered = [c for c in coarse
                    if c.has_fundamental_data
                    and c.price is not None and c.price > MIN_PRICE
                    and c.dollar_volume is not None and c.dollar_volume > MIN_DOLLAR_VOL]
        filtered.sort(key=lambda c: c.dollar_volume, reverse=True)
        return [c.symbol for c in filtered[:UNIVERSE_SIZE]]

    def on_securities_changed(self, changes):
        for sec in changes.added_securities:
            sym = sec.symbol
            if sym not in self.atr_inds:
                self.atr_inds[sym] = self.atr(sym, ATR_PERIOD, MovingAverageType.SIMPLE, Resolution.DAILY)
            if sym not in self.vol_history:
                self.vol_history[sym] = deque(maxlen=VOLUME_LOOKBACK)
        for sec in changes.removed_securities:
            sym = sec.symbol
            if self.portfolio[sym].invested:
                self.liquidate(sym)
            self.atr_inds.pop(sym, None)
            self.vol_history.pop(sym, None)
            self.day_open.pop(sym, None)
            self.or_high.pop(sym, None)
            self.or_low.pop(sym, None)
            self.or_volume.pop(sym, None)
            self.last_close.pop(sym, None)
            self.stop_price.pop(sym, None)
            self.entered_today.discard(sym)
            self.tradeable_today.discard(sym)

    def on_data(self, data):
        if self.is_warming_up:
            return
        t = self.time
        hm = (t.hour, t.minute)

        # ---- day rollover ----
        if t.date() != self.current_day:
            # archive yesterday's 5-min OR volumes into rolling history
            for sym, vol in self.or_volume.items():
                if vol > 0 and sym in self.vol_history:
                    self.vol_history[sym].append(vol)
            self.current_day = t.date()
            self.day_open = {}
            self.or_high = {}
            self.or_low = {}
            self.or_volume = {}
            self.day_decided = False
            self.tradeable_today = set()
            self.entered_today = set()
            self.stop_price = {}

        # ---- forced EOD flatten ----
        if hm >= FLATTEN_TIME:
            if self.portfolio.invested:
                self.liquidate()
            return

        in_or = hm <= OR_END

        # iterate over current universe symbols
        symbols = list(self.active_securities.keys())

        # ---- accumulate opening range + latest price ----
        for sym in symbols:
            if not (data.contains_key(sym) and data[sym] is not None):
                continue
            bar = data[sym]
            if in_or:
                if sym not in self.day_open:
                    self.day_open[sym] = bar.open
                self.or_high[sym] = bar.high if sym not in self.or_high else max(self.or_high[sym], bar.high)
                self.or_low[sym]  = bar.low  if sym not in self.or_low  else min(self.or_low[sym],  bar.low)
                self.or_volume[sym] = self.or_volume.get(sym, 0.0) + bar.volume
            self.last_close[sym] = bar.close

        if in_or:
            return

        # ---- once per day, just after OR closes: rank and pick top-N ----
        if not self.day_decided:
            self.day_decided = True
            self.rank_and_select()

        # ---- manage exits on any open position (ATR stop) ----
        for sym in symbols:
            holding = self.portfolio[sym]
            if not holding.invested:
                continue
            if not (data.contains_key(sym) and data[sym] is not None):
                continue
            bar = data[sym]
            stop = self.stop_price.get(sym)
            if stop is None:
                continue
            if holding.is_long and bar.low <= stop:
                self.liquidate(sym)
                self.stop_price.pop(sym, None)
            elif holding.is_short and bar.high >= stop:
                self.liquidate(sym)
                self.stop_price.pop(sym, None)

        # ---- entries: top-N tradeable symbols, ORB break ----
        if hm >= ENTRY_CUTOFF:
            return
        open_count = sum(1 for s in symbols if self.portfolio[s].invested)
        pending = set(o.symbol for o in self.transactions.get_open_orders())
        if open_count + len(pending) >= MAX_POSITIONS:
            return

        equity = self.portfolio.total_portfolio_value

        for sym in list(self.tradeable_today):
            if sym in self.entered_today or sym in pending:
                continue
            if self.portfolio[sym].invested:
                continue
            if not (data.contains_key(sym) and data[sym] is not None):
                continue
            if sym not in self.or_high or sym not in self.or_low:
                continue
            atr_ind = self.atr_inds.get(sym)
            if atr_ind is None or not atr_ind.is_ready:
                continue
            atr = float(atr_ind.current.value)
            if atr <= 0:
                continue
            bar = data[sym]

            side = None
            if bar.high > self.or_high[sym]:
                side = "LONG"
                entry_ref = self.or_high[sym]
            elif bar.low < self.or_low[sym]:
                side = "SHORT"
                entry_ref = self.or_low[sym]
            if side is None:
                continue

            risk_per_share = ATR_STOP_MULT * atr
            risk_dollars = equity * RISK_PCT
            qty_by_risk = int(risk_dollars / risk_per_share)
            qty_by_cap  = int((equity * MAX_POSITION_PCT) / bar.close) if bar.close > 0 else 0
            qty = min(qty_by_risk, qty_by_cap)
            if qty < 1:
                continue

            if side == "LONG":
                self.market_order(sym, qty)
                self.stop_price[sym] = entry_ref - ATR_STOP_MULT * atr
            else:
                self.market_order(sym, -qty)
                self.stop_price[sym] = entry_ref + ATR_STOP_MULT * atr
            self.entered_today.add(sym)
            self.trades += 1

            open_count += 1
            if open_count >= MAX_POSITIONS:
                break

    def rank_and_select(self):
        scored = []
        for sym, vol in self.or_volume.items():
            hist = self.vol_history.get(sym)
            if hist is None or len(hist) < 5:
                continue
            avg = sum(hist) / len(hist)
            if avg <= 0:
                continue
            rel_vol = vol / avg
            if rel_vol < MIN_REL_VOL:
                continue
            scored.append((rel_vol, sym))
        scored.sort(reverse=True)
        self.tradeable_today = set(sym for _, sym in scored[:TOP_N])

    def on_end_of_algorithm(self):
        self.log(f"END | equity=${self.portfolio.total_portfolio_value:,.2f} | "
                 f"entries={self.trades}")
