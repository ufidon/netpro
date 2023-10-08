#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter10/timeapp_werkz.py
# A WSGI callable built using Werkzeug.
# Install Werkzeug:  pip install Werkzeug

# Werkzeug has not even made you remember the correct signature for a WSGI callable, 
# instead giving you a decorator that switches your function to 
# a far simpler calling convention. You receive a Werkzeug Request object
# automatically as your only argument and are given 
# the privilege of simply returning a Response object—the library
# will handle everything else for you

import time
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

@Request.application
def app(request):
    host = request.host
    if ':' in host:
        host, port = host.split(':', 1)
    if request.method != 'GET':
        return Response('501 Not Implemented', status=501)
    elif host != '127.0.0.1' or request.path != '/':
        return Response('404 Not Found', status=404)
    else:
        return Response(time.ctime())
    
if __name__ == '__main__':
     run_simple('localhost', 8000, app, use_reloader=True)   
