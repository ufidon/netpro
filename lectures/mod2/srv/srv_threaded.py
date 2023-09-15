#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_threaded.py
# Using multiple threads to serve several clients in parallel.

import zen_utils
from threading import Thread # memory image and file descriptor space

#  multiprocessing.Process gives each thread of control 
# its own separate memory image and file descriptor space, 
# increasing expense from an operating system point of view but
# better isolating the threads and making it 
# much more difficult for them to crash a main monitor thread

def start_threads(listener, workers=4):
    t = (listener,)
    for i in range(workers):
        Thread(target=zen_utils.accept_connections_forever, args=t).start()

if __name__ == '__main__':
    address = zen_utils.parse_command_line('multi-threaded server')
    listener = zen_utils.create_srv_socket(address)
    # option 1: the main thread starts several server threads then exits
    start_threads(listener)

    # option 2: the main thread acts as a monitor
    # restarts replacement threads if any of them die