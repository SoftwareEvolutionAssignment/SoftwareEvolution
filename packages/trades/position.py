"""Module trades.position.
Class
-----
Position : Represents the position a particular client has on a particular security.


Methods
-------
getSymbol() : returns symbol of the company
getQuantity() : returns quantity of shares
getLastModificationDate() : returns the date shares were last acquired
setLastModificationDate() : sets the date from last acquisition
getAcquisitionDate() : returns the date shares were first acquired
getCurrentValue() : returns the value of the shares

Functions
----------
__init__() : Constructor for the Position
__str__() : Representation of the position with symbol , quantity , acquisition date and last modification date.

Created on 30 Nov 2017

@author: Adil Al-Yasiri

Updated on 20 March 2018

@author: Ibrahim Masembe
"""
from datetime import datetime


class Position:
    """
    A class representing the position a particular client has on a particular security
    """

    DATE_FORMAT = '%Y/%m/%d'

    def __init__(self, symbol, quantity, acquisition_date, last_modification_date=""):
        """
        Constructor for the position class

        Arguments
        ---------
        symbol: type string
        quantity: type integer
        acquisition_date: type date
        lastModificationDate : type date

        """
        self.symbol = symbol
        self.quantity = quantity
        self.acquisitionDate = acquisition_date
        self.lastModificationDate = (acquisition_date if last_modification_date == "" else last_modification_date)

    def getSymbol(self):
        """returns symbol of the company"""
        return self.symbol

    def getQuantity(self):
        """returns quantity of shares"""
        return self.quantity

    def getLastModificationDate(self):
        """returns the date shares were last acquired"""
        return self.lastModificationDate

    def setLastModificationDate(self, value):
        """sets the date from last acquisition"""
        self.lastModificationDate = value

    def getAcquisitionDate(self):
        """returns the date shares were first acquired"""
        return self.acquisitionDate

    def getCurrentValue(self):
        """returns the value of the shares"""
        pass

    # where to edit print out
    def __str__(self):
        # the format in which a position is printed in
        return "%s|%d|%s|%s" % (self.symbol, self.quantity,
                                datetime.strftime(self.acquisitionDate, Position.DATE_FORMAT),
                                datetime.strftime(self.lastModificationDate, Position.DATE_FORMAT))
