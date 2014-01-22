# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from pyapi import RequestPrivate

# <codecell>

class Account():
    def __init__(self, public_key = '', private_key = '', private_request = RequestPrivate):
        """
            This class is designed to hold all information specific to
                a user account on cryptsy.com.
            Be carefull the secret (priv_key)
        """
        self.CryptoAdresses = {}
        self.CryptoAdresses['LTC'] = 'LMGgCFsxJBjkPwAW9bn5MnZG4vyTGv1aJr'
        self.pub_key = public_key
        self.priv_key = private_key
        self.Request = private_request(Account = self)
        return None
    
    def update_Info(self,):
        return self.Request.fetch('getinfo')

