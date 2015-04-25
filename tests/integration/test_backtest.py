'''
Created on 2015/04/15

@author: Taiga
'''

from metatrader.mt4 import initizalize
from metatrader.backtest import BackTest
from datetime import datetime
import logging

def test_backtest():
    logging.basicConfig(level=logging.DEBUG)
    initizalize('C:\\Program Files\\FXCM MetaTrader 4')

    from_date = datetime(2014, 9, 1)
    to_date = datetime(2015, 1, 1)
#     ea_name = 'Chronicle_Strategy'
#     param = {
#              'type': {'value': 2},
#              'chronicle_value': {'value': 0.05, 'max': 0.2, 'interval': 0.05},
#              'profit_pips': {'value': 200},
#              'loss_pips': {'value': 50},
#              'timeframe': {'value': 5},
#              'one_lot_base': {'value': 10000},
#              }

    ea_name = 'Moving Average'
    param = {
             'Lots': {'value': 0.1},
             'MaximumRisk': {'value': 0.02, 'max': 0.2, 'interval': 0.05},
             'DecreaseFactor': {'value': 3.0},
             'MovingPeriod': {'value': 12},
             'MovingShift': {'value': 6}
             }


    backtest = BackTest(ea_name, param, 'USDJPY', 'M5', from_date, to_date)

    ret = backtest.run()
    assert ret.profit == 88.73
    assert ret.profit_factor == 1.02
    assert ret.expected_payoff == 0.07
    assert ret.max_drawdown == 763.72
    assert ret.max_drawdown_rate == 7.47
    assert ret.gross_profit == 5640.39
    assert ret.gross_loss == -5551.66
    assert ret.total_trades == 1232

