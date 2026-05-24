# ============================================================================
# Strategy Lab -- H4: Faithful Zarattini ORB on Stocks in Play (Stage 4)
# ============================================================================
# Stage 3 APPROVED by Rhett 2026-05-24. Spec source of truth:
#   strategy-research/STRATEGY_LAB.md  (master)
#   strategy-research/H4_spec_for_audit.md  (standalone copy)
#
# Spec summary (every choice tagged: [PAPER] / [QC-IMPL-CHOICE] / [OUR-ADD]):
#   - [PAPER] Universe = NYSE+NASDAQ, ~7,000 stocks
#   - [PAPER] + [OUR-ADD] opening price > $7 (paper: $5; lab: $7 marginability buffer)
#   - [PAPER] 14-day avg volume >= 1,000,000 shares/day
#   - [PAPER] 14-day Wilder ATR > $0.50
#   - [PAPER] Relative Volume = today_first_5m_vol / mean(prior 14d first_5m_vol) >= 100%
#   - [OUR-ADD] exclude leveraged ETFs; listed >= 1 year
#   - [PAPER] Tradeable per day = top 20 by Relative Volume
#   - [PAPER] OR window = 9:30-9:35 ET (5 one-minute bars timestamped 9:31..9:35)
#   - [PAPER] Direction: OR close > open -> LONG, OR close < open -> SHORT, doji -> skip
#   - [PAPER] Entry = stop-market at OR high (long) / OR low (short)
#   - [PAPER] Protective stop = 0.10 x 14d ATR from entry
#   - [PAPER] No profit target; hold to session close
#   - [OUR-ADD G1] Flatten at 3:50 PM ET (paper: 4:00 PM)
#   - [PAPER] Risk = 1% of capital allocated to that position
#   - [QC-IMPL-CHOICE] Slice = equity / 20 -> $5,000 at $100k equity, $50 max risk/position
#         (Picked over Claude-Opus's $20k slice because 20 x $200 = $4,000 breaches G2.)
#   - [PAPER] Max leverage account-wide 4x
#   - [OUR-ADD safeguard] Per-position notional cap = equity * (4 / 20) = 0.2 x equity
#   - [OUR-ADD G2] Halt for the day if intraday P&L <= -$2,000
#   - [OUR-ADD] TradeStation brokerage model, Margin account, $0 commission
#   - [OUR-ADD] Slippage = 2.5 bps per fill (Stage 3 decision; 5 bps sensitivity later)
#   - [OUR-ADD safeguard] Daily diagnostic log: universe / top20 / breakouts / stop_outs / held
# ============================================================================

from AlgorithmImports import *
from datetime import time as dt_time, timedelta
import math


# --- Constants (every constant traces to a spec row) ---
SLIPPAGE              = 0.00025         # 2.5 bps per fill (Stage 3 decision)
STARTING_CASH         = 100_000         # $300k actual scaled down to $100k for lab
PRICE_FLOOR           = 7.0             # paper says >$5; lab uses $7 [OUR-ADD]
ADV_FLOOR             = 1_000_000       # 14d avg volume >= 1M shares [PAPER]
ATR_FLOOR             = 0.50            # 14d ATR > $0.50 [PAPER]
RELVOL_FLOOR          = 1.0             # >= 100% [PAPER]
TOP_N                 = 20              # tradeable set per day [PAPER]
ATR_PERIOD            = 14              # 14d Wilder [PAPER]
ATR_STOP_MULT         = 0.10            # 0.10 x ATR stop [PAPER]
SLICE_RISK_PCT        = 0.01            # 1% of slice [PAPER]
ACCOUNT_LEV_CAP       = 4.0             # FINRA intraday [PAPER]
PER_POS_LEV_CAP       = ACCOUNT_LEV_CAP / TOP_N   # 0.2x equity per position [OUR-ADD safeguard]
DAILY_LOSS_CAP        = 2_000.0         # G2 [OUR-ADD]
MIN_LISTING_DAYS      = 365             # listed >= 1 year [OUR-ADD]

# Leveraged ETFs excluded [OUR-ADD]. Not exhaustive; covers the common 2x/3x names.
LEVERAGED_ETF_BLOCKLIST = frozenset([
    "TQQQ","SQQQ","SOXL","SOXS","SPXL","SPXS","UPRO","SPXU","TNA","TZA",
    "FAS","FAZ","LABU","LABD","TMF","TMV","UVXY","SVXY","VXX","UVIX","SVIX",
    "BOIL","KOLD","NUGT","DUST","JNUG","JDST","ERX","ERY","YINN","YANG",
    "DRN","DRV","URTY","SRTY","TECL","TECS","CURE","RXD","UDOW","SDOW",
    "QLD","QID","SSO","SDS","DDM","DXD","BIB","BIS","ROM","REW",
])


