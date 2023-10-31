#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter15/open_imap.py
# Opening an IMAP connection with the powerful IMAPClient

# Fix the program with the two references below
# 1.
# [Dovecot SSL configuration](https://ubuntu.com/server/docs/mail-dovecot)
# ssl_cert = </etc/dovecot/private/dovecot.pem
# ssl_key = </etc/dovecot/private/dovecot.key
# 2.
# create a context that will use custom CA certificate. 
# This is required to perform verification of 
# a self-signed certificate used by the IMAP server.
# [Use a self-signed certificate](https://imapclient.readthedocs.io/en/3.0.0/concepts.html#tls-ssl)
# 3. or set ssl=False for test purpose only


import getpass, sys
from imapclient import IMAPClient

def main():
    if len(sys.argv) != 3:
        print('usage: %s hostname username' % sys.argv[0])
        sys.exit(2)

    hostname, username = sys.argv[1:]
    c = IMAPClient(hostname, ssl=True)
    try:
        c.login(username, getpass.getpass())
    except c.Error as e:
        print('Could not log in:', e)
    else:
        # Each line of data comes back as a tuple, 
        # giving you the folder flags, folder name delimiter, and folder name,
        # and the flags themselves are a sequence of strings

        """
        The standard flags listed for each folder may be zero or more of the following:
 
        \Noinferiors: This means that the folder does not contain any subfolders and that it is
        impossible for it to contain subfolders in the future. Your IMAP client will receive an error if it
        tries to create a subfolder within this folder.
        
        \Noselect: This means that it is not possible to run select_folder() on this folder; that
        is, this folder does not and cannot contain any messages. (Perhaps it exists just to allow
        subfolders beneath it, as one possibility.)

        \Marked: This means that the server considers this box to be interesting in some way.
        Generally, this indicates that new messages have been delivered since the last time the folder
        was selected. However, the absence of \Marked does not guarantee that the folder does not
        contain new messages; some servers simply do not implement \Marked at all.
        
        \Unmarked: This guarantees that the folder doesn’t contain new messages.
        Some servers return additional flags not covered in the standard. Your code must be able to accept and ignore
        those additional flags.
        """

        print('Capabilities:', c.capabilities())
        print('Listing mailboxes:')
        data = c.list_folders()
        for flags, delimiter, folder_name in data:
            print('  %-30s%s %s' % (' '.join(flags), delimiter, folder_name))
    finally:
        c.logout()

if __name__ == '__main__':
    main()
