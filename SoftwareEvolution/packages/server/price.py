'''Module server.price.py

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
@author: adil

Updated 18 Feb 2018
@author Norbert
'''
from datetime import datetime
from server.Price_Unavailable_Ex import PriceUnavailableEx
from server.dataunavailable import DataUnavailableEx
import sys
import pprint

class PriceServer():
    '''
    Class representing the pricing server used to get market data prices
    '''
    DATE_FORMAT = "%Y-%m-%d"
    DAY_SERIES_FUNCTION = 'TIME_SERIES_DAILY'

    def __init__(self, mkt_data_source):
        '''
        source represents the source of the market data "Yahoo" or "Alpha"
        '''
        self.mkt_data_srvr = mkt_data_source
    
    #---------------------------------------------------------
    # Returns today's price; else raises a PriceUnavailableEx
    #---------------------------------------------------------   
    def getTodaySecurityPriceBySymbol(self, symbol):
        """
        Returns the average price of the security for the current day
        
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
        """
        Returns security's price of the last recorded price
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
    @unimplemented 
    def getTodaysAveragePriceBySymbol(self, symbol):       
        """
        returns the average price of the security for the current day
        """
        return ''
    @unimplemeted
    def getTodaysVolumeBySymbol(self, symbol):      
        """
        Returns ADTV for a security - the amount of individual securities traded in a day on average over a specified period of time.
        """
        return ''
    