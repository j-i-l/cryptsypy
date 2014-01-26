# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

class Info(object):
    def __init__(self,):
        """
            This class holds esentially information about www.cryptsy.com
            At some time some of this information might be stored in 
                the form of files.
        """
        self.pubDomain = 'http://pubapi.cryptsy.com' #http://... before
        self.pubApiPath = '/api.php'
        self.privDomain = 'https://www.cryptsy.com'
        self.privApiPath = '/api'
        #this might be put into a config file at some point
        self.pubAddress = self.pubDomain + self.pubApiPath
        self.privAddress = self.privDomain + self.privApiPath
        self.currenices = ()

