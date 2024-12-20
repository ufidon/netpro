#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter15/folder_summary.py
# Opening an IMAP connection with IMAPClient and retrieving mailbox messages.

# downloads all of the messages from the INBOX folder into your computer’s memory 
# in a Python data structure, and then displays a bit of summary information 
# about each one.

import email, getpass, sys
from imapclient import IMAPClient

def main():
    if len(sys.argv) != 4:
        print('usage: %s hostname username foldername' % sys.argv[0])
        sys.exit(2)

    hostname, username, foldername = sys.argv[1:]
    # c = IMAPClient(hostname, ssl=True)
    c = IMAPClient(hostname, ssl=False)
    try:
        c.login(username, getpass.getpass())
    except c.Error as e:
        print('Could not log in:', e)
    else:
        print_summary(c, foldername)
    finally:
        c.logout()

def print_summary(c, foldername):
    # select_folder() to put yourself “inside” the given folder
    #  close_folder() if you want to leave
    c.select_folder(foldername, readonly=True)

    #  'BODY.PEEK[]' is the way to ask IMAP for the “whole body” of the message
    #  PEEK indicates that you are just looking inside the message to build a summary, 
    # and that you do not want the server to set the \Seen flag automatically on all of 
    # these messages

    #  The range '1:*' means “the first message through the end of the mail folder,” 
    # because message IDs—whether temporary or UIDs—are always positive integers.
    
    msgdict = c.fetch('1:*', ['BODY.PEEK[]'])

    # The dictionary that is returned maps message UIDs to dictionaries 
    # giving information about each message. 
    for message_id, message in list(msgdict.items()):
        body = message[b'BODY[]'].decode('utf-8', errors='replace')  # Decode bytes to string
        e = email.message_from_string(body)
        print(message_id, e['From'])
        payload = e.get_payload()
        if isinstance(payload, list):
            part_content_types = [ part.get_content_type() for part in payload ]
            print('  Parts:', ' '.join(part_content_types))
        else:
            print('  ', ' '.join(payload[:60].split()), '...')

if __name__ == '__main__':
    main()
