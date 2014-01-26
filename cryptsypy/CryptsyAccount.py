# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from pyapi import Request,RequestPrivate
from CryptsyInfo import Info
import time

# <codecell>

class Account():
    def __init__(self, Platform = 'crypsty', public_key = '', private_key = '',):
        """
            This class is designed to hold all information specific to
                a user account on cryptsy.com.
            Be carefull the secret (priv_key)
        """
        self._init_Requests(Platform = Platform)
        self.marketid = {}
        self.Pairs = {}
        self._init_mid_pairs()
        self.CryptoAdresses = {}
        self.CryptoAdresses['LTC'] = 'LMGgCFsxJBjkPwAW9bn5MnZG4vyTGv1aJr'
        self.pub_key = public_key
        self.priv_key = private_key
        #self.Request = private_request(Account = self)
        
        self.MyTrades = {}
        self.MyOrders = {}
        self.MyTransactions = {}
        self.TradeHisory = {}
        self.Depths = {}
        return None
    
    def _init_Requests(self, Platform):
        PlatformInfo = Info()
        self.Request = RequestPrivate(Account = self, Info = PlatformInfo)
        self.pubRequest = Request(Info = PlatformInfo)
        return 0
    
    def _init_mid_pairs(self,):
        md = self.pubRequest.fetch('marketdatav2')['markets']
        for p in md.keys():
            pair = tuple(p.split('/'))
            mid = md[p]['marketid']
            self.Pairs[mid] = pair
            self.marketid[pair] = mid
            self.OpenOrders[pair] = md[p]['buyorders']
        del md
        return 0
    
    def update_Info(self,):
        return self.Request.fetch('getinfo')
    
    def update_MarketsInfo(self,):
        return self.Request.fetch('getmarkets')
    
    def update_MyTransactions(self,):
        m_trans = self.Request.fetch('mytransactions')
        for trans in m_trans:
            self.MyTransactions[trans.pop('timestamp')] = trans
        return 0
    
    def update_TradeHistory(self, market):
        """market is a tuple"""
        ##self.marketid is to do!!!
        mid = self.marketid(market)
        history = self.Request.fetch('markettrades',params={'marketid':mid})
        pair = self.Pairs[mid]
        self.TradeHistory[pair] = history
        return 0
    
    def update_OpenOrders(self, market):
        """market is a tuple"""
        mid = self.marketid(market)
        o_orders = self.Request.fetch('marketorders',params={'marketid':mid})
        ##check the form of o_orders
        
        print o_orders
        #self.OpenOrders[self.Pairs[mid]] = 
        return 0
    
    def update_MyTrades(self, market = None, limit = 200):
        if market:
            mid = self.marketid[market]
            pair = self.Pairs[mid]
            method = 'mytrades'
            params = {'marketid':mid, 'limit':limit}
        else:
            method = 'allmytrades'
            params = {}
        m_trades = self.Request.fetch(method,params = params)
        #check format of m_trades
        print m_trades
        #self.MyTrades[pair] = m_trades
        return 0
    
    def update_MyOrders(self, market = None):
        if market:
            mid = self.marketid[market]
            pair = self.Pairs[mid]
            method = 'myorders'
            params = {'marketid':mid}
        else:
            method = 'allmyorders'
            params = {}
        m_orders = self.Request.fetch(method, params = params)
        ##check the format.
        #self.MyOrders[pair] = ...
        print m_orders
        return 0
    
    def update_Depths(self, market):
        mid = self.marketid[market]
        pair = self.Pairs[mid]
        depths = self.Request.fetch('depth',params={'marketid':mid})
        ##check format
        #self.Dephts[pair] = ...
        return 0
    
    def CreateOrder(self, market, order_type, quantity, price):
        mid = self.marketid[market]
        pair = self.Pairs[mid]
        params = {
                  'marketid':mid,
                  'ordertype':order_type,
                  'quantity':quantity,
                  'price':price
                  }
        ##check if funds are sufficient, if minimal value is exceded, etc
        if self._order_possible(params):
            now = time.time()
            oid = self.Request.fetch('createorder',params = params)
            self.MyOpenOrders[oid] = params
            self.MyOpenOrders[oid][u'timestamp'] = now
        return 0
    
    def _order_possible(self, params):
        ##to do
        #if ok
        #    return True
        #else:
        #    return False
        return True
    
    def CancelOrder(self, **orders):
        if 'orderid' in orders:
            c_o = self.Request.fetch('cancelorder',params={'orderid':orderid})
            print c_o
            #if successfull:
            #    if orderid in self.MyOpenOrders:
            #        self.MyOpenOrders.pop(orderid)
        if 'marketid' in orders:
            mid = orders['marketid']
            c_o = self.Request.fetch('cancelmarketorders',params={'marketid':mid})
            print c_o
            #if successfull:
            #    remove them from self.MyOpenOrders (use marketid)
        if not len(orders.keys()):
            all_c_o = self.Request.fetch('cancelallorders')
            ##check the output
            ##update self.MyOpenOrders
            print all_c_o
        return 0
    
    def get_fees(self, ordertype, quantity, price):
        """does this mean same fees for all markets?"""
        params = {
                  'ordertype': ordertype,
                  'quantity': quantity,
                  'price': price
                  }
        ret = self.Request.fetch('calculatefees',params=params)
        print ret
        return 0
    
    def _update_Fees(self,):
        """"""
        #update self.Fees
        #self.get_fees('
        return 0
        
    
    

