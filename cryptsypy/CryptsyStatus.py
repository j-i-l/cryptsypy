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
    
    def get_Clicks(self,):
        self.Clicks = {}
        Pairs = self.Pairs.keys()
        for i in xrange(len(Pairs) - 2):
            for j in xrange(1+i, len(Pairs) - 1):
                for k in xrange(j+1, len(Pairs)):
                    if any([cur in Pairs[i] for cur in Pairs[j]]):
                        cand = filter(lambda x:x not in Pairs[i],Pairs[j])[0]
                        middle = filter(lambda x:x != cand,Pairs[j])[0]
                        other = filter(lambda x:x not in Pairs[j], Pairs[i])[0]
                        if cand in Pairs[k]:
                            o_cand = filter(lambda x:x not in Pairs[j], Pairs[k])[0]
                            if o_cand in Pairs[i] and o_cand == other:
                                forw = [(other, middle),(middle, cand), (cand, other)]
                                bwd = [(middle, other),(other, cand),(cand, middle)]
                                self.Clicks[(Pairs[i],Pairs[j],Pairs[k])] = [forw, bwd]
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


