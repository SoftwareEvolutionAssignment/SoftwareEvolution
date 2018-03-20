'''server.YahooServer
Class
----- 
A module representing a the Yahoo Server class - connector to yahoo fincance api 
ref: https://finance.yahoo.com/lookup?s=API
It builds the URL to point to Yahoo domain.
   
Methods
---------
getURL() : returns the URL of the yahoo server
getLastRecordedDate() : Returns the last recorded date from the maret data
getPrices() : Returns the market data prices for a particular time series (interval) 

Updated on 18 March 2018
by Norbert

Created on 25 Nov 2017
@author: adil
'''
from server.Server import MarketDataServer

class YahooServer(MarketDataServer):
    '''
    A module representing a the Yahoo Server class
    It builds the URL to point to Yahoo domain.
    '''

    def __init__(self, config_fname):
        """
        Constructor inherited from its super class MarketDataServer
        """
        MarketDataServer.__init__(self, config_fname)
        
    def getURL (self):
        """
        Returns URL of the yahoo server with symbol and interval values
        """
        return self.path+self.symbol+"?interval="+self.interval
    @uniplemented
    def getLastRecordedDate(self, market_data):
        """
        Returns the last recorded date from the maret data
        """
        return ''
    
    def getPrices (self, market_data):
        """
        Returns the market data prices for a particular time series (interval) 
        """
        mkt_data_fileds = market_data.keys()
        for field in mkt_data_fileds :
            if field.find('Time Series') :
                return market_data[field]