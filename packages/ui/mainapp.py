"""Module ui.mainapp.

Class
-----
MainMenu: Subclass of the application class 

Functions
---------
__init__(): Constructor for the MainMenu class 
menu(): Main menu that welcomes user 
run(): Manages operation based on what option menu user picks 

Created on 20 February 2018

@author: Adil Al-Yasiri

Updated on the 15th March , 2018 by Omotola Shogunle
"""

import sys
import re

from ui.abstractapp import Application
from ui.clientmanager import ClientManager
from ui.tradingappl import TradingApplication
from ui.progArgumentsErr import ProgArgumentsErr

from trades.client import ClientException
from trades.PositionException import PositionException

from server.dataunavailable import DataUnavailableEx


class MainMenu(Application) :
    """A class that displays the main menu.
    
    This main menu gives access to either the Client's Manager or Trades Application
    """    
    
    def __init__(self, args):
        """Constructor checks that the program is run with the correct number of arguments.
        
        if the args length is 5 it is stored in a list and set in the Application class via 
        its methods. An instance of both the clientManager class and TradingApplication
        class is created and store in a variable.   
        Argument
        -------
        args: type list object
            stores the filenames in a list
        """
        if len(args) < 5:
            raise ProgArgumentsErr(args[0])
        else:
            (config_file_name, clients_file_name, transactions_file_name, compnies_file_name)  = args[1:5]
            #sets the individual file names in the Application class 
            Application.setConfigFileName(config_file_name)
            Application.setClientsFileName(clients_file_name)
            Application.setTransactionsFileName(transactions_file_name)
            Application.setCompaniesFileName(compnies_file_name)
            #gets instance of the client manager and trading application
            self.clientMgr = ClientManager.getInstance()
            self.tradesAppl = TradingApplication.getInstance()
    
    def menu(self):
        """Main menu option list/ welcome screen to users
        
        This gives access to the manage clients option screen and trading application
        screen.
        
        Returns
        -------
        input: type integer of option menu chosen 
        
        Exceptions
        ----------
        @raise exception: ValueError in the case user inputs unusual input
        """
        print("""System's Main Menu
            Please choose an option: 
            1:    Manage Clients.
            2:    Trading Application

            9:    Quit without saving.
            0:    Save and Exit.
            """)
        try :
            return int(input("Enter your choice: "))
        except ValueError :
            return ""        
        
    def run(self):
        """Manages option menus based on the input choice of user
        
        option 1: calls the run function of the clientMgr class 
        option 2: calls the run function of the tradesAppl class 
        option 0: saves clients and transactions made 
        option 9: quits the application, by entering 'Yy' user confirms operation
        
        Exceptions
        ---------
        @raise exception: ClientEXception, PositionException, DataUnavailableEx as ex
            ex is raised based on which exception is brought forward by user input
        """
        while(True) :
            try:
                choice = self.menu()
                if choice == 1:
                    self.clientMgr.run()
                elif choice == 2:
                    self.tradesAppl.run()
                    
                elif choice == 0:
                    self.clientMgr.saveClients()
                    self.tradesAppl.saveTransactions()
                    break
                
                elif choice == 9:
                    response = input("Are you sure, you want to quit the system; all changes will be discarded [y/n]? ")
                    if re.search(r"^[Yy]", response):
                        break
                    
                else :
                    print ("Error: Undefined input ", file=sys.stderr)
                    
            except (ClientException, PositionException, DataUnavailableEx) as ex :
                print("Exception: ", ex, file=sys.stderr)
            
            finally:
                input ("Please press RETURN:")
                print("\n\n")

######### main program starts here ###########

#Create and run the application main menu      
    #    argv[1] is the price server config file
    #    argv[2] is the clients' data file; one line per client. Each line contains the client's information and
    #        all positons held by that client.
    #    argv[3] is the transactions data file. Each line contains one buy or sell transaction
    #    argv[4] is the companies file containing information about the companies     
if __name__ == '__main__' :
    try:
        main_appl = MainMenu(sys.argv)
        main_appl.run()
    except ProgArgumentsErr as ex :
        print("Exception: ", ex.__doc__, file=sys.stderr)
        print(ex, file=sys.stderr)

