#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter10/timeapp_webob.py
# A WSGI callable built using webob.
# Refs:
# - [Another Do-It-Yourself Framework](https://docs.pylonsproject.org/projects/webob/en/stable/do-it-yourself.html#serving-your-application)

# Install WebOb: pip install WebOb
# WebOb already implements the two common patterns of wanting 
# to examine the hostname from the Host header
# separately from any optional port number that might be attached 
# and of looking at the path without its trailing query string. 
# It also provides a Response object that knows all about 
# content types and encodings—it defaults to plain text—
# so that you need only to provide a string for the response body, 
# and WebOb will take care of everything else.

#  The WebOb Response class lets you treat the two pieces of 
# a Content-Type header like text/plain;
# charset=utf-8 as two separate values, 
# which it exposes as the separate attributes content_type and charset

import time, webob
from wsgiref.simple_server import make_server
def app(environ, start_response):
    request = webob.Request(environ)
    if environ['REQUEST_METHOD'] != 'GET':
        response = webob.Response('501 Not Implemented', status=501)
    elif request.domain != '127.0.0.1' or request.path != '/':
        response = webob.Response('404 Not Found', status=404)
    else:
        response = webob.Response(time.ctime())
    return response(environ, start_response)

if __name__ == '__main__':
    httpd = make_server('', 8000, app)
    host, port = httpd.socket.getsockname()
    print('Serving on', host, 'port', port)
    httpd.serve_forever()