"""" Module aphvavantage.py

Class
-----
Aplphavatnage class is a class of a server and it builds URL 
to point to Alphavantage domain which provides API's for 
getting current values of trading securities. 
Refer to: https://www.alphavantage.co/documentation/

Functions
----------
getURL() : Returns the full URL for a particular security. 
setFunction() : Sets the function variable. To define what time series it holds.

Created on 25 Nov 2017
@author: Adil Al-Yasiri

Updated on 16 March 2018
@author: Norbert
"""

import re
from pprint import pprint

from server.Server import MarketDataServer
from server.dataunavailable import DataUnavailableEx


class Alphavantage(MarketDataServer):
    """A module representing a the Alphavantage Server class.
    
    It builds the URL to point to Alphavantage domain.The class inherits from MarketDataServer
    """


    def __init__(self, config_fname):
        MarketDataServer.__init__(self, config_fname)
    
    
    def getURL (self):
        """Returns the full URL for a particular security. 
        
        By collecting the time series e.g itraday,daily etc, security symbol, interval between two 
        consecutive data points in time series, api key, and data type which the data is stored by default
        which in json in this case.
        """
        
        return self.path+"?function="+self.function+ \
            "&symbol="+self.symbol+ \
            "&interval="+self.interval+ \
            "&apikey="+self.apikey+ \
            "&datatype="+self.datatype
            

    def setFunction(self, function):
        """
        Sets the function variable. To define what time series it holds.
        
        Arguments
        --------- 
        function: 'string'
            definition of the time series
        """
        self.function = function     
        
    def setInterval(self, interval):
        self.interval = interval
        
    def getPrices (self, market_data):
        """
        Returns prices of securities on the market for a particular time series. 
        
        Arguments
        --------- 
        market_data: 'market_data'
            market_data object
            
        Exception
        ---------
        @raise exception: DataUnavailableEx Error if the market data file is not available
            
        """
        for key in market_data:
            if key.startswith('Time Series') :
                return market_data[key]
        else :
            raise DataUnavailableEx
    
    
    def getLastRecordedDate(self, market_data):
        """
        Returns last recored date from the market data object
        
        Arguments
        --------- 
        market_data: 'market_data'
            market_data object
            
        Exception
        ---------
        @raise exception: DataUnavailableEx Error if the market data file is not available
            
        """
        #pprint(market_data)
        if(market_data and 'Meta Data' in market_data) :
            last_refreshed = market_data['Meta Data']['3. Last Refreshed']
            
            #get the date part of the last refreshed dattime (first 10 characters)
            return last_refreshed[0:10]
        else :
            raise DataUnavailableEx("Price data not found")
