'''
Created on 2015/01/31

@author: Taiga
'''

from mt4 import get_mt4
from mt4 import DEFAULT_MT4_NAME
import logging

def has_divtag_with_style(tag):
    return tag.name == 'div' and tag.has_attr('style')

class BaseReport(object):
    """
    Notes:
      this is a base class that has input of backtest
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
    """
    def __init__(self, backtest):
        self.ea_name = backtest.ea_name
        self.param = backtest.param
        self.symbol = backtest.symbol
        self.from_date = backtest.from_date
        self.to_date = backtest.to_date
        self.model = backtest.model
        self.spread = backtest.spread

class BacktestReport(BaseReport):
    """
    Note:
      backtest report class.
    Attributes:
      initial_deposit(int): initial deposit of backtest of optimization
    """
    # result
    profit = None
    profit_factor = None
    expected_payoff = None
    max_drawdown = None
    max_drawdown_rate = None
    relative_drawdown = None
    relative_drawdown_rate = None
    abs_drawdown = None
    abs_drawdown_rate = None
    gross_profit = None
    gross_loss = None
    total_trades = None
    largest_profit_trade = None
    largest_loss_trade = None
    average_profit_trade = None
    average_loss_trade = None
    modeling_quality_percentage = None
    max_consecutive_profit_count = None
    max_consecutive_profit = None
    max_consecutive_loss_count = None
    max_consecutive_loss = None
    max_consecutive_wins_count = None
    max_consecutive_wins_profit = None
    max_consecutive_losses_count = None
    max_consecutive_losses_loss = None
    profit_trades = None
    profit_trades_rate = None
    loss_trades = None
    loss_trades_rate = None
    ave_consecutive_wins = None
    ave_consecutive_losses = None
    short_positions = None
    short_positions_rate = None
    long_positions = None
    long_positions_rate = None

    def __init__(self, backtest, alias=DEFAULT_MT4_NAME):
        from bs4 import BeautifulSoup
        import re
        super(BacktestReport, self).__init__(backtest)

        report_file = get_report_abs_path(backtest.ea_name, alias=alias)
        with open(report_file, 'r') as fp:
            raw_html = fp.read()
            
        b_soup = BeautifulSoup(raw_html)
        summary_in_table = b_soup.find_all('table')[0]
        tds = summary_in_table.find_all('td')
        
        for index, td in enumerate(tds):
            if td.text == 'Initial deposit':
                self.initial_deposit = float(tds[index+1].text)
            if td.text == 'Modelling quality':
                modeling_quality_percentage_str = re.sub('%', '', tds[index+1].text)
                self.modeling_quality_percentage = float(modeling_quality_percentage_str)
            elif td.text == 'Total net profit':
                self.profit = float(tds[index+1].text)
            elif td.text == 'Gross profit':
                self.gross_profit = float(tds[index+1].text)
            elif td.text == 'Gross loss':
                self.gross_loss = float(tds[index+1].text)
            elif td.text == 'Profit factor':
                self.profit_factor = float(tds[index+1].text)
            elif td.text == 'Expected payoff':
                self.expected_payoff = float(tds[index+1].text)
            elif td.text == 'Absolute drawdown':
                self.abs_drawdown = float(tds[index+1].text)
            elif td.text == 'Maximal drawdown':
                data, rate = self.get_data_and_rate(tds[index+1].text)
                self.max_drawdown_rate = rate
                self.max_drawdown = data
            elif td.text == 'Relative drawdown':
                data, rate = self.get_data_and_rate(tds[index+1].text)
                self.relative_drawdown_rate = rate
                self.relative_drawdown = data
            elif td.text == 'Total trades':
                self.total_trades = int(tds[index+1].text)
            elif td.text == 'Short positions (won %)':
                data, rate = self.get_data_and_rate(tds[index+1].text)
                self.short_positions_rate = rate
                self.short_positions = data
            elif td.text == 'Long positions (won %)':
                data, rate = self.get_data_and_rate(tds[index+1].text)
                self.long_positions_rate = rate
                self.long_positions = data
            elif td.text == 'Profit trades (% of total)':
                data, rate = self.get_data_and_rate(tds[index+1].text)
                self.profit_trades_rate = rate
                self.profit_trades = int(data)
            elif td.text == 'Loss trades (% of total)':
                data, rate = self.get_data_and_rate(tds[index+1].text)
                self.loss_trades_rate = rate
                self.loss_trades = int(data)
            elif td.text == 'Largest':
                if tds[index+1].text == 'profit trade':
                    self.largest_profit_trade = float(tds[index+2].text)
                if tds[index+3].text == 'loss trade':
                    self.largest_loss_trade = float(tds[index+4].text)
            elif td.text == 'Average':
                if tds[index+1].text == 'profit trade':
                    self.average_profit_trade = float(tds[index+2].text)
                elif tds[index+1].text == 'consecutive wins':
                    self.ave_consecutive_wins = int(tds[index+2].text)
                if tds[index+3].text == 'loss trade':
                    self.average_loss_trade = float(tds[index+4].text)
                elif tds[index+3].text == 'consecutive losses':
                    self.ave_consecutive_losses = int(tds[index+4].text)
            elif td.text == 'Maximum':
                if tds[index+1].text == 'consecutive wins (profit in money)':
                    token = self.split_to_tokens(tds[index+2].text)
                    self.max_consecutive_wins_count = int(token[0])
                    self.max_consecutive_wins_profit = float(token[1])
                if tds[index+3].text == 'consecutive losses (loss in money)':
                    token = self.split_to_tokens(tds[index+4].text)
                    self.max_consecutive_losses_count = int(token[0])
                    self.max_consecutive_losses_loss = float(token[1])
            elif td.text == 'Maximal':
                if tds[index+1].text == 'consecutive profit (count of wins)':
                    token = self.split_to_tokens(tds[index+2].text)
                    self.max_consecutive_profit = float(token[0])
                    self.max_consecutive_profit_count = int(token[1])
                if tds[index+3].text == 'consecutive loss (count of losses)':
                    token = self.split_to_tokens(tds[index+4].text)
                    self.max_consecutive_loss = float(token[0])
                    self.max_consecutive_loss_count = int(token[1])


    def get_data_and_rate(self, line):
        import re
        from exception import InvalidReportFormat
        formatted_str = re.sub('(\(|\))', '', line)
        values = formatted_str.split(r' ')

        if len(values) != 2:
            raise InvalidReportFormat('value of Maximal drawdown contains more than 2 values')
        
        for value in values:
            if re.match('.*\%$',value):
                rate = re.sub(r'%','',value)
                rate = float(rate)
            else:
                data = float(value)            
        return data, rate
    
    def split_to_tokens(self, line):
        '''
        Notes:
          split consecutive xxx into two tokens.
          e.g. 1 (123.45) => (1, 123.45)
               123.45 (1) => (123.45, 1)
        '''
        import re
        from exception import InvalidReportFormat

        formatted_str = re.sub('(\(|\))', '', line)
        values = formatted_str.split(r' ')

        if len(values) != 2:
            raise InvalidReportFormat('value of Maximal drawdown contains more than 2 values')
        
        return values

