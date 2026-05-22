# ============================================================================
# Alpha Quant — Bot Strategy Backtest  (QuantConnect / LEAN, Python)
# ----------------------------------------------------------------------------
# A faithful price-replay of the live Alpha Quant SIM bot's trading rules.
# Source of truth: ALPHA_QUANT_STRATEGY_SPEC.md (verified from bot source,
# May 22, 2026). Build/verify against that spec, not from memory.
#
# THIS IS A BACKTESTING LAB ONLY. DO NOT DEPLOY LIVE.
#
# What this faithfully replicates:
#   - The composite entry score (momentum/volume/spread/price-action)
#   - Long and short hard filters (incl. the short-side below-open/prev-close)
#   - The SPY volatility-regime gate (NORMAL / HIGH / EXTREME)
#   - The tiered trailing stop + breakeven lock + 0.50% hard stop exit engine
#   - Risk floors: 4 positions, 25% sizing, $100k exposure, $10k daily loss
#   - 15-min re-entry cooldown, sector cap (max 2/sector), 3:50 PM cutoff+flatten
#
# Known fidelity gaps (see spec section 10) — disclose on every result:
#   1. Historical bars have NO bid/ask. Spread is approximated (ASSUMED_SPREAD).
#   2. Entries modeled as market orders + slippage (the bot's last +/- $0.10
#      limit is marketable, so this is close); fills are a model, not reality.
#   3. Cadence: the live bot loops every ~15s; this evaluates every 1-min bar.
#   4. The Claude advisor overlay is NOT simulated — this is the bare strategy.
#   5. Universe is today's ~150 symbols applied to history -> survivorship bias.
#
# Honest baseline to judge against: 593 trades, -$2,282 net over 22 SIM days
# (broker truth). The strategy's edge is unproven.
# ============================================================================

from AlgorithmImports import *

# ---------------------------------------------------------------------------
# EDITABLE: backtest window. 150 symbols x 1-min x 5y is heavy — for a quick
# first run, shorten this (e.g. one year) or trim UNIVERSE.
# ---------------------------------------------------------------------------
START_YEAR, START_MONTH, START_DAY = 2021, 1, 1
END_YEAR,   END_MONTH,   END_DAY   = 2025, 12, 31
STARTING_CASH = 100_000

# ---------------------------------------------------------------------------
# Risk floors / constants — mirror the bot's hard floors exactly (spec sec 8)
# ---------------------------------------------------------------------------
DAILY_MAX_LOSS       = 10_000      # full halt for the day if today's P&L <= -this
MAX_POSITIONS        = 4           # long + short combined
MAX_POSITION_PCT     = 0.25        # 25% of (equity capped at $100k) per position
MAX_TOTAL_EXPOSURE   = 100_000
MAX_SECTOR_POSITIONS = 2           # per sector group ("OTHER" is exempt)
COOLDOWN_MINUTES     = 15          # re-entry cooldown per symbol
LIMIT_OFFSET         = 0.10        # bot's marketable-limit offset

# Entry composite score (spec sec 4)
W_MOMENTUM, W_VOLUME, W_SPREAD, W_PRICEACTION = 0.35, 0.25, 0.20, 0.20
MIN_SCORE = 0.40

# Exit engine (spec sec 7)
HARD_STOP_PCT        = 0.50
PROFIT_TRIGGER_PCT   = 0.20
TRAILBACK_PCT        = 0.08
TIER2_PROFIT_PCT     = 0.75
TIER2_TRAILBACK_PCT  = 0.05
TIER3_PROFIT_PCT     = 1.50
TIER3_TRAILBACK_PCT  = 0.03
BREAKEVEN_TRIGGER_PCT = 0.40
BREAKEVEN_BUFFER_PCT  = 0.05

# Volatility regime (spec sec 5)
VOL_HIGH_PCT    = 2.5
VOL_EXTREME_PCT = 4.0

# Fidelity assumption: 1-min historical bars carry no bid/ask. The bot scores
# spread (20% weight) and hard-filters on it. We assume a fixed spread. A wider
# value makes the spread-quality score worse and is more conservative.
ASSUMED_SPREAD = 0.02

ENTRY_CUTOFF = (15, 50)   # no new entries at/after 3:50 PM ET

