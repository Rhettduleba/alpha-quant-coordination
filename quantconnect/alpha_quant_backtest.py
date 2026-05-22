# ============================================================================
# Alpha Quant — Bot Strategy Backtest  (QuantConnect / LEAN, Python)   v2
# ----------------------------------------------------------------------------
# A faithful price-replay of the live Alpha Quant SIM bot's trading rules.
# Source of truth: ALPHA_QUANT_STRATEGY_SPEC.md (verified from bot source).
# THIS IS A BACKTESTING LAB ONLY. DO NOT DEPLOY LIVE.
#
# v1 result (2021-2025, 150 symbols): -99.92%, account decayed to ~$80.
# v2 changes (NOT to make the result "look right" — to make it trustworthy
# and diagnosable):
#   - OVER-ENTRY GUARD: now counts open *orders* as well as open positions,
#     so the 1-bar fill lag can no longer briefly stack >4 positions.
#   - DAILY LOGGING: one line per day (open equity, close equity, change,
#     fills) so the re-run shows exactly HOW capital is lost.
#   - SLIPPAGE knob: a top-level constant. Set SLIPPAGE = 0.0 for a diagnostic
#     run — if that alone turns the result roughly breakeven, it confirms the
#     strategy only "survives" in TradeStation SIM because SIM fills are
#     idealized (no slippage), and collapses under realistic costs.
#
# Honest note: do NOT tune this until it matches the -$2,282 SIM baseline.
# The backtest disagreeing with SIM is a finding, not a defect.
# ============================================================================

from AlgorithmImports import *

# ---------------------------------------------------------------------------
# EDITABLE. For a fast diagnostic run, do ONE year first (e.g. 2021 only).
# ---------------------------------------------------------------------------
START_YEAR, START_MONTH, START_DAY = 2021, 1, 1
END_YEAR,   END_MONTH,   END_DAY   = 2025, 12, 31
STARTING_CASH = 100_000

# Slippage per fill. 0.001 = 0.1% (~the bot's marketable-limit cross on a
# ~$100 stock). DIAGNOSTIC: set to 0.0 and re-run to isolate slippage's effect.
SLIPPAGE = 0.001

# ---------------------------------------------------------------------------
# Risk floors / constants — mirror the bot's hard floors exactly (spec sec 8)
# ---------------------------------------------------------------------------
DAILY_MAX_LOSS       = 10_000
MAX_POSITIONS        = 4           # long + short combined (positions + pending)
MAX_POSITION_PCT     = 0.25
MAX_TOTAL_EXPOSURE   = 100_000
MAX_SECTOR_POSITIONS = 2
COOLDOWN_MINUTES     = 15
LIMIT_OFFSET         = 0.10

W_MOMENTUM, W_VOLUME, W_SPREAD, W_PRICEACTION = 0.35, 0.25, 0.20, 0.20
MIN_SCORE = 0.40

HARD_STOP_PCT         = 0.50
PROFIT_TRIGGER_PCT    = 0.20
TRAILBACK_PCT         = 0.08
TIER2_PROFIT_PCT      = 0.75
TIER2_TRAILBACK_PCT   = 0.05
TIER3_PROFIT_PCT      = 1.50
TIER3_TRAILBACK_PCT   = 0.03
BREAKEVEN_TRIGGER_PCT = 0.40
BREAKEVEN_BUFFER_PCT  = 0.05

VOL_HIGH_PCT    = 2.5
VOL_EXTREME_PCT = 4.0

ASSUMED_SPREAD = 0.02   # 1-min bars carry no bid/ask; spread is approximated
ENTRY_CUTOFF   = (15, 50)

