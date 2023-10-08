#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter10/timeapp_raw.py
# A simple HTTP service built directly against the low-level WSGI spec.

# Each HTTP request names a coordinate in the space of 
# possible methods, hostnames, and paths.
#  your code must do all of the negative work of 
# determining which hostnames, paths, and methods 
# do not match the services you intend to provide

import time
from pprint import pformat
from wsgiref.simple_server import make_server

def app(environ, start_response):
    host = environ.get('HTTP_HOST', '127.0.0.1')
    path = environ.get('PATH_INFO', '/')
    if ':' in host:
        yield host.encode('utf-8')
        host, port = host.split(':', 1)
    if '?' in path:
        yield path.encode('utf-8')
        path, query = path.split('?', 1)
    headers = [('Content-Type', 'text/plain; charset=utf-8')]
    if environ['REQUEST_METHOD'] != 'GET':
        start_response('501 Not Implemented', headers)
        yield b'501 Not Implemented'
    elif host != '127.0.0.1' or path != '/':
        start_response('404 Not Found', headers)
        yield b'404 Not Found'
    else:
        start_response('200 OK', headers)
        yield time.ctime().encode('utf-8')

if __name__ == '__main__':
    httpd = make_server('', 8000, app)
    host, port = httpd.socket.getsockname()
    print('Serving on', host, 'port', port)
    httpd.serve_forever()