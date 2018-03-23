"""Module trades.client.
Class
-----
Client : Represents a client holding a position as well as all details associated with said client.
ClientException : Subclass of class Exception

Methods
-------
setName() : sets name of the client
get_name() : returns name of the client
setEmail() : sets the email of the client
getID() : returns the identification number of the client
getPositions() : returns a list of positions currently owned by the client

Functions
---------
__init__() : Constructor for the Client
addPosition() : Adds a position to a client's account
getPosition() : Returns the position if a client owns said position
__str__() : Representation of the client instance in form of name,id , email and positions held by the client.


Created on 30 Nov 2017

@author: Adil Al-Yasiri

Updated on 20 March 2018

@author: Ibrahim Masembe
"""

__all__ = ["Client", "ClientException"]
from trades.PositionException import PositionException


class ClientException(Exception):
    """Client Error"""


class Client:
    """
    A class representing a client holding a position with their details and positions on different assets.
    """

    def __init__(self, clientID, name, email):
        """
        Constructor for the client class

         Arguments
        ---------
        name: type
            Creates the name of the client
        email: type string
            Creates the email belonging to the client
        client_id: type integer
            Used to identify the client
        positions: type list


        Exception
        ---------
        @raise exception: PositionException Error if client does not hold a position on the property.
        """
        self.name = name
        self.email = email
        self.clientID = clientID
        self.positions = {}

    def get_name(self):
        """Returns the name of the client."""
        return self.name

    def getID(self):
        """Returns the iD of the client."""
        return self.clientID

    def getPositions(self):
        """Returns the positions owned by the client."""
        return list(self.positions.values())

    def setName(self, name):
        """Changes the name of the client."""
        self.name = name

    def setEmail(self, email):
        """Changes the email of the client."""
        self.email = email

    def addPosition(self, position):
        """Adds positions to the clients account."""

        if self.hasPosition(position.getSymbol()):
            currentPosition = self.positions[position.getSymbol()]
            # increases the amount owned by the client
            currentPosition.quantity += position.getQuantity()
            # updates the date from last change
            currentPosition.setLastModificationDate(position.getLastModificationDate())
        else:
            # adds the position to the client account
            self.positions[position.getSymbol()] = position

    def getPosition(self, symbol):
        """
        Returns:
        position: type list
            Returns positions owned by the client

        Exception
        ---------
        @return: PositionException exception if the client doesn't hold the position
        """
        if self.hasPosition(symbol):
            return self.positions[symbol]
        else:
            raise PositionException("Client does not hold position on this security")

    def hasPosition(self, symbol):
        """Checks if a symbol exists in the client's positions.
        
        Arguments
        ---------
        symbol: of type string
        
        Returns
        -------
        boolean if client has positions in symbol 
        """
        return True if symbol in self.positions else False

    def updatePositions(self, transacton):
        pass

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        # edit format for print out
        positions = [str(position) for position in self.positions.values()]

        return "%d:%s:%s:%s" % (self.clientID, self.name, self.email, ",".join(positions))
