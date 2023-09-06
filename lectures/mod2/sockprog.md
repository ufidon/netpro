# Socket programming

Access network information
---
- [source code](./code/socketpro.ipynb)
  ```bash
  sudo apt install  ipython3 jupyter jupyter-notebook
  ```

Get & set socket options
---
- make port number reusable
  - [source code](./code/reuseaddr.py)


## Basic socket programming

Endpoint: (IP : Port number)
---
- Source (8.8.8.8:53) -> Destination (10.0.2.5:46132)
- 3 types of UDP and TCP port numbers
  - well-known ports (0-1023)
  - registered ports (1024-49151)
  - free ports (49152-65535)

```python
# find well-known port number
import socket
socket.getservbyname('http') # ->80

# socket.getaddrinfo() can get port as well
```


[UDP](https://en.wikipedia.org/wiki/User_Datagram_Protocol)
---
- User Datagram Protocol
  - connectionless, unreliable
  - no guarantee of delivery, ordering, or duplicate protection
  - no congestion control, lightweight
- Suitable applications
  - time-sensitive
  - error tolerable
  - broadcast and multicast


🖊️ Practice
---
- Play with [udp_local.py](./udp/udp_local.py)
  ```bash
  # in two terminals, one runs udp server, 
  ./udp_local.py server

  # the other runs udp client
  ./udp_local.py client
  ./udp_local.py client
  ```
- Spoof the server
  ```bash
  # in the server terminal, ctrl+z suspend the server
  # in the client terminal, run the client
  ./udp_local.py client # note the port number Pclient

  # in the server terminal
  nc -u localhost Pclient # type something and enter
  # the client prints those typing and quit
  ```
- promiscuous client accepts every packet it received
  - identify requests and responses with unique id numbers


🖊️ Practice
---
- Unreliability, Backoff, Blocking, and Timeouts
- play with [udp_remote.py](./udp/udp_remote.py)
  ```bash
  # on seed vm, in the folder contains udp_remote.py
  python3 -m http.server

  # on parrot, access seed http.server by a browser
  # download udp_remote.py and run it
  python3 udp_remote.py server ""

  # on seed, 
  python3 udp_remote.py client parrotIP
  ```


🖊️ Practice
---
- UDP fragmentation  
  - play with [big_sender.py](./udp/big_sender.py) to find the MTU
    ```bash
    ./big_sender.py parrotIP

    ./big_sender.py 127.0.0.1
    ```
- broadcast vs. multicast
  - play with [udp_broadcast.py](./udp/udp_broadcast.py)
    ```bash
    # run multiple server
    ./udp_broadcast.py server ""

    # send message to broadcast address
    ./udp_broadcast.py client 10.0.2.255
    ```
  


Simple client/server programs
---
- simple TCP client/server programs
  - [TCP echo server](./code/tcpEchoServer.py)
  - [TCP echo client](./code/tcpEchoClient.py)
- simple UDP client/server programs
  - [UDP echo server](./code/udpEchoServer.py)
  - [UDP echo client](./code/udpEchoClient.py)


Handle socket errors
---
- [code](./code/hserror.py)


## Simple socket programs

Get time from the internet time server
---
- Network Time Protocol (NTP) can be used to synchronize your machine time with one of the internet time servers.
- Simple Network Time Protocol (SNTP) can be used to get the time from NTP server but not as accurate as NTP
  ```bash
  # install ntplib
  sudo apt install python3-pip
  pip3 install ntplib
  ```

# References
- [socket — Low-level networking interface](https://docs.python.org/3/library/socket.html)
- [argparse — Parser for command-line options, arguments and sub-commands](https://docs.python.org/3/library/argparse.html)
- [ntplib](https://pypi.org/project/ntplib/)