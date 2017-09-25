#!/usr/bin/python

# Title: building_login.py
#
# Author: Troy <twc17@pitt.edu>
# Date Modified: 09/25/2017
# Version: 1.3.5
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
# TODO: Find a way to make LDAP searches faster!

# Imports
import getpass, argparse, ldap, sys

def get_input():
    """Get ths users input for either their ID card swipe, or manually enter information

    Returns:
        Users input as string
    """
    user_input = getpass.getpass("Swipe Pitt ID Card or press 'Return' to sign in a guest...")

    if len(user_input) == 0:
        return "GUEST"
    else:
        card_number = user_input.split('=')
        if len(card_number) == 2:
            return card_number[0][-9:]
        else:
            return "ERROR"

def query_ldap(card_number):
    """Query Pitt LDAP server for users 2P number

    Arguments:
        card_number -- Pitt 2P number from ID card

    Returns:
        Result of LDAP query, as string
    """
    # LDAP bind settings
    l = ldap.initialize('ldaps://pittad.univ.pitt.edu:636')
    basedn = "ou=Accounts,dc=univ,dc=pitt,dc=edu"
    binddn = "PITT\\RS610085"
    pw = "sgcxtrp9"

    # Try to bind to LDAP server. Figured out that the bind
    # will eventually timeout, so we need to do it on every query :/
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

    # Attribute that we are searching for
    search_filter = "(PittPantherCardID=" + card_number + ")"
    # The attributes we want to return from the search
    search_attribute = ["cn", "sn", "givenName"]
    # This will scope one level below Accounts
    search_scope = ldap.SCOPE_ONELEVEL

    # Try to search 
    try:
        ldap_result_id = l.search(basedn, search_scope, search_filter, search_attribute)
        result_set = []
        while 1:
            result_type, result_data = l.result(ldap_result_id, 0)
            if (result_data == []):
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)

        l.unbind_s()
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
    while True:
        user_input = get_input()
        result = query_ldap("*" + user_input + "*")
        # Sooo, information is really deep in some data structs
        print("Username: " + result[0][0][1]['cn'][0])
        print("First name: " + result[0][0][1]['givenName'][0])
        print("Last name: " + result[0][0][1]['sn'][0])

# Run the program
if __name__ == "__main__":
    main()