class H4_ZarattiniORB(QCAlgorithm):

    # ---------------- initialize ----------------

    def initialize(self):
        self.set_start_date(2016, 1, 1)
        self.set_end_date(2021, 12, 31)                  # train window [OUR-ADD]
        self.set_cash(STARTING_CASH)
        self.set_brokerage_model(BrokerageName.TRADE_STATION, AccountType.MARGIN)

        # Stamp daily bars at midnight so MOO/MOC orders submit in valid window (H0 v2 fix).
        self.settings.daily_precise_end_time = False

        self.universe_settings.resolution = Resolution.MINUTE
        self.universe_settings.extended_market_hours = False
        self.add_universe(self.coarse_select, self.fine_select)

        # SPY anchors the schedule to actual trading days. Excluded from trading.
        self.spy = self.add_equity("SPY", Resolution.MINUTE).symbol

        self.schedule.on(self.date_rules.every_day(self.spy),
                         self.time_rules.at(9, 30),
                         self.on_session_open)

        # on_or_close fires at 9:36 (NOT 9:35) so the 9:35 minute bar has already
        # been processed by on_data and the OR is fully accumulated.
        self.schedule.on(self.date_rules.every_day(self.spy),
                         self.time_rules.at(9, 36),
                         self.on_or_close)

        self.schedule.on(self.date_rules.every_day(self.spy),
                         self.time_rules.at(15, 50),
                         self.on_eod_flatten)                # G1

        self.symbol_data = {}
        self.day_halted = False
        self.day_start_equity = STARTING_CASH
        self.diag = self._fresh_diag()

        # Warm up enough days for ATR(14) + 14d volume window.
        self.set_warmup(timedelta(days=30))

    def _fresh_diag(self):
        return dict(universe=0, top20=0, breakouts=0, stop_outs=0, held_to_close=0)

    # ---------------- Universe selection ----------------

    def coarse_select(self, coarse):
        """[PAPER] price > $7 ($5 + OUR-ADD), exclude leveraged ETFs, fundamentals required.
        Dollar-volume gate is a cheap proxy for the 14-d 1M-share filter; the strict
        14-d test still runs later in passes_paper_filters()."""
        out = []
        floor_dollar = PRICE_FLOOR * ADV_FLOOR  # $7 * 1M = $7M -- floor on today's $vol
        for c in coarse:
            if not c.has_fundamental_data:
                continue
            if c.symbol.value.upper() in LEVERAGED_ETF_BLOCKLIST:
                continue
            if c.price < PRICE_FLOOR:
                continue
            if c.dollar_volume < floor_dollar:
                continue
            out.append(c.symbol)
        return out

    def fine_select(self, fine):
        """[PAPER] exchange = NYSE/NASDAQ, [OUR-ADD] listed >= 1 year."""
        out = []
        today = self.time.date()
        for f in fine:
            if f.security_reference.exchange_id not in ("NYS", "NAS"):
                continue
            ipo = f.security_reference.ipo_date
            if ipo is None:
                continue
            if (today - ipo.date()).days < MIN_LISTING_DAYS:
                continue
            out.append(f.symbol)
        return out

    def on_securities_changed(self, changes):
        for sec in changes.added_securities:
            sym = sec.symbol
            if sym == self.spy:
                continue
            sec.set_slippage_model(ConstantSlippageModel(SLIPPAGE))
            sec.set_data_normalization_mode(DataNormalizationMode.ADJUSTED)
            # QC's TradeStation brokerage model defaults to RegT 2x (50% initial margin).
            # Paper p.9 uses 4x intraday FINRA margin. Set it explicitly per security.
            sec.set_leverage(ACCOUNT_LEV_CAP)
            self.symbol_data[sym] = SymbolData(self, sym)
        for sec in changes.removed_securities:
            sym = sec.symbol
            if sym in self.symbol_data:
                sd = self.symbol_data.pop(sym)
                sd.dispose()
            if self.portfolio[sym].invested:
                self.liquidate(sym, "universe removal")

    # ---------------- Daily lifecycle ----------------

    def on_session_open(self):
        """9:30 ET. Reset per-day state."""
        self.day_halted = False
        self.day_start_equity = self.portfolio.total_portfolio_value
        self.diag = self._fresh_diag()
        self.diag["universe"] = len(self.symbol_data)
        for sd in self.symbol_data.values():
            sd.reset_for_new_day()

    def on_or_close(self):
        """9:36 ET. OR finalized -> rank by RelVol -> place top-20 breakout orders."""
        if self.is_warming_up or self.day_halted:
            return

        eligible = []
        for sym, sd in self.symbol_data.items():
            if not sd.is_ready():
                continue
            if not sd.passes_paper_filters():
                continue
            relvol = sd.relvol()
            if relvol is None or relvol < RELVOL_FLOOR:
                continue
            direction = sd.or_direction()
            if direction == 0:        # doji -> skip [PAPER]
                continue
            eligible.append((relvol, sym, direction, sd))

        eligible.sort(key=lambda x: -x[0])
        top = eligible[:TOP_N]
        self.diag["top20"] = len(top)

        for _, sym, direction, sd in top:
            self._place_breakout(sym, sd, direction)

        # After ranking, push today's OR volume into history for tomorrow's denominator.
        for sd in self.symbol_data.values():
            if sd.or_finalized and sd.or_volume > 0:
                sd.or_vol_hist.add(float(sd.or_volume))

    def _place_breakout(self, sym, sd, direction):
        """Sizing per spec:
            shares = (slice * 1%) / (0.10 * ATR), capped by per-position notional cap.
        QC's Python order API can't always match overloads when args come through as Decimal
        rather than float; explicit float()/int() coercion below avoids that.
        """
        equity = float(self.portfolio.total_portfolio_value)
        slice_cap = equity / TOP_N                          # $5k at $100k [QC-IMPL-CHOICE]
        risk_dollars = slice_cap * SLICE_RISK_PCT           # $50 [PAPER 1% of slice]
        stop_dist = ATR_STOP_MULT * float(sd.atr_value)     # 0.10 x ATR [PAPER]
        if stop_dist <= 0:
            return
        shares_by_risk = int(risk_dollars / stop_dist)
        if shares_by_risk <= 0:
            return

        if direction > 0:
            trigger = float(sd.or_high)
            stop_price = trigger - stop_dist
        else:
            trigger = float(sd.or_low)
            stop_price = trigger + stop_dist
        if trigger <= 0:
            return

        per_pos_notional_cap = equity * PER_POS_LEV_CAP     # 0.2 * equity [OUR-ADD safeguard]
        shares_by_lev = int(per_pos_notional_cap / trigger)
        shares = int(min(shares_by_risk, shares_by_lev))
        if shares <= 0:
            return
        qty = shares if direction > 0 else -shares

        ticket = self.stop_market_order(sym, qty, trigger, tag="H4 entry")
        sd.pending_entry_id = ticket.order_id
        sd.pending_stop_price = float(stop_price)
        sd.pending_direction = direction

    def on_order_event(self, oe):
        if oe.status != OrderStatus.FILLED:
            return
        sym = oe.symbol
        if sym not in self.symbol_data:
            return
        sd = self.symbol_data[sym]

        # Entry filled -> attach protective stop at 0.10 x ATR.
        if sd.pending_entry_id is not None and oe.order_id == sd.pending_entry_id:
            self.diag["breakouts"] += 1
            filled_qty = int(oe.fill_quantity)
            protective = self.stop_market_order(
                sym, -filled_qty, float(sd.pending_stop_price), tag="H4 protective stop")
            sd.protective_stop_id = protective.order_id
            sd.entry_filled = True
            sd.pending_entry_id = None
            return

        # Protective stop filled -> stop-out.
        if sd.protective_stop_id is not None and oe.order_id == sd.protective_stop_id:
            self.diag["stop_outs"] += 1
            sd.entry_filled = False
            sd.protective_stop_id = None
            return

    def on_data(self, data):
        if self.is_warming_up:
            return

        # G2 — hard daily loss cap. Checked every minute.
        if not self.day_halted:
            day_pl = self.portfolio.total_portfolio_value - self.day_start_equity
            if day_pl <= -DAILY_LOSS_CAP:
                self.day_halted = True
                self._cancel_all_open()
                self._flatten_all("G2 daily cap")
                self.log(f"G2 HIT @ {self.time}: day_pl={day_pl:.2f}")
                return

        # Build OR bars from the 9:31-9:35 minute bars.
        for sym, sd in self.symbol_data.items():
            if sym in data.bars:
                bar = data.bars[sym]
                if bar is not None:
                    sd.on_minute_bar(bar, self.time)

    def on_eod_flatten(self):
        """G1 — 3:50 PM ET. Cancel pending, flatten everything, log diagnostics."""
        if self.is_warming_up:
            return
        self._cancel_all_open()
        flattened = 0
        for sym in list(self.symbol_data.keys()):
            if self.portfolio[sym].invested:
                self.liquidate(sym, "H4 EOD flatten (G1)")
                flattened += 1
        self.diag["held_to_close"] = flattened

        end_eq = self.portfolio.total_portfolio_value
        day_pl = end_eq - self.day_start_equity
        self.log(
            f"DIAG {self.time.date()} "
            f"universe={self.diag['universe']} "
            f"top20={self.diag['top20']} "
            f"breakouts={self.diag['breakouts']} "
            f"stop_outs={self.diag['stop_outs']} "
            f"held_to_close={self.diag['held_to_close']} "
            f"eod_equity={end_eq:.2f} "
            f"day_pl={day_pl:.2f} "
            f"halted={self.day_halted}"
        )

    def _cancel_all_open(self):
        for order in self.transactions.get_open_orders():
            self.transactions.cancel_order(order.id)

    def _flatten_all(self, reason):
        for sym in list(self.symbol_data.keys()):
            if self.portfolio[sym].invested:
                self.liquidate(sym, reason)


