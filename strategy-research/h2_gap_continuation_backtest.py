# ============================================================================
# Strategy Research — Hypothesis H2: Intraday Gap Continuation
# QuantConnect / LEAN (Python).  Plan: strategy-research/H2_gap_continuation_research_plan.md
# ----------------------------------------------------------------------------
# Hypothesis: when a liquid large-cap gaps >= 4% at the open (a real overnight
# catalyst) and still holds the gap at 9:45, the move continues through the day.
# Designed to trade RARELY -- the opposite of H1, which died to cost drag.
#
# RESEARCH BACKTEST ONLY -- not the Alpha Quant bot, not live trading.
#
# HOW TO RUN:
#   Run A: paste as-is (SLIPPAGE = 0.0005), backtest.
#   Run B: set SLIPPAGE = 0.0, backtest again.
#   Both use the TRAIN window (2016-2021). Do NOT touch the 2022+ holdout.
# ============================================================================

from AlgorithmImports import *

# --- Train window. Holdout 2022+ is run later, once, per the research plan. ---
START = (2016, 1, 1)
END   = (2021, 12, 31)
STARTING_CASH = 100_000

# --- Knobs ---
SLIPPAGE          = 0.0005    # 0.05% per fill. Run B: set to 0.0.
RISK_PCT          = 0.01      # risk 1% of equity per trade
GAP_PCT           = 4.0       # trade only if |overnight gap| >= this %
OPENING_RANGE_END = (9, 45)   # first 15 min -> defines the stop reference
ENTRY_CUTOFF      = (15, 0)   # (one decision is made at 9:45; this is a guard)
FLATTEN_TIME      = (15, 50)  # flatten everything at 3:50 PM
MAX_POSITIONS     = 5
MAX_POSITION_PCT  = 0.25      # notional cap per position

UNIVERSE = [
    "AAPL","MSFT","AMZN","GOOGL","META","NVDA","TSLA","AMD","INTC","QCOM",
    "CRM","ADBE","NFLX","CSCO","JPM","BAC","GS","WFC","V","MA",
    "UNH","JNJ","PFE","MRK","ABBV","HD","NKE","MCD","SBUX","COST",
    "WMT","DIS","XOM","CVX","BA","CAT",
]


class GapContinuation_H2(QCAlgorithm):

    def initialize(self):
        self.set_start_date(*START)
        self.set_end_date(*END)
        self.set_cash(STARTING_CASH)
        self.set_brokerage_model(BrokerageName.TRADE_STATION, AccountType.MARGIN)

        self.symbols = []
        for tk in UNIVERSE:
            try:
                eq = self.add_equity(tk, Resolution.MINUTE)
                eq.set_data_normalization_mode(DataNormalizationMode.ADJUSTED)
                eq.set_slippage_model(ConstantSlippageModel(SLIPPAGE))
                self.symbols.append(eq.symbol)
            except Exception as e:
                self.debug(f"skip {tk}: {e}")

        self.current_day = None
        self.last_close  = {}   # most recent close (rolls into prev_close)
        self.prev_close  = {}   # prior trading day's close
        self.trades = 0
        self._reset_day()

    def _reset_day(self):
        self.day_open     = {}
        self.or_high      = {}
        self.or_low       = {}
        self.stop_price   = {}
        self.day_decided  = False

    def on_data(self, data):
        t = self.time
        hm = (t.hour, t.minute)

        # ---- day rollover ----
        if t.date() != self.current_day:
            for s in self.symbols:
                if s in self.last_close:
                    self.prev_close[s] = self.last_close[s]
            self.current_day = t.date()
            self._reset_day()

        # ---- forced EOD flatten ----
        if hm >= FLATTEN_TIME:
            if self.portfolio.invested:
                self.liquidate()
            return

        in_or = hm <= OPENING_RANGE_END

        # ---- accumulate the opening range + latest price ----
        for s in self.symbols:
            if not (data.contains_key(s) and data[s] is not None):
                continue
            bar = data[s]
            if in_or:
                if s not in self.day_open:
                    self.day_open[s] = bar.open
                self.or_high[s] = bar.high if s not in self.or_high else max(self.or_high[s], bar.high)
                self.or_low[s]  = bar.low  if s not in self.or_low  else min(self.or_low[s],  bar.low)
            self.last_close[s] = bar.close

        if in_or:
            return

        # ---- manage open positions: opposite-OR stop ----
        for s in self.symbols:
            holding = self.portfolio[s]
            if not holding.invested:
                continue
            if not (data.contains_key(s) and data[s] is not None):
                continue
            bar = data[s]
            stop = self.stop_price.get(s)
            if stop is None:
                continue
            if holding.is_long and bar.low <= stop:
                self.liquidate(s)
            elif holding.is_short and bar.high >= stop:
                self.liquidate(s)

        # ---- the one-time 9:45 decision for the whole day ----
        if self.day_decided:
            return
        self.day_decided = True
        if hm >= ENTRY_CUTOFF:
            return

        # build the day's gap candidates
        candidates = []   # (abs_gap, side, symbol, price, stop, risk_per_share)
        for s in self.symbols:
            if self.portfolio[s].invested:
                continue
            if s not in self.prev_close or self.prev_close[s] <= 0:
                continue
            if s not in self.day_open or s not in self.or_low or s not in self.or_high:
                continue
            if s not in self.last_close:
                continue
            day_open = self.day_open[s]
            prev_close = self.prev_close[s]
            price = self.last_close[s]            # ~price at 9:45
            gap = (day_open - prev_close) / prev_close * 100.0

            if gap >= GAP_PCT and price >= day_open:          # up-gap, held -> long
                stop = self.or_low[s]
                risk = price - stop
                if risk > 0:
                    candidates.append((abs(gap), "LONG", s, price, stop, risk))
            elif gap <= -GAP_PCT and price <= day_open:       # down-gap, held -> short
                stop = self.or_high[s]
                risk = stop - price
                if risk > 0:
                    candidates.append((abs(gap), "SHORT", s, price, stop, risk))

        # biggest gaps first; enter up to the position cap
        candidates.sort(key=lambda c: c[0], reverse=True)
        opened = 0
        equity = self.portfolio.total_portfolio_value
        for _abs_gap, side, s, price, stop, risk in candidates:
            if opened >= MAX_POSITIONS:
                break
            qty = min(int((equity * RISK_PCT) / risk),
                      int((equity * MAX_POSITION_PCT) / price))
            if qty < 1:
                continue
            self.market_order(s, qty if side == "LONG" else -qty)
            self.stop_price[s] = stop
            self.trades += 1
            opened += 1

    def on_end_of_algorithm(self):
        self.log(f"END | equity=${self.portfolio.total_portfolio_value:,.2f} | "
                 f"entries={self.trades}")
