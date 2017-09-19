#!/usr/bin/python

# Title: building_login.py
# Author: Troy <twc17@pitt.edu>
# Date Modified: 09/19/2017
# Version: 1.0.0
# 
# Purpose:
#   This is a program for a building access log book. It uses a magnetic card reader to grab
#   a Pitt employees 2P number from their ID card. This will then be used for an LDAP query to
#   get the rest of their account information. You also have the option to manually enter in 
#   information for guests, or if you forgot your ID card.
#
# Usage:
#   python [-h] building_login.py
#
# TODO: Everything! lololol

# Imports
import getpass

# 
# Get ths users input for either their ID card swipe, or manually enter information
#
# Return:
#   Users input as string
#
def get_input():
    pass

#
# Query Pitt LDAP server for users 2P number
#
# Return:
#   Result of LDAP query, as string
#
def query_ldap(2PNumber):
    pass

# 
# Add record to current building access log
#
# Return:
#   True if the add is successful, False otherwise
#
def add_log(user, first, last, time):
    pass

#
# Delete record from the current building access log
#
# Return:
#   True if the delete is successful, False otherwise
#
def del_log(user):
    pass

#
# Main program logic
#
def main():
    pass

# Run the program
if __name__ == "__main__":
    main()
