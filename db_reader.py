'''
Created on 2014/7/17

@author: USER
'''

from stock_profile import *  
from PyDbLite import Base
'''
k = Base('2325.db')
k.open()

for r in k:
    print r
'''   
one_dream = Base('overall.db')
one_dream.open()
print one_dream.fields
stock = Stock_Profile('2002') 
current = stock.get_result(0)[0]
stocks = [r for r in one_dream if (r['buy']==1) and (r['date']==current)]
for s in stocks:
    print s['date'], s['buy'], s['stock']