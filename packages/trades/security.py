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
from server.dataunavailable import DataUnavailableEx

class Secuirty:
    
    def __init__ (self, symbol, name, sector, industry):
        self.symbol = symbol
        self.name = name
        self.sector = sector
        self.industry = industry
        self.price_srvr = PriceServer(Alphavantage(Application.getConfigFileName()))
        
    def getCurrentMarketValue(self):
        """
        Returns a current vale of the security object on the market
        """
        price = self.price_srvr.getLastRecordedPriceBySymbol(self.symbol)
        return price
    
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
        
    def setSymbol(self, industry):
        self.industry=industry