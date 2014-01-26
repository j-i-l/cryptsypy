# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from pyapi import Request
from CryptsyInfo import Info
import time

# <codecell>

#to do: The goal is to make the status class not platform specific
class Status():
    def __init__(self, Platform = 'cryptsy',):# Api = Request()):
        """
            Arguments:
                - Platform: either the name of the paltform or 
                    the path to a config file.
                    Permitted names for the platform are:
                        ['btc-e','crypsty']
        """
        self._init_Request(Platform) #defs self.Api
        self.MarketCurrent = {}
        self.OrdersCurrent = {}
        self.PricesLast = {}
        self.Currencies = []
        self.Pairs = []
        self.marketid = {}
        ##call self.update_info before
        self.update_info()
        self._init_marketid() #defs self.marketid
        ##are not really needed to be dicts yet
        ##to do: get the fees through request.
        self.fee = 0.997
        
        
        return None
    
    def _init_Request(self, Platform):
        self.Request = Request(Info = Info())
        return 0
    
    def update_info(self,):
        self.get_marketdata()
        self._order_Pairs()
        self.update_PricesLast()
        #hm...
        #self.get_orderdata()
        for curs in self.MarketCurrent.keys():
            for cur in curs:
                if cur not in self.Currencies:
                    self.Currencies.append(cur)
            if curs not in self.Pairs:
                self.Pairs.append(curs)
        self.update_PricesLast()
        return 0
        
    def update_PricesLast(self,):
        for pair in self.Pairs:
            pairMarket = self.MarketCurrent[pair]
            try:
                self.PricesLast[pair] = {'price':float(pairMarket['buyorders'][0]['price']) if pairMarket['secondarycode'] == pair[1] else 1/float(pairMarket['sellorders'][0]['price']),
                                         'timestamp': self.MarketCurrent[pair]['timestamp']
                                        }
                self.PricesLast[tuple(list(pair)[::-1])] = {'price':1/float(pairMarket['sellorders'][0]['price']) if pairMarket['secondarycode'] == pair[1] else float(pairMarket['buyorders'][0]['price']),
                                                            'timestamp': self.MarketCurrent[pair]['timestamp']
                                                           }
            except TypeError:
                pass
        return 0
        
    def _order_Pairs(self,):
        for i in range(len(self.Pairs)):
            pair = tuple([
                            self.MarketCurrent[pair]['primarycode'],
                            self.MarketCurrent[pair]['secondarycode']
                            ])
            self.Pairs[i] = pair   
            #self.Pairs[pair]
            #self.Pairs[pair]['primary'] = self.MarketCurrent[pair]['primarycode']
            #self.Pairs[pair]['secondary'] = self.MarketCurrent[pair]['secondarycode']
            #self.Pairs[pair]['marketid'] = self.MarketCurrent[pair]['marketid']
        return 0
    
    def _init_marketid(self, ):
        for pair in self.MarketCurrent:
            self.marketid[pair] = int(self.MarketCurrent[pair]['marketid'])
        return 0
            
        
    def get_marketdata(self, marketid = None):
        kwargs = {}
        if not marketid:
            kwargs['method'] = 'marketdatav2'
            #kwargs['params'] = {}
            #market = self.Api.fetch('marketdatav2')[u'markets']
        else:
            kwargs['method'] = 'singlemarketdata'
            kwargs['params'] = {'marketid':marketid}
            #market = self.Api.fetch('singlemarketdata',{'marketid':marketid})[u'markets']
        now = time.time()
        market = self.Request.fetch(**kwargs)[u'markets']
        #market = self.Api.public_request({'method':'marketdatav2'})[u'markets']
        self.MarketCurrent = {}
        for pair in market:
            t_pair = tuple(pair.split('/'))
            self.MarketCurrent[t_pair] = market[pair]
            self.MarketCurrent[t_pair]['timestamp'] = now
        return 0
        
    def get_orderdata(self, marketid = None):
        kwargs = {}
        if not marketid:
            kwargs['method'] = 'orderdata'
        else:
            kwargs['method'] = 'singleorderdata'
            kwargs['params'] = {'marketid':marketid}
        now = time.time()
        orders = self.Request.fetch(**kwargs)
        for key in orders:
            pair = (
                    orders[key]['primarycode'],
                    orders[key]['secondarycode']
                   )
            self.OrdersCurrent[pair] = orders[key]
            self.OrdersCurrent[pair]['timestamp'] = now
        return 0

