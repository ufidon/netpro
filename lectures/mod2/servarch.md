# Server Architectures
FPNP Ch 7


The aphorisms of the Zen of Python
---
- a poem about the inner consistent design of the Python language
- Run Python and type import this to show it


A Simple Protocol
---
- the client asks one of three plain-text ASCII questions 
   -  then waits for the server to complete its answer
- The end of each question is delimited with the ASCII question mark character ?
- the end of each answer is delimited with a period .
- close the connection without any warning when it has no more questions
- Each of the three question-and-answer pairs is based on 
  - one of the aphorisms of the Zen of Python
- packaged in [zen_utils.py](./srv/zen_utils.py)


The central patterns of a server process
---
- implemented in the final four routines in [zen_utils.py](./srv/zen_utils.py)


💡 Demo
---
- Go through [zen_utils.py](./srv/zen_utils.py)
- Play with [client.py](./srv/client.py)
  ```bash
  # normal play
  python3 client.py 127.0.0.1
  # cause mistakes to investigate the server response
  python3 client.py -e 127.0.0.1
  ```

A Single-Threaded Server
---
- The server can only handle a single connection at a time


🖊️ Practice
---
- Play with the [single-threaded server](./srv/srv_single.py)
  
```bash
## 1. Functionality test
# open three terminals, one runs the server
python3 srv_single.py 127.0.0.1 # or
python3 srv_single.py "" # listens on all interfaces

# run the client in the second terminal
python3 client.py 127.0.0.1 # play normally
python3 client.py -e 127.0.0.1 # see whether the server can handle mistakes

# in the third terminal, run one more client
python3 client.py 127.0.0.1 # see whether the server can handle multiple clients

## 2. Robustness test
# launch a DoS attack on this server with netcat
nc localhost 1060 # keep this running, the server will not able to accept other clients

# the server may set timeout to avoid waiting forever
# but this can be defeated by launching nc frequently enough

## 3. Performance test
# -m trace: use the trace module from PSL to time how long  each line 
# in the single threaded server takes
# Each line of output gives the moment when it starts execution,
# counted in seconds from when the server is launched
# --ignore-dir=/usr: ignore PSL, output only server code
# further info: python3 -m trace --help
python3 -m trace -tg --ignore-dir=/usr srv_single.py ""

# then launch a client to interact with the server
```


Threaded and Multiprocess Servers
---
- serve multiple clients simultaneously
  - by exploiting OS builtin support fo multiprocess and multithread
  - a master thread with an accept() loop that hands off the new client sockets to  waiting queue of workers (thread pool)
- advantage:
  - simple: launch several copies of the single-threaded server
  - suitable for in-house services without resourse coordination between threads
- disadvantage:
  - the OS concurrency mechanisms scale is limited
  - OSes rarely scale well to thousands or more threads running concurrently


🖊️ Practice
---
- Play with [multithreaded server](./srv/srv_threaded.py)

```bash
# open three terminals, one runs the server
python3 srv_threaded.py localhost
# in the other two terminals, run a client in each
python3 client.py localhost
```


The Legacy *SocketServer* Framework
---
- built into the Python Standard Library
- breaks into two patterns
  - the server pattern: opens a listening socket and accept new client connections, from
  - the handler pattern:  converses over an open socket
- These two patterns are combined by instantiating a server object 
  - that is given a handler class as one of its arguments
- lets the pool of connecting clients determine how many threads to start
  - vulnerable to DoS attack
  - not recommended for production services

🖊️ Practice
---
- Play with [socketserver framework](./srv/srv_legacy1.py)

```bash
# open three terminals, one runs the server
python3 srv_legacy1.py localhost
# in the other two terminals, run a client in each
python3 client.py localhost
```


Async Servers
---
- hear from a whole list of waiting client sockets 
  - respond whenever one of those clients is ready for more interaction
- supported by two features of modern OS network stacks
  - they supply system calls that lets a process block waiting on a whole list of client sockets
  -  a socket can be configured as nonblocking
     -  in nonblocking mode, send() or recv() call always return immediately
- asynchronous means
  -  the client code never stops to wait for a particular client 
  -  it switches freely among all connected clients to serve
- the system calls support asynchronous mode
  - the POSIX (Portable Operating System Interface) call select()
    - inefficient, not recommended
  - modern poll() on Linux and epoll() on BSD


🖊️ Practice
---
- Play with [Asynchronous server](./srv/srv_async.py)

```bash
# open three terminals, one runs the server
python3 srv_async.py localhost
# in the other two terminals, run a client in each
python3 client.py localhost
```

[Asyncio framework - Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)
---
- a new framework in the PSL introduced from Python 3.4
- provides a *standard interface* for event loops based on select(), epoll(), and similar mechanisms
- supports two programming styles
  - callback style
  - coroutine style



[Callback-Style Asyncio](https://docs.python.org/3/library/asyncio-protocol.html)
---
-  lets the programmer keep up with each open client connection by means of an object instance
- advances a client conversation using method calls on the object
- further deferred I/O such as database I/O needs *futures* objects to provide further callbacks


🖊️ Practice
---
- Play with [Asynchronous server](./srv/srv_asyncio1.py)

```bash
# open three terminals, one runs the server
python3 srv_asyncio1.py localhost
# in the other two terminals, run a client in each
python3 client.py localhost
```


Coroutine-Style Asyncio
---
- a [coroutine](https://docs.python.org/3/library/asyncio-task.html) is a function that pauses when it wants to perform I/O
  - returning control to its caller—instead of blocking in an I/O routine itself
  - supported by generators which have one or more yield statements
  - generates a sequence of items instead of terminating with a single return value when called
- asyncio takes advantage of the extended yield syntax which
  - allows a running generator to reel off all the items yielded by another generator with the *yield from* statement
  - allows yield to return a value to the inside of the coroutine
  - raises an exception if the consumer demands it


🖊️ Practice
---
- Play with [Asynchronous server](./srv/srv_asyncio2.py)

```bash
# open three terminals, one runs the server
python3 srv_asyncio2.py localhost
# in the other two terminals, run a client in each
python3 client.py localhost
```


The Legacy Module Asyncore
---
- two PSL modules, for backwards compatibility only
  - asyncore: [Asynchronous socket handler](https://docs.python.org/3/library/asyncore.html)
  - asynchat: [Asynchronous socket command/response](https://docs.python.org/3/library/asynchat.html)
  - many socket level details are packaged (hidden)
- For new code asyncio is recommended


🖊️ Practice
---
- Play with [Asynchronous server](./srv/srv_legacy2.py)

```bash
# open three terminals, one runs the server
python3 srv_legacy2.py localhost
# in the other two terminals, run a client in each
python3 client.py localhost
```

Summary
---
-  Multithreading and multiprocessing run single-threaded code without modification
-  An asynchronous approach breaks up code into little pieces that can each run without ever blocking
   -  A callback style wraps each unblockable code snippet inside a method
   -  A coroutine style encloses each basic unblockable operation in between yield or yield from statements
- An asynchronous server 
  - can serve clients with far less expense without context switch
  - but is limited by the capability of the OS thread since it does all of its work within a single thread
    - overcomed by using asynchronous callback object or coroutine and launch it under an asynchronous framework
- Deployment of servers is another big topic



# References
- [Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/)
- [Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html)
  - [How to Use Generators and yield in Python](https://realpython.com/introduction-to-python-generators/)
- [Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/)