'''
Created on 2014/6/18

@author: USER
'''
from PyDbLite import Base
db = Base('overall.db')


db.create('date', 'stock', 'state', 'buy', 'sell' ,mode="override")
db.commit()


'''
db.open()
print db.fields
for r in db:
    print r['date'], r['state'], r['stock'], r['buy'], r['sell']
'''