'''
Created on 2015/02/08

@author: Taiga
'''

class InvalidReportFormat(Exception):
    '''
    exception when backtest or optimization report format is invalid
    '''
    
    def __init__(self, report_file, err_msg):
        '''
        Constructor
        '''
        self.report_file = report_file
        self.err_msg = err_msg
    
    def __str__(self):
        return '%s seems invalid format. %s not found' % (self.report_file, self.err_msg)