"""Module server.price.py

Class
-----
Class representing the pricing server used to get market data prices


Functions
---------
getTodaySecurityPriceBySymbol() : returns today's security price by symbol
getLastRecordedPriceBySymbol() : returns the last recorded price of the security
getTodaysAveragePriceBySymbol() : returns the average price of the security for the current day
getTodaysVolumeBySymbol () : returns ADTV for a security

Created on 27 Nov 2017
@author: Adil Al-Yasiri

Updated on 16 March 2018
@author: Norbert
"""

from datetime import datetime
from server.price_Unavailable_Ex import PriceUnavailableEx
from server.dataunavailable import DataUnavailableEx
import sys
import pprint
from janitor.plugincore.exceptions import UnimplementedMethod

class PriceServer():
    """Class representing the pricing server used to get market data prices."""
    
    DATE_FORMAT = "%Y-%m-%d"
    DAY_SERIES_FUNCTION = 'TIME_SERIES_DAILY'
    DAY_SERIES_FUNCTION2 = 'TIME_SERIES_INTRADAY'

    def __init__(self, mkt_data_source):
        """source represents the source of the market data "Yahoo" or "Alpha". """
        self.mkt_data_srvr = mkt_data_source
    
    
    def getTodaySecurityPriceBySymbol(self, symbol):
        """Returns today's security price by symbol.
        
        Exceptions
        ---------
        @raise exception:PriceUnavailableEx error if no price found for a symbol
        """
        self.mkt_data_srvr.setSymbol(symbol)
        self.mkt_data_srvr.setFunction(PriceServer.DAY_SERIES_FUNCTION) #function to get last 100 prices per date
        mkt_data = self.mkt_data_srvr.getDataAsJSON()
        
        try:
            prices = self.mkt_data_srvr.getPrices(mkt_data)
            today = datetime.now().strftime (PriceServer.DATE_FORMAT)
            if today in prices:
                return prices[today]['4. close']       
            else:
                raise PriceUnavailableEx()
        except (DataUnavailableEx):
            print("No data is available")
    

    def getLastRecordedPriceBySymbol(self, symbol):
        """Returns security's price of the last recorded price
        
        Exceptions
        ---------
        @raise exception:DataUnavailable error if today's price does not exist
        """
        self.mkt_data_srvr.setSymbol(symbol)
        self.mkt_data_srvr.setFunction(PriceServer.DAY_SERIES_FUNCTION) #function to get last 100 prices per date
        mkt_data = self.mkt_data_srvr.getDataAsJSON()
        try:
            last_date = self.mkt_data_srvr.getLastRecordedDate(mkt_data)
            prices = self.mkt_data_srvr.getPrices(mkt_data)
            return prices[last_date]['4. close']
        except DataUnavailableEx :
            print ("Exception in Price by Symbol!", file=sys.stderr)
            raise DataUnavailableEx("Price not found")
        

    def getTodaysAveragePriceBySymbol(self, symbol):       
        """Returns the average price of the security for the current day
        
        Arguments
        -------
        symbol: symbol of type string for example "GOOG" 
        
        Exception
        ---------
        @raise exception:
            DataUnavailableError: If data for the specific symbol does not exist
        """
        self.mkt_data_srvr.setSymbol(symbol)
        #sets the function to intraday 
        self.mkt_data_srvr.setFunction(PriceServer.DAY_SERIES_FUNCTION2) 
        #sets the interval to 15 minutes
        self.mkt_data_srvr.setInterval('15min')
        mkt_data = self.mkt_data_srvr.getDataAsJSON()
        i = 0
        summ=0
        try:
            prices = self.mkt_data_srvr.getPrices(mkt_data)
            today = datetime.now().strftime (PriceServer.DATE_FORMAT)
            for key in prices.keys():
                if key.startswith(today[:10]):
                    i+=1
                    summ+=float(prices[key]['4. close'])
            
        except (DataUnavailableEx):
            print("No data is available")
        return round(summ/i, 4)
        

    def getTodaysVolumeBySymbol(self, symbol):      
        """Returns ADTV for a security.
        
        the amount of individual securities traded in a day on average over a specified period of time (day)
        Arguments
        -------
        symbol: symbol of type string for example "GOOG" 
        
        Exception
        ---------
        @raise exception:
            DataUnavailableEX: If data for symbol does not exist 
        """
        self.mkt_data_srvr.setSymbol(symbol)
        #sets the function to intraday 
        self.mkt_data_srvr.setFunction(PriceServer.DAY_SERIES_FUNCTION2) 
        #sets the interval to 15 minutes
        self.mkt_data_srvr.setInterval('15min')
        mkt_data = self.mkt_data_srvr.getDataAsJSON()
        all_volume = 0
        i=0
        try:
            prices = self.mkt_data_srvr.getPrices(mkt_data)
            today = datetime.now().strftime (PriceServer.DATE_FORMAT)
            for key in prices.keys():
                if key.startswith(today[:10]):
                    i+=1
                    all_volume+=float(prices[key]['5. volume'])

        except (DataUnavailableEx):
            print("No data is available")
          
        return all_volume 

    