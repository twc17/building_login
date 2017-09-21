#!/usr/bin/python

# Title: building_login.py
#
# Author: Troy <twc17@pitt.edu>
# Date Modified: 09/21/2017
# Version: 1.2.2
# 
# Purpose:
#   This is a program for a building access log book. It uses a magnetic card reader to grab
#   a Pitt employees 2P number from their ID card. This will then be used for an LDAP query to
#   get the rest of their account information. You also have the option to manually enter in 
#   information for guests, or if you forgot your ID card.
# 
# Dependencies:
#   python 2.6.6+
#   python-ldap
#
# Usage:
#   python [-h] building_login.py
#
# TODO: Test LDAP lookups. User input is working well. Should be able to handle bad card reads too.

# Imports
import getpass, argparse, ldap, sys

def get_input():
    """Get ths users input for either their ID card swipe, or manually enter information

    Returns:
        Users input as string
    """
    user_input = getpass.getpass("Swipe Pitt ID Card or press 'g' to sign in a guest...")

    if user_input[0] == 'g':
        return user_input[0]
    else:
        card_number = user_input.split('=')
        if len(card_number) == 2:
            return card_number[0][-10:]
        else:
            return "ERROR"

def query_ldap(card_number, l):
    """Query Pitt LDAP server for users 2P number

    Arguments:
        card_number -- Pitt 2P number from ID card
        l -- LDAP connection

    Returns:
        Result of LDAP query, as string
    """
    basedn = "ou=account,dc=unit,dc=pitt,dc=edu"

    # Attribute that we are searching for
    search_filter = "(PittPantherCardID=" + card_number + ")"
    # The attributes we want to return from the search
    search_attribute = ["cn", "sn"]
    # This will scope the entire subtree under Accounts
    search_scope = l.SCOPE_SUBTREE

    # Try to search 
    try:
        ldap_result_id = l.search(basedn, search_scope, search_filter, search_attribute)
        result_set = []
        while 1:
            result_type, result_data = l.result(ldap_result_id, 0)
            if (result_data == []):
                break
            else:
                if result_type == l.RES_SEARCH_ENTRY:
                    result_set.append(result_data)

        return result_set
    
    except ldap.LDAPError, e:
        print(e)

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
    # LDAP bind settings
    l = ldap.initialize('ldaps://pittad.univ.pitt.edu:636')
    binddn = "PITT\\twc17"
    pw = "MyPassword"

    # Try to bind to LDAP server
    try:
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(binddn, pw)
    except ldap.INVALID_CREDENTIALS:
        print("Invalid username/password for LDAP bind")
        sys.exit(0)
    except ldap.LDAPError, e:
        if type(e.message) == dict and e.message.key_key('desc'):
            print(e.message['desc'])
        else:
            print(e)
        sys.exit(0)

    user_input = get_input()
    print(user_input)

# Run the program
if __name__ == "__main__":
    main()
