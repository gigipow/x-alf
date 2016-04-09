# -*- coding: utf-8 -*-
'''
Created on 2014/6/9

@author: fpy
'''
from flask import Flask
from flask import request
from flask import render_template
from PyDbLite import Base
from stock_profile import *  
from flask import Markup
from cindy import *
import markdown
 
app = Flask(__name__)

'''
@app.route('/')
def index():
    username = request.cookies.get('Username')
    if username is None:
        return 'Hello, ALF'
    else:
        return 'Hello, Java' 
'''
@app.route('/welcome', methods=['POST'])
def welcome():
    db = Base('alf.db')
    db.create('name','pwd',mode="open") #override
    user = request.form['Username']
    passwd = request.form['password1']
    db.insert(name=user,pwd=passwd)
    db.commit()
    return 'welcome ' + user

def run():
    sa = StockActor()
    batch = CsvBatchCommander('alf.csv', sa)



@app.route('/alf', methods=['POST'])
def alf():
    db = Base('alf.db')
    db.open()
    user = request.form['Username']
    pwd = request.form['password']
    user_verf = [r['password'] for r in db if r['name'] == user]
    if len(user_verf) > 0:
        if user_verf[0] == pwd:
            return 'Hello, ' + user
    else:
        return 'Who are you!!!'
        

@app.route('/reg')
def signup():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/users')
def users():
    db = Base('alf.db')
    db.open()
    users = []
    for r in db:
        n = r['name']
        p = r['pwd']
        users.append((n, p))
    return render_template('user.html', users=users)

@app.route('/stock/<stockid>')
def show_stock_profile(stockid):
    # show the user profile for that stock
    stock = Stock_Profile(stockid)
    return render_template('stock_30.html', stock=stock)

@app.route('/buy')
def buy():
    # show the user profile for that stock
    sm = StockManager()
    stock = Stock_Profile('2002') 
    current = stock.get_result(0)[0]
    db = Base('overall.db')
    db.open()
    stocks = [r for r in db if (r['buy']==1) and (r['date']==current)]
    return render_template('buy.html', stocks=stocks)

@app.route('/sell')
def sell():
    # show the user profile for that stock
    sm = StockManager()
    stock = Stock_Profile('2002') 
    current = stock.get_result(0)[0]
    db = Base('overall.db')
    db.open()
    stocks = [r for r in db if r['sell']==1 and (r['date']==current)]
    return render_template('buy.html', stocks=stocks)

@app.route('/host')
def host():
    # show the user profile for that stock
    db = Base('overall.db')
    db.open()
    #stocks = [r for r in db if r['state']==1]
    stocks = [r for r in db]
    return render_template('all.html', stocks=stocks)



@app.route('/')
def frontpage():
    run()
    return render_template('frontpage.html')

@app.route('/help')
def helps():
    return render_template('help.html', **locals())


def helps_old():
    content = """
Quick Start
=======

Search
-------

* Enter the stock id
* Click the search icon

Buy Signals
----------

* List all the stocks (the subset of All My Fav) with buy signal 

Sell Signals
----------

* List all the stocks transited from buy signal to sell signal

All My Fav
----------

* List all stocks you like


"""
    content = Markup(markdown.markdown(content))
    return render_template('help_old.html', **locals())


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')