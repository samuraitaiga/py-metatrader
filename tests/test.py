#coding: utf-8
'''
Created on 2015/04/15

@author: Taiga
'''
from nose.core import run

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    import os
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    run('tests.integration.test_backtest')
