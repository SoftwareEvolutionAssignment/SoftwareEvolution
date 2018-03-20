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


""""

'''
Created on 25 Nov 2017
@author: adil

Updated on 16 March 2018
@author: norbert
'''

import re
from pprint import pprint

from server.Server import MarketDataServer
from server.dataunavailable import DataUnavailableEx


class Alphavantage(MarketDataServer):
    '''
    A module representing a the Alphavantage Server class
    It builds the URL to point to Alphavantage domain.
    The class inherits from MarketDataServer
    '''


    def __init__(self, config_fname):
        MarketDataServer.__init__(self, config_fname)
    
    
    def getURL (self):
        """
        Returns the full URL for a particular security. 
        
        """
        return self.path+"?function= "+self.function+ \ # time series e.g. intraday, daily, ...
            "&symbol="+self.symbol+ \ #symbol of the sequirity
            "&interval="+self.interval+ \ #interval between two consequiteve datapoints in time series
            "&apikey="+self.apikey+ \ #api key
            "&datatype="+self.datatype # data type in which the data are stored by default it's json
    
    def setFunction(self, function):
        """
        Sets the function variable. To define what time series it holds.
        
        Arguments
        --------- 
        function: 'string'
            defition of the time series
        """
        self.function = function     
        
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
