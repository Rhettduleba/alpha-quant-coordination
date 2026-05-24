# ============================================================================
# Strategy Lab -- H0: Framework sanity check (buy-and-hold SPY)  v2
# ============================================================================
# This is NOT a real strategy. It exists to verify our QuantConnect framework
# (TradeStation brokerage model, slippage, sizing logic) produces the correct
# result on a known-good baseline BEFORE we trust any active strategy result.
#
# Expected result on 2016-01-01 to 2021-12-31:
#   Net return roughly +85% to +95% (SPY's actual adjusted total return over
#   the window typically lands in that range).
#
# If our framework returns materially less, or shows unexplained fees -- that
# is a configuration bug we have to find before any active strategy result
# can be trusted.
#
# v2 fix (2026-05-24): added `self.settings.daily_precise_end_time = False`.
# H0 v1 errored with "BrokerageModel declared unable to submit order: MOO
# submission time is invalid. Valid local times are 06:00-09:29." because
# daily bars stamp at 16:00 by default, so QC submitted MOO orders at the
# wrong time. Setting `daily_precise_end_time = False` stamps daily bars at
# midnight, so MOO for next-day open submits in the broker's valid window.
# ============================================================================

from AlgorithmImports import *

SLIPPAGE      = 0.0005
STARTING_CASH = 100_000


class H0_BuyHoldSPY(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2016, 1, 1)
        self.set_end_date(2021, 12, 31)
        self.set_cash(STARTING_CASH)
        self.set_brokerage_model(BrokerageName.TRADE_STATION, AccountType.MARGIN)

        # Fix for v1 MOO-timing error
        self.settings.daily_precise_end_time = False

        self.spy = self.add_equity("SPY", Resolution.DAILY)
        self.spy.set_data_normalization_mode(DataNormalizationMode.ADJUSTED)
        self.spy.set_slippage_model(ConstantSlippageModel(SLIPPAGE))

        self.bought = False

    def on_data(self, data):
        if self.bought:
            return
        if not (data.contains_key(self.spy.symbol) and data[self.spy.symbol] is not None):
            return
        self.set_holdings(self.spy.symbol, 1.0)
        self.bought = True

    def on_end_of_algorithm(self):
        equity = self.portfolio.total_portfolio_value
        ret = (equity - STARTING_CASH) / STARTING_CASH * 100.0
        self.log(f"END | equity=${equity:,.2f} | return={ret:.2f}% | "
                 f"expected approximately +85% to +95%")
