"""Module ui.traidingappl

Class
-----
TradingApplication: A subclass of the Application class. 

Methods
-------
getInstance(): Returns instance of TradingApplication

Functions
---------
_transactions_between(from_date, to_date):function called in listTransactionsInPeriod
saveTransactions(): save transactions to transaction file 
sell(client, symbol): sell positions of security owned by client
buy(client, symbol): buy positions of security for client
queryPrice(symbol): ask current price of security symbol
listAllTransactions(): list all transactions
listTransactionsPerClient(client): list all transactions for clients
listTransactionsInPeriod(from_date, to_date): list transactions between two dates 
_menu() to _menu8(): Displays operation based on user input 
run(): manages menu options and user input 

Created on 20 February 2018

@author: Adil Al-Yasiri

Updated on 15 March 2018
@author: Omotola Shogunle

"""


import sys
import re
import datetime
import bisect

from ui.abstractapp import Application
from ui.clientmanager import ClientManager
from ui.symbolDoesNotExist import SymbolDoesNotExistError

from server import price
from server.price import PriceServer
from server.alphavantage import Alphavantage
from server.dataunavailable import DataUnavailableEx
from server.orderbroker import OrderBroker

from trades.transaction import Transaction, TransactionError
from trades.order import Order, OrderStatus
from trades.order import TransType
from trades.positionException import PositionException
from trades.client import ClientException

