# Check network status

Find the routes between two hosts
---
- traceroute
- mtr (my traceroute)


Practice 🖊️
---
- From your computer to a target, along the way, find 
  - the autonomous systems (ASes) 
  - the routers (hops)

```bash
# 1. find the autonomous systems (ASes)
mtr -zb www.google.com

## mtr is used to find the slowness or loss in traffic between two hosts
## let the MTR trace run for 10-15 minutes for better statistics results

# 2. find the routers (hops)
traceroute www.google.com # Linux & MacOS
tracert www.google.com # Windows

## Traceroute sends out three packets per TTL increment
## Each column corresponds to the time is took to 
## get one packet back (round-trip-time)
## - A traceroute packet could be routed along a different link than other attempts
## - A traceroute packet could be dropped, noted with *
```


[netcat(nc)](https://en.wikipedia.org/wiki/Netcat)
---
- read from and write to network connections using TCP or UDP
  - good for testing network programs
- a feature-rich network debugging and investigation tool which can perform
  - port scanning
  - file transferring 
  - port listening


Practice 🖊️
---
With netcat (nc), 
- transfer files between two terminals
- simulate a chat session
- hex-dump transmitted and received data


Check network status
---
- ip: show / manipulate routing, network devices, interfaces and tunnels
- netstat: Print network connections, routing tables, interface statistics, masquerade connections, and multicast memberships
- **ss**: another utility to investigate sockets


Practice 🖊️
---
```bash
# 1. find ip addresses of all interfaces
ip a

# 2. display all listening tcp ports
# describe the output differences 
netstat -ltp
sudo netstat -ltp 

# 3. display all listening udp ports
sudo ss -lup
```


[INetSim: Internet Services Simulation Suite](https://www.inetsim.org/requirements.html)
---
- simulates common internet services in a lab environment 
  - for analyzing the network behaviour of unknown malware samples
- modules for the simulation of [the following services](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers)
  - HTTP/HTTPS, SMTP/SMTPS, POP3/POP3S, DNS, FTP/FTPS, TFTP, 
  - IRC, NTP, Ident, Finger, Syslog, Dummy
  - Small services: Daytime, Time, Echo, Chargen, Discard, Quotd


Practice 🖊️
---
- install and run inetsim
- identify all ports used by inetsim
- request the inetsim services using netcat
- check the socket status with ss