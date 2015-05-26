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
    assert ret.largest_profit_trade == 156.46
    assert ret.largest_loss_trade == -86.91
    assert ret.average_profit_trade == 18.55
    assert ret.average_loss_trade == -5.98
    assert ret.modeling_quality_percentage == 90.0
    assert ret.max_consecutive_profit == 272.96
    assert ret.max_consecutive_profit_count == 3
    assert ret.max_consecutive_loss == -178.94 
    assert ret.max_consecutive_loss_count == 30
    assert ret.max_consecutive_wins_count == 5
    assert ret.max_consecutive_wins_profit == 71.06
    assert ret.max_consecutive_losses_count ==30
    assert ret.max_consecutive_losses_loss ==-178.94
    assert ret.profit_trades == 304
    assert ret.profit_trades_rate == 24.68
    assert ret.loss_trades == 928
    assert ret.loss_trades_rate == 75.32
    assert ret.ave_consecutive_wins == 1
    assert ret.ave_consecutive_losses == 4
    assert ret.short_positions == 549
    assert ret.short_positions_rate == 23.13
    assert ret.long_positions == 683
    assert ret.long_positions_rate == 25.92