class TradingApplication(Application):
    """Trading Application Class, a singleton for selling and buying securities.
    
    The trading application is used to buy,sell, query, store and list transactions
    made by clients. It also contains its on menu system that enables different operations
    to be carried out based on user input.
    
    Variables
    ---------
    instance initialised to none used to store object when created 
    """

    instance = None

    @staticmethod
    def getInstance():
        """Creates and intailises variable instance for Trading Application class 
        
        Returns
        -------
        TradingApplication instance object.
        """
        if not TradingApplication.instance :
            TradingApplication.instance = TradingApplication(
                                                Application.getConfigFileName(), 
                                                Application.getTransactionsFileName() )
            
        return TradingApplication.instance
    
    def __init__(self, config_file_name, transactions_file_name):
        """Constructor for TradingApplication takes arguments for configuration and transaction setup.
        
        alpha.conf is set in the PriceServer, and files that are read from the file
        are stored in a dictionary called transactions.
        
        Arguments
        ---------
        config_file_name: takes name of configuration filename alpha.conf
        transaction_file_name: takes name of transaction filename transactions.txt
        
        """
        self.price_srvr = PriceServer(Alphavantage(config_file_name))
        self.transactions_file_name = transactions_file_name
        self.broker = OrderBroker.getInstance()
        
        self.transactions = {}  #create a dictionary named transactions 
        
        with open(self.transactions_file_name, "r") as transactions_file :
            for line in transactions_file :
                line = line.rstrip()    #remove any trailing spaces 
                
                (trans_date, clt_id, tran_type, symbol, price, qty) = line.split("|")
                transaction = Transaction() #class in module trades.transaction.py
                transaction.clientID = int(clt_id)
                transaction.date = datetime.datetime.strptime(trans_date, Transaction.DATE_FORMAT)  #Convert to date object
                transaction.trans_type = TransType(int(tran_type))
                transaction.symbol = symbol
                transaction.price = float(price)
                transaction.quantity = int(qty)
                
                self.transactions[transaction.date] = transaction   #insert each transaction object as value for key transaction.date
    
              
    #Helper function implementing an efficient algorithm to return all transactions between two dates
    #The function returns a list of all found transactions Order ( nlog(N) )
    def _transactions_between(self, from_date, to_date):
        
        #First get a sorted list of all transactions dictionary keys (transaction dates)
        date_list = sorted(self.transactions.keys())
        
        #Then get location of first transaction on the from_date
        begin = bisect.bisect_left(date_list, from_date)
        
        #And location of first transaction on the day after the to_date
        end = bisect.bisect_right(date_list, to_date + datetime.timedelta(days=1))
        
        if begin != len(date_list) : #check that there are transactions on or after the from_date
            
            #Build a list of transactions using comprehension 
            #by using items in date_list from begin - end, 
            #as keys to the transactions dictionary
            return [ self.transactions[key] for key in date_list[begin:end] ]
    
    
    def saveTransactions(self):
        """Saves transactions to a text file by writing to it."""
        
        with open(self.transactions_file_name, "w") as trans_file :
            for trans_date in sorted(self.transactions.keys()) :
                trans_file.write(str(self.transactions[trans_date]) + "\n")            
                
                
    def sell(self, client, symbol):
        """Sell positions to client based on what symbol client choose.
        
        if client has security with available positions to sell, client proposes an ask
        price for a particular number of positions that they wish to sell. if ask price 
        is less than or equal to current trading price order is FULFILLED else it is KILLED.
        
        Arguments
        ---------
        client: client's id to identify which client is requesting to sell
        symbol: which security symbol already owned by client do they wish to sell positions
        
        Exceptions
        ----------
        @raise exception: 
            TransactionError: order failed 
            TypeError: user input invalid 
            PositionException: client does not hold valid number of positions they are requesting to sell
        """
        if self.broker.checkSecurityBySymbol(symbol) and client.hasPosition(symbol) :
            try:
                max_qty = client.getPosition(symbol).getQuantity()  
                print("You can sell a maximum of %d" % max_qty)
                quantity = int(self._promptForQuantity())
                if quantity <= max_qty : 
                    ask_price = float(self._promptForPrice())
                    if ask_price <= float(self.queryPrice(symbol)) :
                        sell_order = Order(int(client.getID()), symbol, TransType.SELL, quantity, ask_price)
                        print("You asked to sell %d stocks of %s, which is now trading at %s" % 
                                    (quantity, symbol, self.queryPrice(symbol))
                          )
                        response = input("Are you happy to submit your order [y/n]? ")
                        if re.search(r"^[Yy]", response):
                            transaction = self.broker.executeOrder(sell_order)
                            if transaction :
                                transaction.commit()
                                self.transactions[transaction.date] = transaction
                                print("Order was successful security balance %d " % (max_qty - quantity))
                                return
                            else :
                                raise TransactionError("Sell order failed")
                    
                        else:
                            sell_order.setStatus(OrderStatus.KILLED)
                    else :
                        print("Your ask price %s is greater than current trading price at %s" %
                              (ask_price, self.queryPrice(symbol))
                              )   
                        sell_order.setStatus(OrderStatus.KILLED)
                        raise TransactionError("Sell order failed")
                else :
                    print("Order cannot be executed; you don't have enough stock")
                    return
            
            except TypeError as ex :
                print ("Exception: %s " %ex, file = sys.stderr)
        else :
            raise PositionException("You do not hold position on this symbol")
            
                  
    def buy(self, client, symbol):
        """Buys positions for symbols input by clients.
        
        if security symbol is available to purchase buy inputs the number of positions 
        they would like and their ask price. if ask price is greater than or equal to 
        current trading price the order is FULFILLED else the order is killed 
        Arguments
        ---------
        client: client's id to identify which client is requesting to buy
        symbol: which security symbol client wish to buy position
        
        Exceptions
        ----------
        @raise exception:
            TypeError: user input invalid 
            SymbolDoesNotExistError: Prints error if symbol does not exist
        """
        if self.broker.checkSecurityBySymbol(symbol) :
            try:
                quantity = int(self._promptForQuantity())
                ask_price = float(self._promptForPrice())
                if ask_price >= float(self.queryPrice(symbol)) :
                    buy_order = Order(int(client.getID()), symbol, TransType.BUY, quantity, ask_price)
                    print("You asked to buy %d stocks of %s, which is now trading at %s" % 
                                (quantity, symbol, self.queryPrice(symbol))
                      )
                    response = input("Are you happy to submit your order [y/n]? ")
                    if re.search(r"^[Yy]", response):
                        transaction = self.broker.executeOrder(buy_order)
                        if transaction :
                            transaction.commit()
                            self.transactions[transaction.date] = transaction
                            print("Order was successful security balance %d ")
                            return
                        else :
                            raise TransactionError("Buy order failed")
                    else :
                        buy_order.setStatus(OrderStatus.KILLED)
                else:
                    print("Your ask price %s is less than current trading price at %s" %
                              (ask_price, self.queryPrice(symbol))
                              ) 
                    buy_order.setStatus(OrderStatus.KILLED)
                    raise TransactionError("Buy order failed")
            except TypeError as ex :
                print ("Exception: %s " %ex, file = sys.stderr)
        else :
            raise SymbolDoesNotExistError("Cannot find symbol")
    
    
    def queryPrice(self, symbol) :
        """A function querying a security's price from Price Server.
        
        Arguments
        ---------
        symbol: argument for security symbol price you want to query
        
        Return
        ------
        price of symbol 
        
        Note:
        A Data_Unavailable_Ex may be thrown
        """
        price = self.price_srvr.getLastRecordedPriceBySymbol(symbol.upper())
        return price
    
    
    def listAllTransactions(self):
        """List transactions from self.transactions dictionary in key-value pairs.
        
        key: date
        value : transaction object
        """
        print("""
            Date & time of transaction  =>     Transaction Details
            ===========================   =============================""")
        for date, transaction in self.transactions.items() :
            print(date, " => ", transaction)
    
    
    def listTransactionsPerClient(self, client):
        """List transactions made by each client.
        
        Arguments
        ---------
        client: identifies client user wants transactions for 
        """
        response = input("Lsting transactions for client %s? [y/n] " % client.get_name())
        if not re.search(r"^[Yy]", response):
            return
        
        for transaction in self.transactions.values() :
            if transaction.get_client_id() == client.getID() :
                print(transaction)

    
    def listTransactionsInPeriod(self, from_date, to_date):
        """List all transactions between two dates inclusive.
        
        user inputs two dates of equal value to list transactions on a particular date 
        
        Arguments
        --------
        from_date: enter date from which you would like to see transactions
        to_date: enter last date that transaction processes should consider 
        
        Exception:
        @raise exception: Whatever exception is caught is printed out to user 
        """
        try :
            trns_in_dates = self._transactions_between(from_date, to_date)
            
            if trns_in_dates :
                for  transaction in trns_in_dates :
                    print(transaction)
            else :
                print("No transaction found on this period!")
        except Exception as ex:
            print("Exception: %s" % ex, file=sys.stderr)
            
