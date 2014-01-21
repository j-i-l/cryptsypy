# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from CryptsyStatus import Status

# <codecell>

class StatusTornado(Status):
    def __init__(self,):
        CryptsyStatus.__init__(self,)
        
        
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

    def get_TornadoRevenue(self,):
        self.TornadoRevenue = {}
        for click in self.Clicks.keys():
            self.TornadoRevenue[click] = {}
            for orien in self.Clicks[click]:
                revenue = 1.0
                for cur in orien:
                    revenue = revenue*self.PricesLast[cur]*self.fee
                self.TornadoRevenue[click][tuple(orien)] = revenue
        return 0

