"""Module trades.transaction.
Class
-----
Transaction : Simulates a transaction which is the buying and selling of orders
TransactionError : Subclass of class Exception

Methods
-------
get_quantity() : returns the quantity of shares to be acquired
set_quantity() : sets the quantity of shares to be acquired
get_client_id() : Returns the iD of the client.
set_client_id() : Sets the iD of the client.
get_symbol() : returns the symbol of the company whose shares are to be ordered
get_trans_type() : returns the transaction type
get_price() : returns the price of the shares
get_date() : Gets the date when the transaction took place.
set_symbol() : Selects the company for the transaction.
set_trans_type() : Selects the transaction type.
set_price() : Sets the price for the transaction
set_date() : Sets the date when the transaction took place.


Functions
---------
  __init__() : Constructor for the Transaction
commit() : Creates or modifies existing position
go() : Buys 20 shares with Google
__str__() : Representation of the transaction in form of client id ,transaction date
,transaction type, quantity,symbol and price.


Created on 30 Nov 2017

@author: Adil Al-Yasiri

Updated on 20 March 2018

@author: Ibrahim Masembe
"""
from datetime import datetime

from trades.order import Order, OrderStatus, TransType
from ui.clientmanager import ClientManager
from trades.position import Position


class TransactionError(Exception):
    """
    Transaction Error; buy or sell order cannot be completed.
    """


class Transaction:
    """
     A class representing a client order that has been executed and hence is now changed into a transaction

    """
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'  # 2018-02-22 15:17:24.617547

    def __init__(self, order=""):
        """
        Constructor
        """
        if order == "":
            return
        # checks if the Order is open
        elif order.getStatus() == OrderStatus.OPEN:
            self.__clientID = int(order.getClientID())
            self.__symbol = order.getSymbol()
            self.__trans_type = order.getTrans_type()
            self.__quantity = int(order.getQuantity())
            self.__price = float(order.getAsk_price())
            self.__date = datetime.now()

            # change the status of order to reflect that is has been submitted
            order.setStatus(OrderStatus.SUBMITTED)
        else:
            raise TransactionError("Order is not valid")

    def get_quantity(self):
        """returns the quantity of shares to be acquired"""
        return self.__quantity

    def set_quantity(self, value):
        """sets the quantity of shares to be acquired"""
        self.__quantity = value

    def commit(self):
        client = ClientManager.getInstance().retrieveClient(str(self.clientID))

        # increases quantity of shares if buy option is selected
        if self.trans_type == TransType.BUY:
            new_position = Position(self.symbol, int(self.quantity), datetime.now())

        # decreases quantity of shares if sell option is selected
        elif self.trans_type == TransType.SELL:
            new_position = Position(self.symbol, -int(self.quantity), datetime.now())

        else:
            raise TransactionError("Some thing weird happened, UNKNOWN order type")

        client.addPosition(new_position)

    def get_client_id(self):
        """Returns the iD of the client."""
        return self.__clientID

    def set_client_id(self, value):
        """Sets the iD of the client."""
        self.__clientID = value

    def get_symbol(self):
        """returns the symbol of the company whose shares are to be ordered"""
        return self.__symbol

    def get_trans_type(self):
        """returns the transaction type"""
        return self.__trans_type

    def get_price(self):
        """returns the price of the shares"""
        return self.__price

    def get_date(self):
        """Gets the date when the transaction took place."""
        return self.__date

    def set_symbol(self, value):
        """Selects the company for the transaction."""
        self.__symbol = value

    def set_trans_type(self, value):
        """Selects the transaction type."""
        self.__trans_type = value

    def set_price(self, value):
        """Sets the price for the transaction."""
        self.__price = value

    def set_date(self, value):
        """Sets the date when the transaction took place."""
        self.__date = value

    def __repr__(self):
        return str(self.__dict__)

    # change output from here
    def __str__(self):
        # returns a transaction as client id , transaction date,transaction type, symbol, quantity and price
        return "%s|%d|%d|%s|%.4f|%d" % (
            self.date, self.clientID, self.trans_type, self.symbol, self.price, self.quantity)

        # ===========================================================================

    # Properties definition
    # ===========================================================================
    symbol = property(get_symbol, set_symbol, None, None)
    trans_type = property(get_trans_type, set_trans_type, None, None)
    quantity = property(get_quantity, set_quantity, None, None)
    price = property(get_price, set_price, None, None)
    date = property(get_date, set_date, None, None)
    clientID = property(get_client_id, set_client_id, None, None)
    quantity = property(get_quantity, set_quantity, None, None)


def go():
    (client, symbol, trans_type, quantity, ask_price) = (1, 'GOOG', TransType.BUY, 20, 99.999)
    order = Order(client, symbol, trans_type, quantity, ask_price)

    trx = Transaction(order)

    print(trx)


if __name__ == '__main__':
    go()
