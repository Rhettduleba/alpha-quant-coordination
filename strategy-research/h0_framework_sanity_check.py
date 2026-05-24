# ============================================================================
# Strategy Lab -- H0: Framework sanity check (buy-and-hold SPY)
# ============================================================================
# This is NOT a real strategy. It exists to verify our QuantConnect framework
# (TradeStation brokerage model, slippage, sizing logic) produces the correct
# result on a known-good baseline BEFORE we trust any active strategy result.
#
# Expected result on 2016-01-01 to 2021-12-31:
#   Net return roughly +85% to +95% (SPY's actual total return over the
#   window, including reinvested dividends, was around +120% including
#   dividends; adjusted-data buy-and-hold typically lands ~+90%-+120%).
#
# If our framework returns materially less (say <+50%) or shows unexplained
# fees -- that's a configuration bug we have to find before any active
# strategy result can be trusted. Every prior backtest (H1 -72%, H2 -5.7%,
# H3 -99.97%) is suspect until H0 passes.
# ============================================================================

from AlgorithmImports import *

# Match the same settings used in our active strategy backtests
SLIPPAGE      = 0.0005   # 0.05% per fill -- same as H1/H2/H3
STARTING_CASH = 100_000


class H0_BuyHoldSPY(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2016, 1, 1)
        self.set_end_date(2021, 12, 31)
        self.set_cash(STARTING_CASH)
        self.set_brokerage_model(BrokerageName.TRADE_STATION, AccountType.MARGIN)

        self.spy = self.add_equity("SPY", Resolution.DAILY)
        self.spy.set_data_normalization_mode(DataNormalizationMode.ADJUSTED)
        self.spy.set_slippage_model(ConstantSlippageModel(SLIPPAGE))

        self.bought = False

    def on_data(self, data):
        if self.bought:
            return
        if not (data.contains_key(self.spy.symbol) and data[self.spy.symbol] is not None):
            return
        # 100% of equity into SPY, one-time, never sell.
        self.set_holdings(self.spy.symbol, 1.0)
        self.bought = True

    def on_end_of_algorithm(self):
        equity = self.portfolio.total_portfolio_value
        ret = (equity - STARTING_CASH) / STARTING_CASH * 100.0
        self.log(f"END | equity=${equity:,.2f} | return={ret:.2f}% | "
                 f"expected approximately +85% to +95%")
