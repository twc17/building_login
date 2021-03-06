#!/usr/bin/python

# Title: building_functions.py
#
# Author: Troy <twc17@pitt.edu>
# Date Modified: 10/05/2017
# Version: 2.7.8
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
#       Make output look better! Then ready to try and break it!

# Imports
import getpass, os, ldap, sys, datetime, time

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
        if len(card_number) == 2 and card_number[0].isdigit():
            return card_number[0][-9:]
        else:
            return "ERROR"

def get_guest():
    """Gets keyboard input for adding or removing a guest

    Returns:
        Guests username, first name, last name
    """
    first_name = raw_input("Enter the guests first name: ")
    last_name = raw_input("Enter the guests last name: ")

    username = first_name[0].upper() + last_name.upper()

    return [username, first_name, last_name]

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

def add_log(user, first, last, db):
    """Add record to current building access log

    Arguments:
        user -- Pitt Username
        first -- First name
        last -- Last name
        db -- Database of current building log

    Returns:
        True if the add is successful, False otherwise
    """
    # Format the time 2013-09-18 11:16:32
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db[user] = [first, last, now]
    os.system('clear')
    print('\x1b[6;30;42m' + user + " logged IN!" + '\x1b[0m')
    time.sleep(2)
    return True

def del_log(user, db):
    """Delete record from the current building access log

    Arguments:
        user -- Pitt username to logout
        db -- Database of current building log

    Return:
        True if the delete is successful, False otherwise
    """
    if db.pop(user, False) is not False:
        os.system('clear')
        print('\x1b[6;30;42m' + user + " logged OUT!" + '\x1b[0m')
        time.sleep(2)
        return True
    else:
        return False

def write_log(entry, log_file):
    """Write add/del entry to log file

    Arguments:
        entry -- Entry to add to log file
                Will probably look something like 'USER,last,first,IN/OUT,date'
        log_file -- Log file to write entry to

    Return:
        True if write to log file was successful, False otherwise
    """
    # Open out log_file to work with
    log_file = open(log_file, 'a')
    # Format the time 2013-09-18 11:16:32
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = ",".join(entry)
    log_file.write(now + " " + entry + "\n")
    log_file.close()

def print_log(db):
    """Print out current building log nice and clean

    Arguments:
        db -- Currently building log

    Returns:
        None
    """
    building_log = []

    for key, value in db.iteritems():
        user_line = key + "," + ",".join(value)
        building_log.append(user_line)

    # Clear the window
    os.system('clear')

    # Sort list based on date/time stamp
    building_log.sort(key = lambda x: str(x.split(',')[3][-20:])) 

    max_username_len = 0
    max_first_name_len = 0
    max_last_name_len = 0

    for entry in building_log:
        entry = entry.split(',')
        if len(entry[0]) > max_username_len:
            max_username_len = len(entry[0])

        if len(entry[1]) > max_first_name_len:
            max_first_name_len = len(entry[1])

        if len(entry[2]) > max_last_name_len:
            max_last_name_len = len(entry[2])

        # print(entry[0] + '\t' + entry[1] + '\t' + entry[2] + '\t' + entry[3])
        print("%s %s %s %s" % (entry[0].center(max_username_len), entry[1].center(max_first_name_len), entry[2].center(max_last_name_len), entry[3].center(len(entry[3]))))