# ---------------------------------------------------------------------------
# Universe: symbol -> sector. Extracted from the live Research Brain file
# advisor_universe_latest.json (150 symbols). "OTHER" is sector-cap exempt.
# ---------------------------------------------------------------------------
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

        # TradeStation brokerage model -> realistic commissions + margin.
        self.set_brokerage_model(BrokerageName.TRADE_STATION, AccountType.MARGIN)

        # SPY drives the volatility-regime gate.
        self.spy = self.add_equity("SPY", Resolution.MINUTE)
        self.spy.set_data_normalization_mode(DataNormalizationMode.ADJUSTED)
        self.spy.set_slippage_model(ConstantSlippageModel(0.001))
        self.spy_symbol = self.spy.symbol

        # Tradeable universe.
        self.symbols = []
        self.sector = {}
        for ticker, sec in UNIVERSE.items():
            try:
                eq = self.add_equity(ticker, Resolution.MINUTE)
                eq.set_data_normalization_mode(DataNormalizationMode.ADJUSTED)
                eq.set_slippage_model(ConstantSlippageModel(0.001))
                self.symbols.append(eq.symbol)
                self.sector[eq.symbol] = sec
            except Exception as e:
                self.debug(f"Could not add {ticker}: {e}")

        # Per-day state
        self.current_day   = None
        self.day_open      = {}     # symbol -> day's opening price
        self.day_volume    = {}     # symbol -> cumulative day volume
        self.last_close    = {}     # symbol -> most recent close (rolls to prev_close)
        self.prev_close    = {}     # symbol -> prior trading day's close
        self.spy_day_high  = None
        self.spy_day_low   = None
        self.spy_prev_close = None
        self.spy_last_close = None

        # Position / cooldown state
        self.pos_extreme    = {}    # symbol -> running high (long) / low (short)
        self.last_exit_time = {}    # symbol -> datetime of last exit

        # Daily loss guard
        self.day_start_equity = None
        self.halted_today     = False

        # Forced flatten 10 min before close (= 3:50 PM ET).
        self.schedule.on(
            self.date_rules.every_day(self.spy_symbol),
            self.time_rules.before_market_close(self.spy_symbol, 10),
            self.eod_flatten,
        )

    # =======================================================================
    def on_data(self, data):
        t = self.time

        # ---- day rollover -------------------------------------------------
        if t.date() != self.current_day:
            self.current_day = t.date()
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

        # ---- update SPY day state ----------------------------------------
        if data.contains_key(self.spy_symbol) and data[self.spy_symbol] is not None:
            b = data[self.spy_symbol]
            self.spy_day_high = b.high if self.spy_day_high is None else max(self.spy_day_high, b.high)
            self.spy_day_low  = b.low  if self.spy_day_low  is None else min(self.spy_day_low,  b.low)
            self.spy_last_close = b.close

        # ---- update per-symbol day state ---------------------------------
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
                self.log(f"{t} DAILY LOSS LIMIT HIT -- trading halted for the day")

        # ---- exits always run --------------------------------------------
        self._manage_exits(data)

        if self.halted_today:
            return
        if (t.hour, t.minute) >= ENTRY_CUTOFF:
            return
        if regime == "EXTREME":
            return  # volatility gate blocks all new entries

        # ---- entries: one long + one short per bar (mirrors the 2 bots) --
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

            last = data[s].close            # mirrors the bot's per-cycle "last"
            avg = holding.average_price
            if avg <= 0:
                continue

            if holding.is_long:
                self.pos_extreme[s] = last if s not in self.pos_extreme \
                    else max(self.pos_extreme[s], last)
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
                if (last <= hard) or (be is not None and last <= be) \
                   or (trail is not None and last <= trail):
                    self.liquidate(s)
                    self.last_exit_time[s] = self.time
                    self.pos_extreme.pop(s, None)

            elif holding.is_short:
                self.pos_extreme[s] = last if s not in self.pos_extreme \
                    else min(self.pos_extreme[s], last)
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
                if (last >= hard) or (be is not None and last >= be) \
                   or (trail is not None and last >= trail):
                    self.liquidate(s)
                    self.last_exit_time[s] = self.time
                    self.pos_extreme.pop(s, None)

    # =======================================================================
    def _try_enter(self, data, regime, side):
        open_count = sum(1 for s in self.symbols if self.portfolio[s].invested)
        if open_count >= MAX_POSITIONS:
            return
        exposure = sum(abs(self.portfolio[s].holdings_value)
                       for s in self.symbols if self.portfolio[s].invested)
        if exposure >= MAX_TOTAL_EXPOSURE:
            return

        # Rank all passing candidates by composite score, descending.
        candidates = []
        for s in self.symbols:
            if self.portfolio[s].invested:
                continue
            le = self.last_exit_time.get(s)
            if le is not None and (self.time - le).total_seconds() < COOLDOWN_MINUTES * 60:
                continue
            if not (data.contains_key(s) and data[s] is not None):
                continue
            if s not in self.prev_close or self.prev_close[s] <= 0:
                continue          # day 1 of the backtest: no prior close yet
            if s not in self.day_open:
                continue
            last = data[s].close
            score = self._score(side, last, self.day_open[s], self.prev_close[s],
                                 self.day_volume.get(s, 0.0), regime)
            if score is not None and score >= MIN_SCORE:
                candidates.append((s, score, last))
        candidates.sort(key=lambda x: x[1], reverse=True)

        # Current sector exposure (for the max-2-per-sector cap).
        sec_count = {}
        for s in self.symbols:
            if self.portfolio[s].invested:
                sc = self.sector.get(s, "OTHER")
                sec_count[sc] = sec_count.get(sc, 0) + 1

        strategy_capital = min(self.portfolio.total_portfolio_value, MAX_TOTAL_EXPOSURE)
        max_dollars = strategy_capital * MAX_POSITION_PCT

        for s, score, last in candidates:
            sc = self.sector.get(s, "OTHER")
            if sc != "OTHER" and sec_count.get(sc, 0) >= MAX_SECTOR_POSITIONS:
                continue
            if side == "LONG":
                limit_price = round(last + LIMIT_OFFSET, 2)
                qty = int(max_dollars // limit_price)
            else:
                qty = int(max_dollars // last)
            if qty < 1:
                continue
            if exposure + qty * last > MAX_TOTAL_EXPOSURE:
                continue
            # Entries modeled as market orders (the bot's last +/- $0.10 limit
            # is marketable); slippage model approximates the cross + slippage.
            self.market_order(s, qty if side == "LONG" else -qty)
            return  # one entry per side per bar

    # =======================================================================
    def _score(self, side, last, day_open, prev_close, day_volume, regime):
        """Composite entry score per spec sec 4. Returns None if a hard filter fails."""
        spread = ASSUMED_SPREAD
        net_change_pct = (last - prev_close) / prev_close * 100.0

        if side == "LONG":
            min_price, min_chg, min_vol, max_spread = 20.0, 0.25, 500_000.0, 0.25
            if regime == "HIGH":
                max_spread *= 0.7
                min_vol *= 1.5
                min_chg *= 1.5
            # hard filters
            if last < min_price:            return None
            if net_change_pct < min_chg:    return None
            if day_volume < min_vol:        return None
            if spread > max_spread:         return None
            # component scores
            mom = _clamp(net_change_pct / 2.5, 0.0, 1.0) if net_change_pct > 0 else 0.0
            pa = self._price_action_long(last, day_open, prev_close)
        else:  # SHORT
            min_price, max_chg, min_vol, max_spread = 20.0, -0.60, 1_000_000.0, 0.15
            min_below_open, min_below_pc = 0.20, 0.20
            if regime == "HIGH":
                max_spread *= 0.7
                min_vol *= 1.5
                max_chg *= 1.5      # deeper drop required (more negative)
            if last < min_price:            return None
            if net_change_pct > max_chg:    return None
            if day_volume < min_vol:        return None
            if spread > max_spread:         return None
            if day_open > 0 and last >= day_open:       return None
            if prev_close > 0 and last >= prev_close:   return None
            below_open = (day_open - last) / day_open * 100.0 if day_open > 0 else 0.0
            if below_open < min_below_open: return None
            below_pc = (prev_close - last) / prev_close * 100.0 if prev_close > 0 else 0.0
            if below_pc < min_below_pc:     return None
            mom = _clamp(abs(net_change_pct) / 2.5, 0.0, 1.0) if net_change_pct < 0 else 0.0
            pa = self._price_action_short(last, day_open, prev_close)

        vol_s = self._volume_score(day_volume, min_vol)
        spr_s = self._spread_score(spread, max_spread)
        return (W_MOMENTUM * mom + W_VOLUME * vol_s
                + W_SPREAD * spr_s + W_PRICEACTION * pa)

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
            above_pct = (last - open_price) / open_price * 100.0
            score += _clamp(above_pct / 2.0, 0.0, 0.3)
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
            below_pct = (open_price - last) / open_price * 100.0
            score += _clamp(below_pct / 2.0, 0.0, 0.3)
        elif open_price > 0 and last > open_price:
            score -= 0.2
        if prev_close > 0 and last < prev_close:
            score += 0.2
        return _clamp(score, 0.0, 1.0)
