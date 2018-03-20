'''module server.Server

Class
----- 
Super Class
A ChartServer class
to create an object use the code:
from Server use ChartServer
obj = MarketDataServer (configfile)
where configfile is the name of the config file containing the server's
path, symbol and interval specification

Methods
------- 
getURL() : abstranct returns the URL of the server
getPrices() : abstract returns the prices from the server
getLastRecordedDate() : abstract returns the last recorded date
       
Functions
---------
setSymbol() : setter for field symbol
setInterval() : setter for field interval
getDataAsText() : returns market data in .txt format 
getDataAsJSON() : returns marekt data in json format

Created on 24 Nov 2017
@author: adil

Updated on 18 March 2018
@author Norbert
'''
from abc import ABCMeta, abstractmethod

import requests
import sys

class MarketDataServer(metaclass=ABCMeta)  :
    """A ChartServer class
        to create an object use the code:
            from Server use ChartServer
            obj = MarketDataServer (configfile)
        where configfile is the name of the config file containing the server's
        path, symbol and interval specification
    """
    
    
    def __init__ (self, config_fname):
    """    
    The constructor uses a config file to read the server's 
    fields and values (separated by a '=' char)
    """
        self.conf_file = open (config_fname, "r")
        
        for line in self.conf_file :
            line=line.strip()
            (key, value) = line.split("=")
            self.__dict__[key] = value
        self.conf_file.close()
    
    def setSymbol(self, symbol):
    """    
    setter for field symbol
    """
        self.symbol = symbol
    
    def setInterval(self, interval):
    """    
    setter for field interval
    """
        self.interval = interval
        
    @abstractmethod
    def getURL (self):
    """    
    returns the URL of the server
    """
        pass
    
    @abstractmethod
    def getPrices (self, market_data):
    """    
    returns the prices from the server
    """
        pass
    
    @abstractmethod
    def getLastRecordedDate(self, market_data):
    """    
    returns the last recorded date
    """
        pass
        
    def getDataAsText(self):
    """    
    returns market data in .txt format 
    """
        url = self.getURL()
        return requests.get(url).text
    
    def getDataAsJSON(self) :
    """    
    returns marekt data in json format
    """
        url = self.getURL()
        return requests.get(url).json()
    
        