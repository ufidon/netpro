#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter06/safe_tls.py
# Simple TLS client and server using safe configuration defaults

import argparse, socket, ssl

def client(host, port, cafile=None):
    # 1. create a TLS context object 
    #   regarding certificate validation and choice of cipher.
    purpose = ssl.Purpose.SERVER_AUTH # verify the server
    context = ssl.create_default_context(purpose, cafile=cafile)
    # cafile : used to validate the remote end of your TLS connection
    # = specified, then only this specified cafile will be used
    # = None, then all of the system default CA certificates will be used
    #         call load_verify_locations() to install any further certificates if needed

    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((host, port))
    print('Connected to host {!r} and port {}'.format(host, port))

    # 2. let the OpenSSL library take control of the TCP connection, 
    #   exchange the necessary greetings with the other end, 
    #   and set up an encrypted channel
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)

    while True:
        # 3. perform all further communication with the ssl_sock
        #   with the same methods as a normal socket, 
        #   such as send() and recv() and close() 
        data = ssl_sock.recv(1024)
        if not data:
            break
        print(repr(data))

def server(host, port, certfile, cafile=None):
    purpose = ssl.Purpose.CLIENT_AUTH # accept client connections
    context = ssl.create_default_context(purpose, cafile=cafile)
    context.load_cert_chain(certfile)

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((host, port))
    listener.listen(1)
    print('Listening at interface {!r} and port {}'.format(host, port))
    raw_sock, address = listener.accept()
    print('Connection from host {!r} and port {}'.format(*address))
    
    ssl_sock = context.wrap_socket(raw_sock, server_side=True)

    ssl_sock.sendall('Simple is better than complex.'.encode('ascii'))
    ssl_sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Safe TLS client and server')
    parser.add_argument('host', help='hostname or IP address')
    parser.add_argument('port', type=int, help='TCP port number')
    parser.add_argument('-a', metavar='cafile', default=None,
                        help='authority: path to CA certificate PEM file')
    parser.add_argument('-s', metavar='certfile', default=None,
                        help='run as server: path to server PEM file')
    args = parser.parse_args()
    if args.s:
        server(args.host, args.port, args.s, args.a)
    else:
        client(args.host, args.port, args.a)