#        Old inefficient implementation (order O(n))
#         for transaction in self.transactions.values() :
#             if transaction.get_date().date() >= from_date.date() and 
#                transaction.get_date().date() <= to_date.date()  :
#
#                 print(transaction)    
    
    def listTransactionsPerSecurity(self, symbol):
        """List transactions per security symbol.
        
        symbol to view transaction is input by user and function first checks if symbol exist
        if not a symbol not found error is raised. If it exist all transactions for that security
        are listed.
        
        Arguments
        ---------
        symbol: user input symbol they will like to view transactions on
        
        Exceptions
        ----------
        @raise exception: 
            SymbolDoesNotExistError : print a cannot find symbol error
        """
        if not self.broker.checkSecurityBySymbol(symbol):
            raise SymbolDoesNotExistError("Cannot find symbol")
        
        print("Listing transactions for Security %s" % symbol )
        for transaction in self.transactions.values() :
            if transaction.get_symbol() == symbol :
                print(transaction)
    
    def _menu(self):
        """Menu option for trading application class
        
        Returns
        -------
        input menu option user has entered 
        
        Exception
        ---------
        @raise exception:
            ValueError: Invalid user entry 
        """
        print("""Client's Manager Menu
            Please choose an option: 
            1:    Buy securities.
            2:    Sell securities.
            3:    Query a security's price.
            4:    List transactions for a client.
            5:    List transactions in date.
            6:    List transactions in a two-dates period
            7:    List transactions in security
            8:    List all recorded transactions
            0:    Return to Main Menu
            """)
        try :
            return int(input("Enter your choice: "))
        except ValueError :
            return ""
        
        
    def _menu0(self):       
        #Return to Main
        pass
    
    
    def _menu1(self):       
        #Menu option for buying security symbols
        #Raises TransactionError or SymbolDoesNotExistError
        try:
            client_id = self._promptForID()
            client = ClientManager.getInstance().retrieveClient(client_id)
            print("Hello %s, you asked to buy some stocks." % 
                    client.get_name()
                  )
            symbol = self._promptForSymbol()
            self.buy(client, symbol) 
            
        except (TransactionError, SymbolDoesNotExistError) as  ex :
            print("Exception: ", ex, ex.__doc__, file = sys.stderr)
    
    def _menu2(self):       
        #Menu option for selling security symbols
        #Raises TransactionError or SymbolDoesNotExistError
        try:
            client_id = self._promptForID()
            client = ClientManager.getInstance().retrieveClient(client_id)
            print("Hello %s, you asked to sell some stocks." % client.get_name())
            
            symbol = self._promptForSymbol()
            
            if client.hasPosition(symbol) :
                self.sell(client, symbol) 
            else :
                print ("You don't hold a position on %s, and we don't currently support sell short" % symbol)
            
        except (TransactionError, SymbolDoesNotExistError) as  ex :
            print("Exception: ", ex, ex.__doc__, file = sys.stderr)
  
    
    def _menu3(self):      
        #Menu option for query price
        symbol = self._promptForSymbol()      
        sec_price = self.queryPrice(symbol)
        
        print("Last recorded price for security %s is %s" %(symbol, sec_price))
        
    
    def _menu4(self):   
        #List transactions for a client.
        #Raises a ClientException error
        try:
            client_id = self._promptForID()
            client = ClientManager.getInstance().retrieveClient(client_id)
            self.listTransactionsPerClient(client)
            
        except ClientException as  ex :
            print("Exception: ", ex, ex.__doc__, file = sys.stderr)  
        
    def _menu5(self):   
        #List transactions in particular day.
        try:
            date_str = input("Enter transaction date using format: YYYY-MM-DD:")
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            self.listTransactionsInPeriod(date, date)
        except Exception as ex:
            print("Exception: ", ex, ex.__doc__, file = sys.stderr)  
    
    def _menu6(self):   
        #List transactions in a periods of different dates 
        try:
            date_str = input("Enter first transaction date using format: YYYY-MM-DD:")
            from_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            date_str = input("Enter second transaction date using format: YYYY-MM-DD:")
            to_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            
            if from_date <= to_date :
                self.listTransactionsInPeriod(from_date, to_date)
            else :
                print("Fist date cannot be after second date!")
                
        except Exception as ex:
            print("Exception: ", ex, ex.__doc__, file = sys.stderr)  
    
    def _menu7(self):  
        #List transactions per security
        try :
            symbol = self._promptForSymbol()
            self.listTransactionsPerSecurity(symbol)
        except Exception as ex:
            print("Exception: ", ex, ex.__doc__, file = sys.stderr)  
        
    
    def _menu8(self):      
        #List all transactions
        self.listAllTransactions()
                              
    def run(self):
        """Run function is called to manage trading applications menu options.
        
        Based on user input a particular menu is called and its operations executed.
        """
        menu_items = [
                        self._menu0, self._menu1, self._menu2, 
                        self._menu3, self._menu4, self._menu5, 
                        self._menu6, self._menu7, self._menu8
                        ]
        try:
            choice = self._menu()
            if choice in range(0,9) :
                menu_item = menu_items[choice]
                menu_item() #gets the option number passed inside the array
            else :
                print ("Error: Undefined input ", file=sys.stderr)
                    
        except (ClientException, PositionException, DataUnavailableEx) as ex :
            print("Exception: ", ex, file=sys.stderr)