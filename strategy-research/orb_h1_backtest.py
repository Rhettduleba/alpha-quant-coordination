# ============================================================================
# Strategy Research — Hypothesis H1: Opening Range Breakout for stocks in play
# QuantConnect / LEAN (Python).  Plan: strategy-research/ORB_H1_research_plan.md
# ----------------------------------------------------------------------------
# Hypothesis: on liquid large-caps that open with elevated relative volume,
# a break of the first-15-minute range continues in that direction often
# enough to be profitable net of realistic costs.
#
# This is RESEARCH, not the Alpha Quant bot. Backtesting lab only.
#
# HOW TO RUN (two runs, then send results back):
#   Run A: paste as-is (SLIPPAGE = 0.0005), backtest -> note return / trades /
#          win rate / profit factor / equity curve.
#   Run B: set SLIPPAGE = 0.0, backtest again. If A has no edge but B does,
#          the "edge" was never real.
#   Both runs use the TRAIN window (2016-2021). Do NOT touch the holdout
#   (2022-2025) until the plan's step 5.
# ============================================================================

from AlgorithmImports import *
from collections import deque

# --- Train window. Holdout 2022-01-01..2025-12-31 — run ONCE, later, per plan.
START = (2016, 1, 1)
END   = (2021, 12, 31)
STARTING_CASH = 100_000

# --- Knobs ---
SLIPPAGE             = 0.0005    # 0.05% per fill. Run B: set to 0.0.
RISK_PCT             = 0.01      # risk 1% of equity per trade
OPENING_RANGE_END    = (9, 45)   # opening range = 9:30 .. 9:45 ET
INPLAY_VOLUME_MULT   = 1.5       # "in play" if OR volume > this x its 14-day avg
VOLUME_LOOKBACK_DAYS = 14
MIN_HISTORY_DAYS     = 10        # need this many days of history before trading
MAX_POSITIONS        = 5
MAX_POSITION_PCT     = 0.25      # notional cap per position
ENTRY_CUTOFF         = (15, 0)   # no new entries at/after 3:00 PM
FLATTEN_TIME         = (15, 50)  # flatten everything at 3:50 PM

# Fixed liquid large-cap universe. Not point-in-time -> mild survivorship bias
# (a known v1 limitation, documented in the research plan).
UNIVERSE = [
    "AAPL","MSFT","AMZN","GOOGL","META","NVDA","TSLA","AMD","INTC","QCOM",
    "CRM","ADBE","NFLX","CSCO","JPM","BAC","GS","WFC","V","MA",
    "UNH","JNJ","PFE","MRK","ABBV","HD","NKE","MCD","SBUX","COST",
    "WMT","DIS","XOM","CVX","BA","CAT",
]


class ORB_H1_Research(QCAlgorithm):

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

        self.vol_history = {s: deque(maxlen=VOLUME_LOOKBACK_DAYS) for s in self.symbols}
        self.current_day = None
        self.trades = 0
        self._reset_day()

    def _reset_day(self):
        self.or_high       = {}
        self.or_low        = {}
        self.or_volume     = {}
        self.or_finalized  = {}
        self.in_play       = {}
        self.entered_today = set()
        self.stop_price    = {}

    def on_data(self, data):
        t = self.time
        hm = (t.hour, t.minute)

        # ---- day rollover: archive yesterday's OR volume, reset ----
        if t.date() != self.current_day:
            for s in self.symbols:
                if self.or_finalized.get(s) and s in self.or_volume:
                    self.vol_history[s].append(self.or_volume[s])
            self.current_day = t.date()
            self._reset_day()

        # ---- forced EOD flatten ----
        if hm >= FLATTEN_TIME:
            if self.portfolio.invested:
                self.liquidate()
            return

        in_opening_range = hm <= OPENING_RANGE_END

        # occupancy for the position cap (positions + pending orders)
        pending = set(o.symbol for o in self.transactions.get_open_orders())
        invested = set(s for s in self.symbols if self.portfolio[s].invested)
        occupied = invested | pending

        for s in self.symbols:
            if not (data.contains_key(s) and data[s] is not None):
                continue
            bar = data[s]

            # ---- build the opening range (9:30-9:45) ----
            if in_opening_range:
                self.or_high[s]   = bar.high if s not in self.or_high else max(self.or_high[s], bar.high)
                self.or_low[s]    = bar.low  if s not in self.or_low  else min(self.or_low[s],  bar.low)
                self.or_volume[s] = self.or_volume.get(s, 0.0) + bar.volume
                continue

            # ---- finalize the OR + "in play" test, once, just after 9:45 ----
            if not self.or_finalized.get(s):
                self.or_finalized[s] = True
                hist = self.vol_history[s]
                if len(hist) >= MIN_HISTORY_DAYS and s in self.or_volume:
                    avg = sum(hist) / len(hist)
                    self.in_play[s] = avg > 0 and self.or_volume[s] > INPLAY_VOLUME_MULT * avg
                else:
                    self.in_play[s] = False

            holding = self.portfolio[s]

            # ---- manage an open position: opposite-OR stop ----
            if holding.invested:
                stop = self.stop_price.get(s)
                if stop is not None:
                    if holding.is_long and bar.low <= stop:
                        self.liquidate(s)
                    elif holding.is_short and bar.high >= stop:
                        self.liquidate(s)
                continue

            # ---- entry checks ----
            if hm >= ENTRY_CUTOFF:
                continue
            if s in self.entered_today or s in occupied:
                continue
            if not self.in_play.get(s):
                continue
            if s not in self.or_high or s not in self.or_low:
                continue
            if len(occupied) >= MAX_POSITIONS:
                continue

            or_high = self.or_high[s]
            or_low  = self.or_low[s]
            or_width = or_high - or_low
            if or_width <= 0 or bar.close <= 0:
                continue

            equity = self.portfolio.total_portfolio_value
            risk_shares = int((equity * RISK_PCT) / or_width)
            cap_shares  = int((equity * MAX_POSITION_PCT) / bar.close)
            qty = min(risk_shares, cap_shares)
            if qty < 1:
                continue

            if bar.high > or_high:        # upside breakout -> long
                self.market_order(s, qty)
                self.stop_price[s] = or_low
                self.entered_today.add(s)
                occupied.add(s)
                self.trades += 1
            elif bar.low < or_low:        # downside breakout -> short
                self.market_order(s, -qty)
                self.stop_price[s] = or_high
                self.entered_today.add(s)
                occupied.add(s)
                self.trades += 1

    def on_end_of_algorithm(self):
        self.log(f"END | equity=${self.portfolio.total_portfolio_value:,.2f} | "
                 f"entries={self.trades}")
