"""Module orderbroker.py

Class
-----
A singleton class representing an order broker system

     
Methods
-------
getInstance() : instantiates the singleton class

Functions
---------
checkSecurityBySymbol() : checks the security symbol 
getSecurityInfoBySymbol() : Returns a dictionary of security details containing "SYMBOL", "NAME", "SECTOR" and "INDUSTRY"
executeOrder() : Creates transaction of type Transaction for a particular order and returns it
      
Created on 21 Nov 2017
@author: Adil Al-Yasiri

Updated on 16 March 2018
@author: Norbert
"""

from trades.transaction import Transaction
from ui.abstractapp import Application



    
class OrderBroker(object):
    """A singleton class representing an order broker system."""

    instance = None
    

    @staticmethod
    def getInstance():
        """Creates and initialises an instance of the orderbroker class.
        
        also initialises the stocks_file_name field
        
        Returns
        -------
        Orderbroker instance
        """
        if not OrderBroker.instance :
            stocks_file_name = Application.getCompaniesFileName()
            OrderBroker.instance = OrderBroker(stocks_file_name)
        return OrderBroker.instance
    
    def __init__(self, stocks_file_name):
        """Uses the (tab delimited) stocks file to retrieve securities details."""
        
        self.securities = {}
        
        with open(stocks_file_name, "r") as securities_file :
            #First read the line containing the header
            securities_file.readline()
            for line in securities_file :
                line = line.rstrip()
                symbol, name, sector, industry = line.split("\t")
                self.securities[symbol] = {"SYMBOL": symbol, "NAME": name, "SECTOR": sector, "INDUSTRY": industry}
    
    
    def checkSecurityBySymbol(self, symbol):
        """Returns true if symbol exists"""
        
        return True if symbol in self.securities else False
    
    
    def getSecurityInfoBySymbol(self, symbol):
        """Returns a dictionary of security details containing "SYMBOL", "NAME", "SECTOR" and "INDUSTRY" """
        
        return self.securities[symbol] if symbol in self.securities else None
        
        
    def executeOrder(self, order):
        """Creates transaction of type Transaction for a particular order"""
        transaction = Transaction(order) 
        
        return transaction
    
    
if __name__ == '__main__' :
    #Code to test the class instantiation
    broker = OrderBroker.getInstance()
    symbol = 'GOOG'
    if broker.checkSecurityBySymbol(symbol) :
        print("%s security exists in DB" % symbol)
        print(broker.getSecurityInfoBySymbol(symbol)['NAME'])
    else :
        print ('No such company')
        
    