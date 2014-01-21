# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

class Account():
    def __init__(self,):
        """
            This class is designed to hold all information specific to
                a user account on cryptsy.com.
            Be carefull the secret (priv_key)
        """
        self.CryptoAdresses = {}
        self.CryptoAdresses['LTC'] = 'LMGgCFsxJBjkPwAW9bn5MnZG4vyTGv1aJr'
        self.pub_key = ''
        self.priv_key = ''
        return None

