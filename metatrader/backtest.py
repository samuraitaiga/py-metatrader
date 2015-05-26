# -*- coding: utf-8 -*-
'''
Created on 2015/01/25

@author: samuraitaiga
'''
import logging
import os
from mt4 import get_mt4
from mt4 import DEFAULT_MT4_NAME
from __builtin__ import str

class BackTest(object):
    """
    Attributes:
      ea_name(string): ea name
      param(dict): ea parameter
      symbol(string): currency symbol. e.g.: USDJPY
      from_date(datetime.datetime): backtest from date
      to_date(datetime.datetime): backtest to date
      model(int): backtest model 
        0: Every tick
        1: Control points
        2: Open prices only
      spread(int): spread
      optimization(bool): optimization flag. optimization is enabled if True
      replace_report(bool): replace report flag. replace report is enabled if True

    """
    def __init__(self, ea_name, param, symbol, period, from_date, to_date, model=0, spread=5, replace_repot=True):
        self.ea_name = ea_name
        self.param = param
        self.symbol = symbol
        self.from_date = from_date
        self.to_date = to_date
        self.model = model
        self.spread = spread
        self.replace_report = replace_repot

    def _prepare(self, alias=DEFAULT_MT4_NAME):
        """
        Notes:
          create backtest config file and parameter file
        """
        self._create_conf(alias=alias)
        self._create_param(alias=alias)

    def _create_conf(self, alias=DEFAULT_MT4_NAME):
        """
        Notes:
          create config file(.conf) which is used parameter of terminal.exe
          in %APPDATA%\\MetaQuotes\\Terminal\\<UUID>\\tester
          
          file contents goes to 
            TestExpert=SampleEA
            TestExpertParameters=SampleEA.set
            TestSymbol=USDJPY
            TestPeriod=M5
            TestModel=0
            TestSpread=5
            TestOptimization=true
            TestDateEnable=true
            TestFromDate=2014.09.01
            TestToDate=2015.01.05
            TestReport=SampleEA
            TestReplaceReport=false
            TestShutdownTerminal=true
        """

        mt4 = get_mt4(alias=alias)
        conf_file = os.path.join(mt4.appdata_path, 'tester', '%s.conf' % self.ea_name)

        # shutdown_terminal must be True.
        # If false, popen don't end and backtest report analyze don't start.
        shutdown_terminal = True

        with open(conf_file, 'w') as fp:
            fp.write('TestExpert=%s\n' % self.ea_name)
            fp.write('TestExpertParameters=%s.set\n' % self.ea_name)
            fp.write('TestSymbol=%s\n' % self.symbol)
            fp.write('TestModel=%s\n' % self.model)
            fp.write('TestSpread=%s\n' % self.spread)
            fp.write('TestOptimization=%s\n' % str(self.optimization).lower())
            fp.write('TestDateEnable=true\n')
            fp.write('TestFromDate=%s\n' % self.from_date.strftime('%Y.%m.%d'))
            fp.write('TestToDate=%s\n' % self.to_date.strftime('%Y.%m.%d'))
            fp.write('TestReport=%s\n' % self.ea_name)
            fp.write('TestReplaceReport=%s\n' % str(self.replace_report).lower())
            fp.write('TestShutdownTerminal=%s\n' % str(shutdown_terminal).lower())

    def _create_param(self, alias=DEFAULT_MT4_NAME):
        """
        Notes:
          create ea parameter file(.set) in %APPDATA%\\MetaQuotes\\Terminal\\<UUID>\\tester
        Args:
          ea_name(string): ea name
        """
        mt4 = get_mt4(alias=alias)
        param_file = os.path.join(mt4.appdata_path, 'tester', '%s.set' % self.ea_name)

        with open(param_file, 'w') as fp:
            for k in self.param:
                values = self.param[k].copy()
                value = values.pop('value')
                fp.write('%s=%s\n' % (k, value))
                if self.optimization:
                    if values.has_key('max') and values.has_key('interval'):
                        fp.write('%s,F=1\n' % k)
                        fp.write('%s,1=%s\n' % (k, value))
                        interval = values.pop('interval')
                        fp.write('%s,2=%s\n' % (k,interval))
                        maximum = values.pop('max')
                        fp.write('%s,3=%s\n' % (k,maximum))
                    else:
                        # if this value won't be optimized, write unused dummy data for same format.
                        fp.write('%s,F=0\n' % k)
                        fp.write('%s,1=0\n' % k)
                        fp.write('%s,2=0\n' % k)
                        fp.write('%s,3=0\n' % k)
                else:
                    if type(value) == str:
                        # this ea arg is string. then don't write F,1,2,3 section in config
                        pass
                    else:
                        # write unused dummy data for same format.
                        fp.write('%s,F=0\n' % k)
                        fp.write('%s,1=0\n' % k)
                        fp.write('%s,2=0\n' % k)
                        fp.write('%s,3=0\n' % k)


    def _get_conf_abs_path(self, alias=DEFAULT_MT4_NAME):
        mt4 = get_mt4(alias=alias)
        conf_file = os.path.join(mt4.appdata_path, 'tester', '%s.conf' % self.ea_name)
        return conf_file

    def run(self, alias=DEFAULT_MT4_NAME):
        """
        Notes:
          run backtest
        """
        from report import BacktestReport

        self.optimization = False

        self._prepare(alias=alias)
        bt_conf = self._get_conf_abs_path(alias=alias)
    
        mt4 = get_mt4(alias=alias)
        mt4.run(self.ea_name, conf=bt_conf)
    
        ret = BacktestReport(self)
        return ret

    def optimize(self, alias=DEFAULT_MT4_NAME):
        """
        """
        from report import OptimizationReport

        self.optimization = True
        self._prepare(alias=alias)
        bt_conf = self._get_conf_abs_path(alias=alias)
    
        mt4 = get_mt4(alias=alias)
        mt4.run(self.ea_name, conf=bt_conf)
        
        ret = OptimizationReport(self)
        return ret


def load_from_file(dsl_file):
    pass
