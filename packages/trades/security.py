"""Module trades.security.py
Class
-----
Security : Enbodies the security object as a unit being traded 


Methods
-------
get_symbol() : returns the symbol of the security
set_symbol() : sets the symbol of the security
get_name() : returns the name of the security
set_name() : sets the name of the security
get_sector() : returns the sector of the security
get_industry() : returns the industry of the security
getCurrentMarketValue() : returns the price of the security
set_sector() : sets the sector of the security
set_industry() : sets the industry of the security
getAveragePriceForADay(): gets the average price for security symbol in a Day
getTotalVolumeForADay(): gets the average volume for security symbol in a Day





Functions
---------
  __init__() : Constructor for the Security



Created on 12 April 2018

@author: Norbert Nazarej

"""
from ui.abstractapp import Application

from server.price import PriceServer
from server.alphavantage import Alphavantage


class Security:
    """The security class stores data for each security read from the companyList file.
    
    it stores data for symbol,name,sector and industry. Other classes query the security class
    to get more information on the security symbol inputed.
    """
    
    def __init__ (self, symbol, name, sector, industry):
        self.symbol = symbol
        self.name = name
        self.sector = sector
        self.industry = industry
        self.price_srvr = PriceServer(Alphavantage(Application.getConfigFileName()))
        
    def getCurrentMarketValue(self):
        """A function querying a security's price from Price Server.
        
        Return
        ------
        price of symbol 
        
        Note:
        A Data_Unavailable_Ex may be thrown
        """
        price = self.price_srvr.getLastRecordedPriceBySymbol(self.symbol)
        return price
    
    def getAveragePriceForADay(self):
        """returns average price for security symbol in a day"""
        averagePrice = self.price_srvr.getTodaysAveragePriceBySymbol(self.symbol)
        return averagePrice
    
    def getTotalVolumeForADay(self):
        """returns average volume for security symbol in a day"""
        totalVolume = self.price_srvr.getTodaysVolumeBySymbol(self.symbol)
        return totalVolume
    
    def getName(self):
        """returns name of company for security symbol"""
        return self.name
    
    def getSector(self):
        """returns sector for security symbol"""
        return self.sector
    
    def getIndustry(self):
        """returns industry for security symbol"""
        return self.industry
    
    def getSymbol(self):
        """returns security symbol"""
        return self.symbol
    
    def setSymbol(self, symbol):
        self.symbol=symbol
        
    def setName(self, name):
        """set name for security symbol"""
        self.name=name
        
    def setSector(self, sector):
        """set sector for security symbol"""
        self.sector=sector
        
    def setIndustry(self, industry):
        """set industry for security symbol"""
        self.industry=industry
        
    def __str__(self):
        # the format in which security  is printed in.
        return "%s %10s %s %21s %s %16s %s %52s" % ('\nSymbol:',self.symbol,'\nName:', self.name, '\nSector:',self.sector, '\nIndustry:',self.industry)