class ShortReport(BaseReport):
    """
    @todo: implement __hash__ and __eq__ to do set operation
    Notes:
      this class has a result of backtest included in optimization report
    Attributes:
      param(dict(str:str)): ea parameter name and value dict
      profit(float): profit
      total_trades(int): num of trades
      profit_factor(float): profit factor
      expected_payoff(float): expected payoff
      max_drawdown(float): max drawdown of deposit
      max_drawdown_rate(float): max drawdown rate of deposit
      initial_deposit(int): initial deposit of backtest of optimization
    """
    
    def __init__(self, back_test, **kwargs):
        super(ShortReport, self).__init__(back_test)
        result = kwargs.copy()

        self.param = result.pop('param')        
        self.profit = result.pop('profit')
        self.total_trades = result.pop('total_trades')
        self.profit_factor = result.pop('profit_factor')
        self.expected_payoff = result.pop('expected_payoff')
        self.max_drawdown = result.pop('max_drawdown')
        self.max_drawdown_rate = result.pop('max_drawdown_rate')
        self.initial_deposit = result.pop('initial_deposit')

class OptimizationReport():
    """
    Note:
      this class has short reports
    """
    reports = []
    
    def _is_valid_format(self, raw_html):
        from bs4 import BeautifulSoup

        is_valid = False

        b_soup = BeautifulSoup(raw_html)
        report_titles = b_soup.find_all(has_divtag_with_style)
        
        for title in report_titles:
            if title.text == 'Optimization Report':
                if self._get_initial_deposit(raw_html) != 0:
                    is_valid = True
        return is_valid

    def _get_initial_deposit(self, raw_html):
        from bs4 import BeautifulSoup

        initial_deposit = 0
        b_soup = BeautifulSoup(raw_html)
        conditions = b_soup.find_all('table')[0]

        trs = conditions.find_all('tr')

        for tr in trs:
            tds = tr.find_all('td')
            if tds[0].text == 'Initial deposit':
                initial_deposit = float(tds[1].text)

        return initial_deposit
    
    def _get_param_from_text(self, text):
        '''
        Note:
          create param dict from text in td title attribute in optimization report.
        Args:
          text(string): 
            e.g.: x=2; y=0.2; z=true;
        Returns:
          param(dict): ea param names and values.
        '''
        param = {}
        param_array = text.split(r';')
        # delete last element because its None data
        param_array.pop(-1)

        for p in param_array:
            name_value = p.split(r'=')
            name = name_value[0]
            value = name_value[1]
            
            param[name] = value
            
        return param
    
    def _get_results(self, backtest, raw_html):
        from bs4 import BeautifulSoup
        results = []
        initial_deposit = self._get_initial_deposit(raw_html)

        b_soup = BeautifulSoup(raw_html)
        results_in_table = b_soup.find_all('table')[1]
        trs = results_in_table.find_all('tr')

        # delete first tr, because it is category name
        trs.pop(0)
        
        for tr in trs:
            tds = tr.find_all('td')
            param = None
            profit = None
            total_trades = None
            profit_factor = None
            expected_payoff = None
            max_drawdown = None
            max_drawdown_rate = None
            
            for i, td in enumerate(tds):
                if i == 0:
                    param_raw_text = td.attrs.pop('title')
                    param = self._get_param_from_text(param_raw_text)
                elif i == 1:
                    profit = float(td.text)
                elif i == 2:
                    total_trades = int(td.text)
                elif i == 3:
                    profit_factor = float(td.text)
                elif i == 4:
                    expected_payoff = float(td.text)
                elif i == 5:
                    max_drawdown = float(td.text)
                elif i == 6:
                    max_drawdown_rate = float(td.text)
            
            short_report = ShortReport(backtest,
                                       param=param,
                                       profit=profit,
                                       total_trades=total_trades,
                                       profit_factor=profit_factor,
                                       expected_payoff=expected_payoff,
                                       max_drawdown=max_drawdown,
                                       max_drawdown_rate=max_drawdown_rate,
                                       initial_deposit=initial_deposit)
            results.append(short_report)
        return results

    def __init__(self, backtest, alias=DEFAULT_MT4_NAME):
        from exception import InvalidReportFormat
        
        report_file = get_report_abs_path(backtest.ea_name, alias=alias)

        with open(report_file, 'r') as fp:
            raw_html = fp.read()

        if self._is_valid_format(raw_html):
            try:
                self.results = self._get_results(backtest, raw_html)                
            except KeyError:
                err_msg = 'optimization report seems invlid format'
                logging.error(err_msg)
                raise
        else:
            raise InvalidReportFormat(report_file, r'"Optimization Report" not found in html')
        
def get_report_abs_path(ea_name, alias=DEFAULT_MT4_NAME):
    import os
    mt4 = get_mt4(alias=alias)
    report = os.path.join(mt4.appdata_path, '%s.htm' % ea_name)
    return report
