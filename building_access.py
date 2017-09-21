#!/usr/bin/python

# Title: building_login.py
#
# Author: Troy <twc17@pitt.edu>
# Date Modified: 09/20/2017
# Version: 1.0.1
# 
# Purpose:
#   This is a program for a building access log book. It uses a magnetic card reader to grab
#   a Pitt employees 2P number from their ID card. This will then be used for an LDAP query to
#   get the rest of their account information. You also have the option to manually enter in 
#   information for guests, or if you forgot your ID card.
# 
# Dependencies:
#   python 2.6.6+
#
# Usage:
#   python [-h] building_login.py
#
# TODO: Everything! lololol

# Imports
import getpass, argparse

def get_input():
    """Get ths users input for either their ID card swipe, or manually enter information

    Returns:
        Users input as string
    """
    pass

def query_ldap(2PNumber):
    """Query Pitt LDAP server for users 2P number

    Arguments:
        2PNumber -- Pitt 2P number from ID card

    Returns:
        Result of LDAP query, as string
    """
    pass

def add_log(user, first, last, time, db):
    """Add record to current building access log

    Arguments:
        user -- Pitt Username
        first -- First name
        last -- Last name
        time -- Date/time that the user is logging in
        db -- Database of current building log

    Returns:
        True if the add is successful, False otherwise
    """
    pass

def del_log(user, db):
    """Delete record from the current building access log

    Arguments:
        user -- Pitt username to logout
        db -- Database of current building log

    Return:
        True if the delete is successful, False otherwise
    """
    pass

def write_log(entry, log_file):
    """Write add/del entry to log file

    Arguments:
        entry -- Entry to add to log file
                Will probably look something like 'USER,last,first,IN/OUT,date'
        log_file -- Log file to write entry to 

    Return:
        True if write to log file was successful, False otherwise
    """
    pass

def main():
    """Main"""
    pass

# Run the program
if __name__ == "__main__":
    main()
