#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter15/open_imaplib.py
# Opening an IMAP connection with the pitiful Python Standard Library

import getpass, imaplib, sys

def main():
    if len(sys.argv) != 3:
        print('usage: %s hostname username' % sys.argv[0])
        sys.exit(2)

    hostname, username = sys.argv[1:]
    m = imaplib.IMAP4_SSL(hostname)
    m.login(username, getpass.getpass())
    try:
        # all returns are raw data protocol-specific quoting
        # each return is a mix of different sequences: 
        # the flags are still uninterpreted byte strings, 
        # while each delimiter and folder name has been decoded to a real Unicode string
        
        print('Capabilities:', m.capabilities)
        print('Listing mailboxes ')
        status, data = m.list() # wrap the LIST command
        print('Status:', repr(status))
        print('Data:')
        for datum in data:
            print(repr(datum))
    finally:
        m.logout()

if __name__ == '__main__':
    main()
