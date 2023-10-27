#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter12/build_unicode_email.py

import email.message, email.policy, sys

# a quoted-printable content encoding for the body, 
# written in any language in utf-8, 
# the default source code encoding for python3
# avoids generating a block of Base64 data 
# shown in the output

text = """\
云想衣裳花想容。
春风拂槛露华浓。
若非群玉山头见。
会向瑶台月下逢。"""

def main():
    message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = '武则天 <recipient@example.com>'
    message['From'] = '李白 <sender@example.com>'
    message['Subject'] = '春'
    message['Date'] = email.utils.formatdate(localtime=True)
    message.set_content(text, cte='quoted-printable')
    sys.stdout.buffer.write(message.as_bytes())

if __name__ == '__main__':
    main()
