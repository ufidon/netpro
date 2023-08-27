# Socket programming

Access network information
---
- [source code](./code/socketpro.ipynb)


Get & set socket options
---
- make port number reusable
  - [source code](./code/reuseaddr.py)


Basic socket programming
---
- simple TCP client/server programs
  - [TCP echo server](./code/tcpEchoServer.py)
  - [TCP echo client](./code/tcpEchoClient.py)
- simple UDP client/server programs
  - [UDP echo server](./code/udpEchoServer.py)
  - [UDP echo client](./code/udpEchoClient.py)
- handle socket errors
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
