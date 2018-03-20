"""Module ui.progArgumentsErr

Class
-----
ProgArgumentsErr : Subclass of class Exception

Created on 15 Mar 2018

@author: Adil Al-Yasiri
"""

class ProgArgumentsErr(Exception):
    """An error of number of arguments passed to program."""
    
    def __init__(self, prog_name):
        super().__init__("Usage: %s <config_file_name> <clients_file_name> <transactions_file_name>" % prog_name)
