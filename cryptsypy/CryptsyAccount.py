from pyapi import Request,RequestPrivate
#this is going to be it
#from pyapi import AccountStructure
from CryptsyInfo import Info
import time

# <codecell>

#pur account into pyapi and inherit the specific platform account
#from the general class.
class Account():
#class Account(AccountStructure):
    #it does not make much sense to have the info in a class...
    def __init__(self, PlatformInfo = Info(), public_key = '', private_key = '',):
        """
            This class is designed to hold all information specific to
                a user account on cryptsy.com.
            Be carefull the secret (priv_key)
        """
        #AccountStructure.__init__(self,
        #                          PlatfromInfo = PlatformInfo,
        #                          public_key = public_key,
        #                          private_key = private_key,
        #                          )
        
        #
        self._init_Requests(PlatformInfo = PlatformInfo)
        self.marketid = {}
        self.Pairs = {}
        self._init_mid_pairs()
        self.CryptoAdresses = {}
        self.CryptoAdresses['LTC'] = 'LMGgCFsxJBjkPwAW9bn5MnZG4vyTGv1aJr'
        #
        self.pub_key = public_key
        #
        self.priv_key = private_key
        #self.Request = private_request(Account = self)
        
        self.MyTrades = {}
        self.MyOrders = {}
        self.MyTransactions = {}
        self.TradeHisory = {}
        self.Depths = {}
        
        
        ##Those have to adapted to the specific platform
        self.command_account_info = 'getinfo'
        self.command_market_info = 'getmarkets'
        self.command_trades_history = ''
        self.command_open_orders = ''
        #not used
        self.command_my_transactions = ''
        self.command_my_trades = ''
        self.command_my_orders = 'allmyorders'
        self.command_new_order = 'createorder'
        self.command_cancel_order = ''
        self.command_cancel_all_orders = ''
        self.parameter_ordertype = 'ordertype'
        self.parameter_market = 'marketid'
        self.parameter_quantity = 'quantity'
        self.parameter_price = 'price'
        self.parameter_order_id = ''
        self.parameter_market_id = ''
        
        return None
    #
    def _init_Requests(self, PlatformInfo):
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
    #
    def update_Info(self,):
        return self.Request.fetch('getinfo')
    #
    def update_MarketInfo(self,):
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
        #what is this again?
        mid = self.marketid[market]
        pair = self.Pairs[mid]
        depths = self.Request.fetch('depth',params={'marketid':mid})
        ##check format
        #self.Dephts[pair] = ...
        return 0
    #
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
            c_o = self.Request.fetch('cancelorder',params={'orderid':orders['orderid']})
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
        
    
    

