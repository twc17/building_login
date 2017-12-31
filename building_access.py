#!/usr/bin/python

# Title: building_login.py
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
from building_functions import *

def main():
    """Main"""
    # File we will use to log all IN/OUT and ERROR activity
    log_file = "building_access.log"
    # Dictionary structure that will be used for running building log
    # db[Username] = first_name, last_name, time_in
    db = {}

    while True:
        # Testing to print the current building log
        print_log(db)
        try:
            # Swipe ID card or press Return for guest...
            user_input = get_input()

            # User hit enter and wants to deal with a guest
            if (user_input == 'GUEST'):
                guest = get_guest()
                # Check to see if the user 'GUEST' is logged in
                # If they are, remove them from the current log
                if guest[0] in db:
                    del_log(guest[0], db)
                    guest.append("OUT")
                    write_log(guest, log_file)
                # Else add the 'GUEST' user to the current log
                else:
                    add_log(guest[0], guest[1], guest[2], db)
                    guest.append("IN")
                    write_log(guest, log_file)
                continue

            # Handle bad inputs
            if (user_input == 'ERROR'):
                # Write error to log file and let the user know something went wrong
                write_log(['ERROR'], log_file)
                os.system('clear')
                print('\x1b[5;30;41m' + user_input + '\x1b[0m')
                time.sleep(2)
                continue

            # User didn't want to enter a guest, and we handled bad inputs,
            # so we now know that we're dealing with a Pitt ID card swipe
            result = query_ldap("*" + user_input + "*")

            # Sooo, information is really deep in some data structs
            # pitt_user = [username, first_name, last_name]
            pitt_user = [result[0][0][1]['cn'][0], result[0][0][1]['givenName'][0], result[0][0][1]['sn'][0]]

            # Check to to see if the user scanned from ID card is logged in
            # If they are, remove them from the current building log
            if pitt_user[0] in db:
                del_log(pitt_user[0], db)
                pitt_user.append("OUT")
                write_log(pitt_user, log_file)
            # Else add the user to the current building log
            else:
                add_log(pitt_user[0], pitt_user[1], pitt_user[2], db)
                pitt_user.append("IN")
                write_log(pitt_user, log_file)
        # Catch keyboard interrupt and exit gracefully
        except KeyboardInterrupt:
            print
            print("Exiting...")
            break

# Run the program
if __name__ == "__main__":
    main()
