#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter17/advbinarydl.py

import os, sys
from ftplib import FTP

def main():
    if os.path.exists('linux-1.0.tar.gz'):
        raise IOError('refusing to overwrite your linux-1.0.tar.gz file')

    ftp = FTP('ftp.kernel.org')
    ftp.login()
    ftp.cwd('/pub/linux/kernel/v1.0')
    ftp.voidcmd("TYPE I")
    '''
    voidcmd passes an FTP command directly to the server and checks for an error, 
    but returns nothing. In this case, the raw command is TYPE I. This sets 
    the transfer mode to “image,” which is how FTP refers internally to binary files. 
    In the previous example, retrbinary() automatically ran this command behind the scenes, 
    but the lower-level ntransfercmd() does not.
    '''

    #  the socket below is just a plain TCP socket
    # the size is merely an estimate
    socket, size = ftp.ntransfercmd("RETR linux-1.0.tar.gz")
    nbytes = 0

    f = open('linux-1.0.tar.gz', 'wb')

    while True:
        data = socket.recv(2048)
        if not data:
            break
        f.write(data)
        nbytes += len(data)
        print("\rReceived", nbytes, end=' ')
        if size:
            print("of %d total bytes (%.1f%%)"
                  % (size, 100 * nbytes / float(size)), end=' ')
        else:
            print("bytes", end=' ')
        sys.stdout.flush()

    print()
    f.close()
    socket.close()
    ftp.voidresp()
    '''
    voidresp() reads the command response code from the server, 
    raising an exception if there was any error during transmission
    '''
    ftp.quit()

if __name__ == '__main__':
    main()
