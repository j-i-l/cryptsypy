# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from CryptsyStatus import Status

# <codecell>

class StatusTornado(Status):
    def __init__(self,):
        CryptsyStatus.__init__(self,)
        
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

