"""
Class
-----
MarketDataTest class used to run unit test on market data and the information retrieved.

Functions
---------
setUp(): Function to set up server 
test_connect_to_Yahoo_server(): Test to connect to Yahoo Server 
test_get_Alphavantage_data_as_json(): Get data in Json format
test_get_Alphavantage_data_as_text(): Get data in Text format
test_tody_price_by_symbol(): Check for today's price symbol
test_last_recorded_price_by_symbol(): Check the last recorded price for specific symbol
test_create_client(): test to create client
test_add_position(): test to add positions for symbols for clients 


Created on 25 November 2017

@author: Adil Al-Yasiri

Updated on 27 March 2018

@author: Omotola Shogunle 
"""
import sys
sys.path.append("../packages")

from server.yahooServer import YahooServer
from server.alphavantage import Alphavantage
from server.price import PriceServer
from server.price_Unavailable_Ex import PriceUnavailableEx

from trades.client import Client
from trades.position import Position
from trades.positionException import PositionException  # @UnusedImport

import datetime

import unittest
import re
import ServerMock

class MarketDataTest(unittest.TestCase):
    """Made up of testcase function for market data test."""
    
    def setUp(self):
        """Sets URL to connect to the Yahoo and Alphavanatage servers. """
        self.yahoo = YahooServer('../trades.conf')
        self.alpha = Alphavantage('../alpha.conf')
        mock = ServerMock.MockAlphaServer()
        self.price_server=PriceServer(mock)
        
        self.json_regex=re.compile(r"^\{.*\}$", re.DOTALL)   #match everything from the start to the end
        self.url_regex=re.compile(r"https://.*/.*?", re.DOTALL) #match everything including the //
        
        self.client = Client(1, "Adil", "a.al-yasiri@salford.ac.uk")    #example client
        
    def test_connect_to_Yahoo_server(self):
        """Get Yahoo server Url and check against REGEX for a match.
        
        if there is no match this test is failed
        """
        url=self.yahoo.getURL()
        self.assertRegex(url, self.url_regex, 'URL of server should match a REGEX')
    
    def test_connect_to_Alphavantage_server(self):
        """Get Yahoo server Url and check against REGEX for a match.
        
        if there is no match this test is failed
        """
        url = self.alpha.getURL()
        self.assertRegex(url, 'https://.*/.*?', 'URL of server should match a REGEX')
    
    #@unittest.skip("skipping yahoo json test")
    def test_get_Yahoo_data_as_json(self):
        self.assertTrue('chart' in self.yahoo.getDataAsJSON(), 'Data from server looks like a json object')
    
    #@unittest.skip("skipping yahoo text test")
    def test_get_Yahoo_data_as_text(self):
        self.assertRegex(self.yahoo.getDataAsText(), self.json_regex, 'Text from server looks like a json object')
        
    #@unittest.skip("skipping alpha json test")
    def test_get_Alphavantage_data_as_json(self):
        self.assertTrue('Meta Data' in self.alpha.getDataAsJSON(), 'Data from server looks like a json object')
    
    #@unittest.skip("skipping alpha text test")
    def test_get_Alphavantage_data_as_text(self):
        self.assertRegex(self.alpha.getDataAsText(), self.json_regex, 'Text from server looks like a json object')
        
    #@unittest.skip("skipping today's price  test")
    @unittest.expectedFailure(PriceUnavailableEx)
    def test_tody_price_by_symbol(self):
        """Checks todays price against '83.8700' for equality
        
        EXception:
            @raise PriceUnvailable exception
        """
        self.assertEqual(self.price_server.getTodaySecurityPriceBySymbol("MSFT"), '83.8700', 'todays price')   
    
    #@unittest.skip("skipping last recorded price  test")
    #@unittest.expectedFailure
    def test_last_recorded_price_by_symbol(self):
        """Checks todays price against '83.8700' for equality. 
        
        Note
        ----
        AN expected failure is possible if no price is recorder for symbol
        """
        self.assertEqual(self.price_server.getLastRecordedPriceBySymbol("MSFT"), '83.8700', 'todays price')     
    
    #@unittest.skip("skipping creating a client test")
    #@unittest.expectedFailure
    def test_create_client(self):
        """Test create client and print success message"""
        client = Client(1, "Adil", "a.al-yasiri@salford.ac.uk")
        self.assertEqual("Adil", client.get_name(), "Clent created successfully")
    
    #@unittest.skip("skipping adding a position")
    #@unittest.expectedFailure
    def test_add_position(self):
        """Add position to symbol for client and check if quantity matches."""
        
        self.client.addPosition(Position("GOOG", 100, datetime.datetime.now()))
        self.assertEqual(100, self.client.getPosition("GOOG").getQuantity())
        self.client.addPosition(Position("GOOG", 100, datetime.datetime.now()))
        self.assertEqual(200, self.client.getPosition("GOOG").getQuantity())
        
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()