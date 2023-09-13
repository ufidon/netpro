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


## Threaded and Multiprocess Servers

### The Legacy SocketServer Framework

## Async Servers

###  Callback-Style Asyncio

### Coroutine-Style Asyncio

### The Legacy Module Asyncore

### The Best of Both Worlds


## Running Under Inetd

## Deployment of network applications