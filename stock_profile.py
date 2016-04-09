# -*- coding: utf-8 -*-
'''
Created on 2014/6/14

@author: fpy
'''
from grs import Stock
import grs
import math
from grs import TWSENo

class Stock_Profile():

    def __init__(self, stockId):
        '''
        Constructor
        '''
        self.conf = [30,30]
        self.offset = 0
        self.stockId = stockId
        self.raw = self.recent_data(43)
        st = TWSENo()
        self.lookup = st.all_stock
      
    def has_data(self):
        if len(self.raw) < 40:
            return False
        else:
            return True  
    def set_offset(self, o):
        self.offset = o
        
    def get_stock_id(self):
        return self.stockId
    
    def get_stock_name(self):
        result = ''
        try:
            result = self.lookup[str(self.stockId)]
        except:
            result = "not in the list"
        return result
    
    def get_current_date_pointer(self):
        return self.date
    
    def get_result(self, offset):
        self.offset = offset
        date = self.recent_data_a(offset)[-1][0]      
        price = self.recent_data_a(offset)[-1][6]
        up = self.Up()
        down = self.Dn()
        result = [date, price, up, down]
        return  result
    
    
    def get_alerts(self, days):
        buys = []
        sales = []
        dates = []
        result = []
        for day in range(days):
            data = self.get_result(day)
            price = data[1]
            up = data[2]
            down = data[3]
            date = data[0]
            buy = 0
            sale = 0
            if price > up:
                buy = 1
            if price < down:
                sale = 1
            result.append((date, buy, sale))

        return result
    
    def recent_data_a(self, dates):
        if dates == 0:
            return [self.raw[-1]]
        else:
            return self.raw[-(dates+self.offset+1):-(1+self.offset)]
    
    def recent_data(self, dates):
        result = []
        try:
            stock = Stock(self.stockId)                # �w�]�����Ӥ�����
            #stock.moving_average(60)
            #IndexError: list index out of range  # ��Ƥ���
            #print len(stock.raw)                       # �^�� 51 �ӭ�
            #stock.plus_mons(2)                   # �b���@�Ӥ���
            #print stock.moving_average(38)             # �p�⦨�\
            #result = stock.raw[-(dates+self.offset+1):-(1+self.offset)]
            result = stock.raw[-(dates+self.offset):]    #15/11/27 modified by alf
            print 'got it'
        except grs.error.StockNoError:
            print 'grs fail~'        
        return result


    def recent_data_alf(self, dates):
        result = []
        try:
            stock = Stock(self.stockId)                # �w�]�����Ӥ�����
            #stock.moving_average(60)
            #IndexError: list index out of range  # ��Ƥ���
            #print len(stock.raw)                       # �^�� 51 �ӭ�
            #stock.plus_mons(2)                   # �b���@�Ӥ���
            #print stock.moving_average(38)             # �p�⦨�\
            result = stock.raw[-(dates+1):-(1)]
            print 'got it'
        except grs.error.StockNoError:
            print 'grs fail~'        
        return result

    
    def recent_price(self, days):
        result = self.raw[-(days+self.offset+1):-(1+self.offset)]
        try:
            result = [float(r[6]) for r in result]
        except:
            result = 'EXCLUDE DIVIDEND'
        return result
    
    def alf(self, flt, ndig):
        return round(flt, ndig) 
    def average(self, s):
        if len(s) > 0:
            av = sum(s) * 1.0 / len(s)
            #print "stock_"+self.stockId, "average: ", av
            return av
        else:
            return 0
    def get_average(self, dates):
        return self.average(self.recent_price(dates))
        

    def std(self, s):
        avg = self.average(s)
        variance = map(lambda x: (x - avg)**2, s)
        standard_deviation = math.sqrt(self.average(variance))
        #print "stock_"+ self.sID, "std: ", standard_deviation
        return standard_deviation
    
    def get_std(self, days):
        return self.alf(self.std(self.recent_price(days)),2)
    
    def MB(self, days):
        return self.alf(self.average(self.recent_price( days)),2)

    def MD(self, days):
        return self.std(self.recent_price( days))

    def Up(self):
        day1 = self.conf[0]
        day2 = self.conf[1]
        u = self.alf(self.MB( day1) + 2* self.MD(day2),2)
        return u

    def Dn(self):
        day1 = self.conf[0]
        day2 = 20#self.conf[1]
        d = self.MB( day1) - 2* self.MD(day2)
        return self.alf(d, 2)