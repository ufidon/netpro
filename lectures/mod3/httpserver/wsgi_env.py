#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter10/wsgi_env.py
# A simple HTTP service built directly against the low-level WSGI spec.

# Refs: 
# 1. [Curl - Mark bundle as not supporting multiuse](https://stackoverflow.com/questions/71171194/curl-mark-bundle-as-not-supporting-multiuse-http-1-1-403)
# 2. [diazo - a theme engine](https://docs.diazo.org/)

from pprint import pformat
from wsgiref.simple_server import make_server

# a WSGI application is a callable that takes two arguments
# Other possibilities would be 
# a Python class
# or a class instance with a __call__() method
def app(environ, start_response):
    headers = {'Content-Type': 'text/plain; charset=utf-8'}
    start_response('200 OK', list(headers.items()))
    yield 'Here is the WSGI environment:\r\n\r\n'.encode('utf-8')
    yield pformat(environ).encode('utf-8')

if __name__ == '__main__':
    httpd = make_server('', 8000, app)
    host, port = httpd.socket.getsockname()
    print('Serving on', host, 'port', port)
    httpd.serve_forever()
