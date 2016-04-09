'''
Created on 2014/6/18

@author: pascal
'''
from PyDbLite import Base

class Sim:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass


class StockEvent:
    
    def __init__(self):
        pass
    

class Stock:
    def __init__(self):
        self.status = []
        self.status['hold'] = '0'
        self.status['release'] = '1'
        self.action = []
        self.action['buy'] = '2'
        self.action['sell'] = '3'
    def action(self, act):
        if act == 'buy':
            pass
    