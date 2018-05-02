# Software Evolution Project- Securities Trading System
The Security Trading System is a console application originally built by Dr Adil Al-Yasiri which specializes in querying market data to buy and sell securities. It uses a menu-driven application which can be operated by traders(staff of the firm that use the console application) or clients (of the firm). Traders are allowed to buy securities as a form of investment, and the quantity of secuirity determines the number of positions a client holds on a secuirty like 'GOOG', secuirities are represented with symbols in the application. The system does not support short positions, that is clients selling positions that they do not own, it only supports long positions meaning traders can only sell position they currently own. 

# Installation - Running the application from the command line
First of inorder to run this application on your system, it is advised you run it on an Ubuntu system, in your terminal run the following commands.

1. Download the project file as a zip file from the git reprository, navigate to where the file is stored using your terminal and unzip the project by running the command

			$ unzip nameofdownload.zip

		
2. The command will create a new directory depending on the name of the directory that was downloaded. Change directory into this new directory

			$ cd nameofdownload/

3. Finally run this command to execute the the console application
			
		$ ./run alpha.conf clients.txt trans.txt companylist.txt

