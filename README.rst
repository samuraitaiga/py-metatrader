****************************************
py-metatrader
****************************************

py-metatrader 0.0.1

Released: 30-May-2015

=============
Introduction
=============

py-metatrader is a python package that provides interfaces to metatrader4(mt4).
`metatrader4`_  is a trading platform that can automate trading(fx, stock, etc...) by your own program(ExpertAdvisor in mt4).

you can automate simuration(backtest in mt4), CI  EA development , etc... by using this library.

currently works with Python 2.7.

contributing and porting is welcome.


=============
Feature
=============

At the moment, py-metatrader supports:

* backtest
* optimization

The goal of py-metatrader is to support execute all feature of metatrader4 from this library.


============
Installation
============

Install via `pip`_:

.. code-block:: bash

    $ pip install metatrader

Install from source:

.. code-block:: bash

    $ git clone https://github.com/samuraitaiga/py-metatrader.git
    $ cd py-metatrader
    $ python setup.py install


============
ChangeLogs
============
* 0.0.1

  * first release. backtest and optimization from python.


============
Usage
============


Backtest:

.. code-block:: python

    from metatrader.mt4 import initizalize
    from metatrader.backtest import BackTest
    
    # point mt4 install folder
    initizalize('C:\\Program Files\\FXCM MetaTrader 4')

    # specify backtest period by datetime format
    from_date = datetime(2014, 9, 1)
    to_date = datetime(2015, 1, 1)

    ea_name = 'Moving Average'

    # create ea param by dict.
    param = {
             'Lots': {'value': 0.1},
             'MaximumRisk': {'value': 0.02},
             'DecreaseFactor': {'value': 3.0},
             'MovingPeriod': {'value': 12},
             'MovingShift': {'value': 6}
             }
    # create backtest object
    backtest = BackTest(ea_name, param, 'USDJPY', 'M5', from_date, to_date)

    # run backtest
    ret = backtest.run()

    # you can get result from result object
    # for example you can print gross profit
    print ret.gross_profit

.. _metatrader4: http://www.metatrader4.com/
.. _pip: http://www.pip-installer.org/
