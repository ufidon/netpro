#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter12/build_basic_email.py

# the modern EmailMessage builder carefully specifies 
# explicit values to ensure the highest level of interoperability 
# possible with modern tools

import email.message, email.policy, email.utils, sys

text = """Hello Biden,
This is a hello message from seed.
 - seed"""

def main():
    message = email.message.EmailMessage(email.policy.SMTP)

    # could we omit all the headers? try it
    # Header names are case insensitive
    message['To'] = 'biden@localhost'
    message['From'] = 'seed@localhost>'
    message['Subject'] = 'Test Message, from Trump to Biden'

    # date format required by the e-mail standards
    # a specific Python datetime or Greenwich Mean Time (GMT)
    # can also be used instead of local time zone
    message['Date'] = email.utils.formatdate(localtime=True)

    # message-id is carefully constructed to be unique
    message['Message-ID'] = email.utils.make_msgid()

    # set_content() and as_bytes() ensured that 
    # the e-mail message was properly terminated with a newline
    message.set_content(text)
    # no related resources, no alternative rendering, no attachment
    sys.stdout.buffer.write(message.as_bytes())

if __name__ == '__main__':
    main()
