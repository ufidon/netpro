#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter17/connect.py

# connects to a remote server, 
# displays the welcome message, 
# and prints the current working directory

import sys, argparse
from ftplib import FTP

def main(ftpsite):
    # try [Ram's list of FTP sites](http://robotics.stanford.edu/people/ramkumar/ftp.html)
    ftp = FTP(ftpsite)
    print("Welcome:", ftp.getwelcome())
    ftp.login()
    print("Current working directory:", ftp.pwd())
    ftp.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Connect to FTP site')
    parser.add_argument('ftpsite', help='FTP site')
    args = parser.parse_args()
    main(args.ftpsite)