UNIVERSE = {
    "SGOV":"OTHER","TLT":"OTHER","TQQQ":"OTHER","IWM":"OTHER","NVDA":"Technology","IBIT":"OTHER",
    "NVO":"Health Care","SPYM":"OTHER","SQQQ":"OTHER","FXI":"OTHER","SLV":"OTHER","SH":"OTHER",
    "SCHD":"OTHER","GOOGL":"Technology","GOOG":"Technology","SPXS":"OTHER","MSFT":"Technology","TSLA":"Industrials",
    "AAPL":"Technology","INTC":"Technology","BABA":"Consumer Discretionary","EWY":"OTHER","AMD":"Technology","XLE":"OTHER",
    "AMZN":"Consumer Discretionary","KWEB":"OTHER","PFE":"Health Care","T":"Telecommunications","XLU":"OTHER","HPQ":"Technology",
    "AVGO":"Technology","GDX":"OTHER","WMT":"Consumer Discretionary","DOW":"Industrials","QBTS":"Technology","XOM":"Energy",
    "CMCSA":"Telecommunications","NVDL":"OTHER","XLF":"OTHER","MRVL":"Technology","SOXL":"OTHER","RKLB":"Industrials",
    "QCOM":"Technology","NFLX":"Consumer Discretionary","PBR":"Energy","GLW":"Industrials","PYPL":"Industrials","XLB":"OTHER",
    "VZ":"Telecommunications","MRK":"Health Care","BMY":"Health Care","RGTI":"Technology","DIS":"Consumer Discretionary","DVN":"Energy",
    "UBER":"Consumer Discretionary","NBIS":"Technology","BKLN":"OTHER","XLK":"OTHER","PLTR":"Technology","CPB":"Consumer Staples",
    "LQD":"OTHER","NKE":"Consumer Discretionary","SMCI":"Technology","MSTR":"Technology","PR":"Energy","NOW":"Technology",
    "IREN":"Technology","CCL":"Consumer Discretionary","TSM":"Technology","STM":"Technology","BIL":"OTHER","IJH":"OTHER",
    "IEF":"OTHER","SBUX":"Consumer Discretionary","MSFU":"OTHER","DIA":"OTHER","BKNG":"Consumer Discretionary","BP":"Energy",
    "QQQI":"OTHER","BNO":"OTHER","SDS":"OTHER","XLY":"OTHER","BA":"Industrials","XLV":"OTHER",
    "TMF":"OTHER","JPST":"OTHER","EWT":"OTHER","EWJ":"OTHER","SONY":"Consumer Staples","MCD":"Consumer Discretionary",
    "EQNR":"Energy","SHY":"OTHER","JAAA":"OTHER","UNH":"Health Care","JEPI":"OTHER","PDD":"Technology",
    "PEP":"Consumer Staples","GLD":"OTHER","AMDL":"OTHER","O":"Real Estate","JEPQ":"OTHER","TXN":"Technology",
    "SNOW":"Technology","MRNA":"Health Care","COIN":"Finance","VST":"Utilities","QLD":"OTHER","VGSH":"OTHER",
    "HD":"Consumer Discretionary","QQQM":"OTHER","BRK.B":"OTHER","USFR":"OTHER","BTI":"Health Care","AMRZ":"Industrials",
    "SCHO":"OTHER","SSO":"OTHER","VBIL":"OTHER","IAU":"OTHER","UL":"Consumer Discretionary","ADBE":"Technology",
    "VGT":"OTHER","SUNB":"Consumer Discretionary","FRO":"Consumer Discretionary","JHG":"Finance","OUST":"Industrials","VTI":"OTHER",
    "GLDM":"OTHER","AZN":"Health Care","CCJ":"Basic Materials","TIP":"OTHER","CCEP":"Consumer Staples","COPX":"OTHER",
    "ISRG":"Health Care","UBS":"Finance","XLRE":"OTHER","GBTC":"OTHER","BCS":"Finance","METU":"OTHER",
    "YINN":"OTHER","ING":"Finance","SGOL":"OTHER","SPSB":"OTHER","TS":"Industrials","GSK":"Health Care",
    "PULS":"OTHER","FNDX":"OTHER","IAUM":"OTHER","SNY":"Health Care","YUMC":"Consumer Discretionary","AMZU":"OTHER",
}


def _clamp(v, lo, hi):
    return max(lo, min(hi, v))


