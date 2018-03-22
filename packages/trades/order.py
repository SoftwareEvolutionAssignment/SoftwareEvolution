"""
Module trades.order.

Class
-----
OrderStatus : A enumerator showing the status of an order
TransType : Used to pick the type of transaction either buying or selling

Methods
-------
getSymbol() : returns the symbol of the company to be order
getClientID() : returns the identification number of the client
getTrans_type() : returns the transaction type whether buying or selling
getQuantity() : returns the quantity of shares required
getAsk_price() : returns the asking price for the order
getStatus() : returns the status of the order
setStatus() : Sets the order status to open
setQuantity() : Used to choose the quantity of shares required
setAsk_price() : Sets the asking price of the shares

Created on 30 Nov 2017

@author: Adil Al-Yasiri

Updated on 20 March 2018

@author: Ibrahim Masembe
"""
import enum


class OrderStatus(enum.IntEnum):
    OPEN = 0
    SUBMITTED = 1
    FULFILLED = 2
    PARTIAL = 3
    KILLED = 4
    O = OPEN
    S = SUBMITTED
    F = FULFILLED
    P = PARTIAL
    K = KILLED


globals().update(OrderStatus.__members__)


class TransType(enum.IntEnum):
    BUY = 0
    SELL = 1


globals().update(TransType.__members__)


class Order:
    """
    A class representing a client order to be executed;
    when it is executed it will be turned into a transaction.
    An order could be in one of statuses
    (open, submitted, fulfilled, partially fulfilled, or killed)
    """

    def __init__(self, client_id, symbol, trans_type, quantity, ask_price):
        """
        Constructor

        Arguments
        ---------
        client_id: type integer
            Used to identify the client
        symbol: type string
            Represents the company
        trans_type: type IntEnum
            Type of transaction to be used
        quantity: type integer
            Amount of shares required
        ask_price: type int
            Amount asked for an order

        """
        self.__client_id = client_id
        self.__symbol = symbol
        self.__trans_type = trans_type
        self.__quantity = quantity
        self.__ask_price = ask_price
        self.__status = OrderStatus.OPEN

    def getClientID(self):
        """ returns the identification number of the client"""
        return self.__client_id

    def getSymbol(self):
        """returns the symbol of the company to be ordered"""
        return self.__symbol

    def getTrans_type(self):
        """returns the transaction type whether buying or selling"""
        return self.__trans_type

    def getQuantity(self):
        """returns the quantity of shares required"""
        return self.__quantity

    def getAsk_price(self):
        """returns the asking price for the order"""
        return self.__ask_price

    def getStatus(self):
        """returns the status of the order"""
        return self.__status

    def setStatus(self, status):
        """Sets the order status to open"""
        self.__status = status

    def setQuantity(self, value):
        """Used to choose the quantity of shares required"""
        self.__quantity = value

    def setAsk_price(self, value):
        """Sets the asking price of the shares"""
        self.__ask_price = value
