# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from pyapi import Request
#something along these lines

# <codecell>

class Status():
    def __init__(self, Api = Request()):
        self.MarketCurrent = {}
        self.PricesLast = {}
        self.Curs = {}
        self.Pairs = {}
        self.Api = Api
        ##to do: get the fees through request.
        self.fee = 0.997
        
        
        return None
    
    def update_info(self,):
        self.get_marketdata()
        for curs in self.MarketCurrent.keys():
            for cur in curs:
                if cur not in self.Curs:
                    self.Curs[cur] = []
            if curs not in self.Pairs.keys():
                self.Pairs[curs] = {}
        return 0
        
    def update_PricesLast(self,):
        self.PricesLast = {}
        for pair in self.Pairs.keys():
            pairMarket = self.MarketCurrent[pair]
            try:
                self.PricesLast[pair] = float(pairMarket['buyorders'][0]['price']) if pairMarket['secondarycode'] == pair[1] else 1/float(pairMarket['sellorders'][0]['price'])
                self.PricesLast[tuple(list(pair)[::-1])] = 1/float(pairMarket['sellorders'][0]['price']) if pairMarket['secondarycode'] == pair[1] else float(pairMarket['buyorders'][0]['price'])
            except TypeError:
                pass
        return 0
        
    def update_pair_info(self,):
        for pair in self.Pairs.keys():
            self.Pairs[pair]['primary'] = self.MarketCurrent[pair]['primarycode']
            self.Pairs[pair]['secondary'] = self.MarketCurrent[pair]['secondarycode']
        return None
            
        
    def get_marketdata(self,):
        market = self.Api.public_request({'method':'marketdatav2'})[u'markets']
        self.MarketCurrent = {}
        for pair in market:
            self.MarketCurrent[tuple(pair.split('/'))] = market[pair]
        return 0

