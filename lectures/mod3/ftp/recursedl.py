#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter17/recursedl.py

# Detecting Directories and Recursive Download
# downloading entire trees of files from the server

from ftplib import FTP, error_perm

def walk_dir(ftp, dirpath):
    original_dir = ftp.pwd()
    try:
        ftp.cwd(dirpath)
    except error_perm:
        return  # ignore non-directores and ones we cannot enter
    print(dirpath)
    names = sorted(ftp.nlst())
    for name in names:
        walk_dir(ftp, dirpath + '/' + name)
    '''
    the only foolproof way to know if an entry is a directory 
    that you are allowed to enter is to try running cwd() against it.
    '''
    ftp.cwd(original_dir)  # return to cwd of our caller

def main():
    ftp = FTP('ftp.kernel.org')
    ftp.login()
    walk_dir(ftp, '/pub/linux/kernel/Historic/old-versions')
    ftp.quit()

if __name__ == '__main__':
    main()
