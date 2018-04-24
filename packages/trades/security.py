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
set_sector() : sets the sectory of the security
set_industry() : sets the industry of the security




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
        averagePrice = self.price_srvr.getTodaysAveragePriceBySymbol(self.symbol)
        return averagePrice
<<<<<<< HEAD
    
    def getTotalVolumeForADay(self):
        totalVolume = self.price_srvr.getTodaysVolumeBySymbol(self.symbol)
        return totalVolume
    
=======
    def getTotalVolumeForADay(self):
        totalVolume = self.price_srvr.getTodaysVolumeBySymbol(self.symbol)
        return totalVolume
>>>>>>> 06d355ae095117f8de11ec301ad875d6f77e6001
    def getName(self):
        return self.name
    
    def getSector(self):
        return self.sector
    
    def getIndustry(self):
        return self.industry
    
    def getSymbol(self):
        return self.symbol
    
    def setSymbol(self, symbol):
        self.symbol=symbol
        
    def setName(self, name):
        self.name=name
        
    def setSector(self, sector):
        self.sector=sector
        
    def setIndustry(self, industry):
        self.industry=industry
        
    def __str__(self):
        # the format in which security  is printed in.
        return "%s %10s %s %21s %s %16s %s %52s" % ('\nSymbol:',self.symbol,'\nName:', self.name, '\nSector:',self.sector, '\nIndustry:',self.industry)
