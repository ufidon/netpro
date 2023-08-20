# TCP/IP stack

What the internet looks like?
---
- [The internet map](http://internet-map.net/)
- [The internet evolution](https://www.opte.org/the-internet)
- [IPv4 and IPv6 AS Core](https://www.caida.org/projects/as-core/)




Internet of Things (IoT)
---
- Cloud of Things (CoT)
- Web of Things (WoT)
- ![iot](../figs/iot.gif)


TCP/IP suite
---
- The internet protocol suite, abreviated as TCP/IP suite
- It organizes the set of communication protocols
- A TCP/IP suite implementation is called a TCP/IP stack

![tcp/ip stack](https://upload.wikimedia.org/wikipedia/commons/c/c4/IP_stack_connections.svg)


[Popular protocols on each layer](https://en.wikipedia.org/wiki/Internet_protocol_suite)
---
| layer | protocols |
| --- | --- |
| Application | BGP, DHCP(v6), DNS, FTP, HTTP (HTTP/3), HTTPS, IMAP, IRC, LDAP, MGCP, MQTT, NNTP, NTP, OSPF, POP, PTP, ONC/RPC, RTP, RTSP, RIP, SIP, SMTP, SNMP, SSH, Telnet, TLS/SSL, XMPP |
| Transport | TCP, UDP, DCCP, SCTP, RSVP, QUIC |
| Internet | IP (v4, v6), ICMP (v6), ARP, NDP, ECN, IGMP, IPsec |
| Link | Tunnels, PPP, MAC |


Questions ❓
---
- Which application protocols are suitable for video conferences?


Encapsulation and decapsulation of application data
---
![encap and decap](https://upload.wikimedia.org/wikipedia/commons/3/3b/UDP_encapsulation.svg)


Practice 🖊️
---
With Wireshark, 
- capture a data frame then
- explain the encapsulation and decapsulation of application data


TCP/IP stacks in Linux & Windows
---
- [Linux network sockets](https://www.beej.us/guide/bgnet/)
- [Windows Sockets 2 (Winsock)](https://learn.microsoft.com/en-us/windows/win32/WinSock/)


TCP/IP OS API wrappers, bindings, or libraries
---
- [The Python Standard Library](https://docs.python.org/3/library/)
  - [Awesome Python: A curated list of awesome Python frameworks, libraries, software and resources](https://github.com/vinta/awesome-python)
- [golang standard library: net -  portable interface for network I/O](https://pkg.go.dev/net)
  - [gnet: a high-performance, lightweight, non-blocking, event-driven networking framework](https://gnet.host/)
  - [Networking - Awesome Go: Libraries for working with various layers of the network](https://awesome-go.com/networking/)
  - [Awesome Go: A curated list of awesome Go frameworks, libraries, and software](https://github.com/avelino/awesome-go)
- [Awesome C++](https://github.com/fffaraz/awesome-cpp)
  - [Awesome Modern C++](https://github.com/rigtorp/awesome-modern-cpp)
- [Java networking](https://docs.oracle.com/en/java/javase/17/core/java-networking.html)
  - [Awesome Java](https://java-lang.github.io/awesome-java/)
- [Network programming in .NET](https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/overview)
  - [Awesome .net](https://github.com/quozd/awesome-dotnet)


# References
- [level-ip](https://github.com/saminiir/level-ip)
  - [doc](https://www.saminiir.com/lets-code-tcp-ip-stack-1-ethernet-arp/)
  - [How to Implement TCP/IP and UDP/IP for Embedded Systems](https://barrgroup.com/embedded-systems/how-to/embedded-tcp-ip)
- *TCP/IP stacks for SoCs*
  - [picoTCP](https://github.com/tass-belgium/picotcp)
  - [lwIP Lightweight IP stack](https://www.nongnu.org/lwip/)
    - [source code](https://git.savannah.nongnu.org/cgit/lwip.git)
  - [uip](https://github.com/adamdunkels/uip)
  - [FreeRTOS-Plus-TCP Open source and thread safe TCP/IP stack for FreeRTOS](https://www.freertos.org/FreeRTOS-Plus/FreeRTOS_Plus_TCP/index.html)
  - [CycloneTCP Embedded TCP/IP stack (dual IPv4/IPv6) for STM32](https://www.st.com/en/partner-products-and-services/cyclonetcp.html)
  - [Microchip's TCP/IP Stacks](https://www.microchip.com/en-us/software-library/tcpipstack)
  - [NDKTCPIP TI-RTOS Networking](https://www.ti.com/tool/NDKTCPIP)