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
  

[TCP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)
---
- Transmission Control Protocol 
- reliable, ordered, and error-checked delivery of packets
- supports the majority of application protocols
  - HTTP, FTP, SMTP, POP3, SSH, etc.


How TCP works?
---
- every TCP packet is identified by a sequence number
  - the initial sequence number is randomly chosen
- next sequence number = current sequence number + current packet size in bytes
- TCP window - bursts of packets at a time expecting a single response
- builtin flow control
- automatic retransmission of unacknowledged packets


Establish and terminate TCP connection
---
- packet (sequence number, acknowledge number)
- three-way (or 3-step) handshake to establish
  - SYN (A, -), SYN-ACK (B, A+1), ACK (A+1, B+1)
- four-way handshake to terminate
  - FIN, ACK, FIN, ACK
- a TCP connection (client: active or connected socket, server: passive or listening socket)
  - e.g. (local ip : local port, remote ip : remote port)


💡 Demo
---
- Show the TCP connection 
  - establishment in three-way handshake
  - termination in four-way handshake


🖊️ Practice
---
- play with the simple [tcp server/client program](./tcp/tcp_sixteen.py)

```bash
# 1. run the client only and analyze the exception
python3 tcp_sixteen.py client localhost
# before send() and recv(), a TCP connection must be established first
# compare this with UDP

# 2. open two terminals, one runs server, the other runs client
python3 tcp_sixteen.py server ""

python3 tcp_sixteen.py client localhost
python3 tcp_sixteen.py client 127.0.0.1

# 3. comment out line 21 in  tcp_sixteen.py 
# run the server in another terminal
# analyze what happened
python3 tcp_sixteen.py server ""

# 4. bind to a specified interface
python tcp_sixteen.py server ip
```


Deadlock
---
- can occur in TCP applications without good design
  - TCP stack sending and receiving buffers are limited
  - send and receive lock mutually
- ways to solve deadlock
  - use non-blocking mode
  - use multiple threads
  - use select() or poll() to handle multiple inputs


🖊️ Practice
---
- try possible inputs that can put [tcp_deadlock.py](./tcp/tcp_deadlock.py) into deadlock

```bash
# open two terminals, one runs the server
python3 tcp_deadlock.py server ""

# in the other terminal, run the client
python tcp_deadlock.py client 127.0.0.1 32

# then try this, will it cause deadlock?
# will this happen to UDP?
 python tcp_deadlock.py client 127.0.0.1 16000000

```


Closed connections and half-open connections
---


Using TCP stream like files
---



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