class AlphaQuantBacktest(QCAlgorithm):

    # =======================================================================
    def initialize(self):
        self.set_start_date(START_YEAR, START_MONTH, START_DAY)
        self.set_end_date(END_YEAR, END_MONTH, END_DAY)
        self.set_cash(STARTING_CASH)
        self.set_brokerage_model(BrokerageName.TRADE_STATION, AccountType.MARGIN)

        self.spy = self.add_equity("SPY", Resolution.MINUTE)
        self.spy.set_data_normalization_mode(DataNormalizationMode.ADJUSTED)
        self.spy.set_slippage_model(ConstantSlippageModel(SLIPPAGE))
        self.spy_symbol = self.spy.symbol

        self.symbols = []
        self.sector = {}
        for ticker, sec in UNIVERSE.items():
            try:
                eq = self.add_equity(ticker, Resolution.MINUTE)
                eq.set_data_normalization_mode(DataNormalizationMode.ADJUSTED)
                eq.set_slippage_model(ConstantSlippageModel(SLIPPAGE))
                self.symbols.append(eq.symbol)
                self.sector[eq.symbol] = sec
            except Exception as e:
                self.debug(f"Could not add {ticker}: {e}")

        self.current_day    = None
        self.day_open       = {}
        self.day_volume     = {}
        self.last_close     = {}
        self.prev_close     = {}
        self.spy_day_high   = None
        self.spy_day_low    = None
        self.spy_prev_close = None
        self.spy_last_close = None

        self.pos_extreme    = {}
        self.last_exit_time = {}

        self.day_start_equity = None
        self.day_label        = None
        self.halted_today     = False
        self.fills_today      = 0
        self.total_fills      = 0

        self.schedule.on(
            self.date_rules.every_day(self.spy_symbol),
            self.time_rules.before_market_close(self.spy_symbol, 10),
            self.eod_flatten,
        )

    # =======================================================================
    def on_order_event(self, order_event):
        if order_event.status == OrderStatus.FILLED:
            self.fills_today += 1
            self.total_fills += 1

    # =======================================================================
    def on_data(self, data):
        t = self.time

        # ---- day rollover (log the day that just ended) ------------------
        if t.date() != self.current_day:
            if self.day_label is not None and self.day_start_equity is not None:
                eq = self.portfolio.total_portfolio_value
                self.log(f"DAY {self.day_label} | open=${self.day_start_equity:,.0f} "
                         f"close=${eq:,.0f} change=${eq - self.day_start_equity:,.0f} "
                         f"fills={self.fills_today}")
            self.current_day = t.date()
            self.day_label = str(t.date())
            for s in self.symbols:
                if s in self.last_close:
                    self.prev_close[s] = self.last_close[s]
            self.day_open = {}
            self.day_volume = {}
            if self.spy_last_close is not None:
                self.spy_prev_close = self.spy_last_close
            self.spy_day_high = None
            self.spy_day_low = None
            self.day_start_equity = self.portfolio.total_portfolio_value
            self.halted_today = False
            self.fills_today = 0

        # ---- SPY day state -----------------------------------------------
        if data.contains_key(self.spy_symbol) and data[self.spy_symbol] is not None:
            b = data[self.spy_symbol]
            self.spy_day_high = b.high if self.spy_day_high is None else max(self.spy_day_high, b.high)
            self.spy_day_low  = b.low  if self.spy_day_low  is None else min(self.spy_day_low,  b.low)
            self.spy_last_close = b.close

        # ---- per-symbol day state ----------------------------------------
        for s in self.symbols:
            if data.contains_key(s) and data[s] is not None:
                b = data[s]
                if s not in self.day_open:
                    self.day_open[s] = b.open
                self.day_volume[s] = self.day_volume.get(s, 0.0) + b.volume
                self.last_close[s] = b.close

        # ---- volatility regime -------------------------------------------
        regime = "NORMAL"
        if self.spy_prev_close and self.spy_prev_close > 0 \
           and self.spy_day_high is not None and self.spy_day_low is not None:
            rng = (self.spy_day_high - self.spy_day_low) / self.spy_prev_close * 100.0
            if rng >= VOL_EXTREME_PCT:
                regime = "EXTREME"
            elif rng >= VOL_HIGH_PCT:
                regime = "HIGH"

        # ---- daily loss guard --------------------------------------------
        if self.day_start_equity is not None and not self.halted_today:
            if self.portfolio.total_portfolio_value - self.day_start_equity <= -DAILY_MAX_LOSS:
                self.liquidate()
                self.halted_today = True
                self.log(f"{t} DAILY LOSS LIMIT HIT -- halted for the day")

        # ---- exits always run --------------------------------------------
        self._manage_exits(data)

        if self.halted_today:
            return
        if (t.hour, t.minute) >= ENTRY_CUTOFF:
            return
        if regime == "EXTREME":
            return

        self._try_enter(data, regime, "LONG")
        self._try_enter(data, regime, "SHORT")

    # =======================================================================
    def eod_flatten(self):
        if self.portfolio.invested:
            self.liquidate()
        self.pos_extreme.clear()

    # =======================================================================
    def _manage_exits(self, data):
        for s in self.symbols:
            holding = self.portfolio[s]
            if not holding.invested:
                self.pos_extreme.pop(s, None)
                continue
            if not (data.contains_key(s) and data[s] is not None):
                continue
            last = data[s].close
            avg = holding.average_price
            if avg <= 0:
                continue

            if holding.is_long:
                self.pos_extreme[s] = last if s not in self.pos_extreme else max(self.pos_extreme[s], last)
                high = self.pos_extreme[s]
                profit = (last - avg) / avg * 100.0
                hard = avg * (1 - HARD_STOP_PCT / 100.0)
                trail = None
                if profit >= TIER3_PROFIT_PCT:
                    trail = high * (1 - TIER3_TRAILBACK_PCT / 100.0)
                elif profit >= TIER2_PROFIT_PCT:
                    trail = high * (1 - TIER2_TRAILBACK_PCT / 100.0)
                elif profit >= PROFIT_TRIGGER_PCT:
                    trail = high * (1 - TRAILBACK_PCT / 100.0)
                be = avg * (1 + BREAKEVEN_BUFFER_PCT / 100.0) if profit >= BREAKEVEN_TRIGGER_PCT else None
                if (last <= hard) or (be is not None and last <= be) or (trail is not None and last <= trail):
                    self.liquidate(s)
                    self.last_exit_time[s] = self.time
                    self.pos_extreme.pop(s, None)

            elif holding.is_short:
                self.pos_extreme[s] = last if s not in self.pos_extreme else min(self.pos_extreme[s], last)
                low = self.pos_extreme[s]
                profit = (avg - last) / avg * 100.0
                hard = avg * (1 + HARD_STOP_PCT / 100.0)
                trail = None
                if profit >= TIER3_PROFIT_PCT:
                    trail = low * (1 + TIER3_TRAILBACK_PCT / 100.0)
                elif profit >= TIER2_PROFIT_PCT:
                    trail = low * (1 + TIER2_TRAILBACK_PCT / 100.0)
                elif profit >= PROFIT_TRIGGER_PCT:
                    trail = low * (1 + TRAILBACK_PCT / 100.0)
                be = avg * (1 + BREAKEVEN_BUFFER_PCT / 100.0) if profit >= BREAKEVEN_TRIGGER_PCT else None
                if (last >= hard) or (be is not None and last >= be) or (trail is not None and last >= trail):
                    self.liquidate(s)
                    self.last_exit_time[s] = self.time
                    self.pos_extreme.pop(s, None)

    # =======================================================================
    def _try_enter(self, data, regime, side):
        # Count positions AND open orders together — the v1 over-entry fix.
        invested = set(s for s in self.symbols if self.portfolio[s].invested)
        pending = set(o.symbol for o in self.transactions.get_open_orders())
        occupied = invested | pending
        if len(occupied) >= MAX_POSITIONS:
            return
        exposure = sum(abs(self.portfolio[s].holdings_value) for s in invested)
        if exposure >= MAX_TOTAL_EXPOSURE:
            return

        candidates = []
        for s in self.symbols:
            if s in occupied:
                continue
            le = self.last_exit_time.get(s)
            if le is not None and (self.time - le).total_seconds() < COOLDOWN_MINUTES * 60:
                continue
            if not (data.contains_key(s) and data[s] is not None):
                continue
            if s not in self.prev_close or self.prev_close[s] <= 0:
                continue
            if s not in self.day_open:
                continue
            last = data[s].close
            score = self._score(side, last, self.day_open[s], self.prev_close[s],
                                 self.day_volume.get(s, 0.0), regime)
            if score is not None and score >= MIN_SCORE:
                candidates.append((s, score, last))
        candidates.sort(key=lambda x: x[1], reverse=True)

        sec_count = {}
        for s in invested:
            sc = self.sector.get(s, "OTHER")
            sec_count[sc] = sec_count.get(sc, 0) + 1

        strategy_capital = min(self.portfolio.total_portfolio_value, MAX_TOTAL_EXPOSURE)
        max_dollars = strategy_capital * MAX_POSITION_PCT

        for s, score, last in candidates:
            sc = self.sector.get(s, "OTHER")
            if sc != "OTHER" and sec_count.get(sc, 0) >= MAX_SECTOR_POSITIONS:
                continue
            if side == "LONG":
                qty = int(max_dollars // round(last + LIMIT_OFFSET, 2))
            else:
                qty = int(max_dollars // last)
            if qty < 1:
                continue
            if exposure + qty * last > MAX_TOTAL_EXPOSURE:
                continue
            self.market_order(s, qty if side == "LONG" else -qty)
            return

    # =======================================================================
    def _score(self, side, last, day_open, prev_close, day_volume, regime):
        spread = ASSUMED_SPREAD
        net_change_pct = (last - prev_close) / prev_close * 100.0

        if side == "LONG":
            min_price, min_chg, min_vol, max_spread = 20.0, 0.25, 500_000.0, 0.25
            if regime == "HIGH":
                max_spread *= 0.7; min_vol *= 1.5; min_chg *= 1.5
            if last < min_price:            return None
            if net_change_pct < min_chg:    return None
            if day_volume < min_vol:        return None
            if spread > max_spread:         return None
            mom = _clamp(net_change_pct / 2.5, 0.0, 1.0) if net_change_pct > 0 else 0.0
            pa = self._price_action_long(last, day_open, prev_close)
        else:
            min_price, max_chg, min_vol, max_spread = 20.0, -0.60, 1_000_000.0, 0.15
            min_below_open, min_below_pc = 0.20, 0.20
            if regime == "HIGH":
                max_spread *= 0.7; min_vol *= 1.5; max_chg *= 1.5
            if last < min_price:                          return None
            if net_change_pct > max_chg:                  return None
            if day_volume < min_vol:                      return None
            if spread > max_spread:                       return None
            if day_open > 0 and last >= day_open:         return None
            if prev_close > 0 and last >= prev_close:     return None
            below_open = (day_open - last) / day_open * 100.0 if day_open > 0 else 0.0
            if below_open < min_below_open:               return None
            below_pc = (prev_close - last) / prev_close * 100.0 if prev_close > 0 else 0.0
            if below_pc < min_below_pc:                   return None
            mom = _clamp(abs(net_change_pct) / 2.5, 0.0, 1.0) if net_change_pct < 0 else 0.0
            pa = self._price_action_short(last, day_open, prev_close)

        vol_s = self._volume_score(day_volume, min_vol)
        spr_s = self._spread_score(spread, max_spread)
        return W_MOMENTUM * mom + W_VOLUME * vol_s + W_SPREAD * spr_s + W_PRICEACTION * pa

    @staticmethod
    def _volume_score(volume, min_volume):
        if volume <= 0:
            return 0.0
        ratio = volume / min_volume
        if ratio >= 3.0:
            return 1.0
        if ratio >= 1.0:
            return (ratio - 1.0) / 2.0
        return 0.0

    @staticmethod
    def _spread_score(spread, max_spread):
        if spread <= 0:
            return 1.0
        if spread >= max_spread:
            return 0.0
        return 1.0 - (spread / max_spread)

    @staticmethod
    def _price_action_long(last, open_price, prev_close):
        if open_price <= 0 and prev_close <= 0:
            return 0.5
        score = 0.5
        if open_price > 0 and last > open_price:
            score += _clamp((last - open_price) / open_price * 100.0 / 2.0, 0.0, 0.3)
        elif open_price > 0 and last < open_price:
            score -= 0.2
        if prev_close > 0 and last > prev_close:
            score += 0.2
        return _clamp(score, 0.0, 1.0)

    @staticmethod
    def _price_action_short(last, open_price, prev_close):
        if open_price <= 0 and prev_close <= 0:
            return 0.5
        score = 0.5
        if open_price > 0 and last < open_price:
            score += _clamp((open_price - last) / open_price * 100.0 / 2.0, 0.0, 0.3)
        elif open_price > 0 and last > open_price:
            score -= 0.2
        if prev_close > 0 and last < prev_close:
            score += 0.2
        return _clamp(score, 0.0, 1.0)

    # =======================================================================
    def on_end_of_algorithm(self):
        self.log(f"END | equity=${self.portfolio.total_portfolio_value:,.2f} "
                 f"total_fills={self.total_fills}")