# ============================================================================
# Per-symbol state holder
# ============================================================================

class SymbolData:

    def __init__(self, algo, symbol):
        self.algo = algo
        self.symbol = symbol

        # 14-day Wilder ATR on daily bars [PAPER]
        self.atr = AverageTrueRange(ATR_PERIOD, MovingAverageType.WILDERS)
        algo.register_indicator(symbol, self.atr, Resolution.DAILY)

        # 14d daily volume window (for the 1M-share filter)
        self.daily_vol = RollingWindow[float](ATR_PERIOD)
        # 14d first-5-min volume window (for RelVol denominator)
        self.or_vol_hist = RollingWindow[float](ATR_PERIOD)

        # Daily consolidator to capture realized daily volume
        self.daily_consolidator = TradeBarConsolidator(timedelta(days=1))
        self.daily_consolidator.data_consolidated += self._on_daily_bar
        algo.subscription_manager.add_consolidator(symbol, self.daily_consolidator)

        # Warm the ATR + daily-volume window from history so this symbol is
        # tradeable on its first day in the universe (instead of waiting 14 days).
        try:
            hist = algo.history(symbol, ATR_PERIOD + 5, Resolution.DAILY)
            if hist is not None and not hist.empty and symbol in hist.index.get_level_values(0):
                for _, row in hist.loc[symbol].iterrows():
                    self.daily_vol.add(float(row["volume"]))
                    # ATR auto-warms via register_indicator + history events; no manual update needed.
        except Exception as ex:
            algo.debug(f"history warmup failed for {symbol}: {ex}")

        # Per-day state
        self.reset_for_new_day()

    def dispose(self):
        try:
            self.algo.subscription_manager.remove_consolidator(self.symbol, self.daily_consolidator)
        except Exception:
            pass

    def reset_for_new_day(self):
        self.or_open  = None
        self.or_high  = -math.inf
        self.or_low   =  math.inf
        self.or_close = None
        self.or_volume = 0.0
        self.or_finalized = False
        self.opening_price = None
        self.pending_entry_id = None
        self.pending_stop_price = None
        self.pending_direction = 0
        self.protective_stop_id = None
        self.entry_filled = False

    def _on_daily_bar(self, sender, bar):
        self.daily_vol.add(float(bar.volume))

    def on_minute_bar(self, bar, now):
        """Accumulate the 5 one-minute bars covering 9:30-9:35 (bars stamped 9:31..9:35)."""
        local = now.time()
        if local <= dt_time(9, 30) or local > dt_time(9, 35):
            return
        if self.or_open is None:
            self.opening_price = bar.open
            self.or_open = bar.open
        self.or_high = max(self.or_high, bar.high)
        self.or_low  = min(self.or_low,  bar.low)
        self.or_close = bar.close
        self.or_volume += float(bar.volume)
        if local >= dt_time(9, 35):
            self.or_finalized = True

    @property
    def atr_value(self):
        return float(self.atr.current.value) if self.atr.is_ready else 0.0

    def is_ready(self):
        return (self.atr.is_ready
                and self.daily_vol.is_ready
                and self.or_vol_hist.is_ready)

    def passes_paper_filters(self):
        """Hard filters from the paper, evaluated at 9:36 ET each day."""
        if self.opening_price is None or self.opening_price < PRICE_FLOOR:
            return False
        if self.daily_vol.count == 0:
            return False
        avg_vol = sum([v for v in self.daily_vol]) / self.daily_vol.count
        if avg_vol < ADV_FLOOR:
            return False
        if self.atr_value <= ATR_FLOOR:
            return False
        return True

    def relvol(self):
        if not self.or_finalized or self.or_vol_hist.count == 0:
            return None
        denom = sum([v for v in self.or_vol_hist]) / self.or_vol_hist.count
        if denom <= 0:
            return None
        return self.or_volume / denom

    def or_direction(self):
        if self.or_open is None or self.or_close is None:
            return 0
        if self.or_close > self.or_open:
            return 1
        if self.or_close < self.or_open:
            return -1
        return 0
