'''
Created on 2014/6/18

@author: pascal
'''
import csv
import os.path
from PyDbLite import Base
from stock_profile import *  
import time
class CsvBatchCommander(object):
    def __init__(self, csv_file_name, actor):
        sm = StockManager()
        stock = Stock_Profile('2002') 
        current = stock.get_result(0)[0]
        with open(csv_file_name, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for task in row:
                    if current == sm.getLatestDate(task):
                        print 'Already done! ', task
                        break
                    else:
                        try:
                            s = Stock_Profile(task)
                            s.recent_data_a(30)[-1][0]
                            actor.run(task)
                        except:
                            pass
'''
    def retry(self, csv_file_name, actor):
        sm = StockManager()
        stock = Stock_Profile('2002') 
        current = stock.get_result(0)[0]
        with open(csv_file_name, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for task in row:
                    if current == sm.getLatestDate(task):
                        print 'Already done! ', task
                    else:
                        try:
                            s = Stock_Profile(task)
                            s.recent_data_a(30)[-1][0]
                            actor.run(task)
                        except:
                            pass
'''

class Actor(object):
    def run(self, tid):
        raise NotImplementedError


class StockActor(Actor):
    
    def run(self, tid):
        
        sm = StockManager()
        print tid, ' alf'
        stock = Stock_Profile(tid)
        if stock.recent_price(30) == 'EXCLUDE DIVIDEND':
            pass
        else:
            alert = stock.get_alerts(2)[0]
            date = alert[0]
            bs = alert[1]
            ss = alert[2]
            b = 0 #default
            s = 0 #default
            pre_status = sm.getCurStatus(tid)
            state = pre_status #default
            if (bs == 1) and (pre_status == 0):
                b = 1
                state = 1
            if (ss == 1) and (pre_status == 1):
                s = 1
                state = 0
            sc = {}
            sc['date'] = date
            sc['buySig'] = bs
            sc['sellSig'] = ss
            sc['state'] = state
            sc['buy'] = b
            sc['sell'] = s
            sm.updateStock(tid, sc)
            

class StockManager(object):
    def __init__(self):
        self.getSummary()

    def dbname(self, sid):
        return sid + '.db'

    def getStock(self, sid):
        sname = self.dbname(sid)
        exist = os.path.isfile(sname)
        db = ''
        if (exist):
            #read db
            db = Base(sname)
            db.open()
        else:
            #create a new db
            db = Base(sname)
            db.create('date','buySig','sellSig', 'state', 'buy', 'sell' ,mode="override")
            db.open()
        return db

    def updateStock(self, sid, sc):
        db = self.getStock(sid)
        sdb = self.sdb
        if sc['date'] in [r['date'] for r in db]:
            pass
        else:
            db.insert(date = sc['date'],buySig = sc['buySig'],sellSig = sc['sellSig'], state = sc['state'], buy = sc['buy'], sell = sc['sell'])
            db.commit()
            print '[stock] # ', sid, '  updating'
            conflict = [r for r in sdb if ((r['date'] == sc['date']) and (r['stock'] == sid))]
            if len(conflict) == 0:
                sdb.insert(date = sc['date'], stock = sid ,state = sc['state'],  buy = sc['buy'], sell = sc['sell'])
                sdb.commit()
                print '[summary] creating ', sid
            update = [r for r in sdb if ((r['date'] != sc['date']) and (r['stock'] == sid))]
            if len(update)>0:
                sdb.update(update[0], date = sc['date'], state = sc['state'],  buy = sc['buy'], sell = sc['sell'])
                sdb.commit()
                print '[summary] updating ', sid

    def getSummary(self):
        self.sdb = Base('overall.db')
        self.sdb.open()
        return self.sdb
    
    def getCurStatus(self, sid):
        db = self.sdb
        match = [r for r in db if r['stock'] == sid]
        if len(match) == 0:
            return 0
        else:
            return match[0]['state']
    def getLatestDate(self, sid):
        db = self.sdb
        records = [r for r in db if r['stock']==sid]
        if len(records) > 0:
            return records[0]['date']
        else:
            return '69/06/19'

if __name__ == '__main__':
    b = StockActor()
    a = CsvBatchCommander('alf.csv', b)

