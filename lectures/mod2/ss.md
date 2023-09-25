# Secure sockets


[TLS/SSL](https://en.wikipedia.org/wiki/Transport_Layer_Security)
---
- Transport Layer Security (TLS)/ Secure Sockets Layer (SSL) 
- A crytographic protocol that provides communications security over a computer network
  - privacy (confidentiality), integrity, and authenticity by certificates, between two or more communicating computer applications
  - runs in the presentation layer
  - composed of two layers: the TLS record and the TLS handshake protocols
- Widely used in email, instant messaging, voice over IP, and Hypertext Transfer Protocol Secure (HTTPS) 


What TLS Does Not Protect in the the TLS-encrypted socket?
---
- Secures connection data payload only
- but not the information in the IP header of each packet
  - the IP addresses of both client and server
  - the port numbers of both client and server
- The DNS request made by the client to learn the server’s IP address
- the size of the chunks of data that pass in each direction 
- the overall pattern of requests and responses
- securer ways 
  - online anonymity networks like Tor and anonymous remailers
  - [Internet Protocol Security (IPsec)](https://en.wikipedia.org/wiki/IPsec)
  - [Domain Name System Security Extensions (DNSSEC) ](https://en.wikipedia.org/wiki/Domain_Name_System_Security_Extensions)



🍎 Example
---
- Describe the patterns that could be observed while browsing a HTTPS website $w$ such as https://gaia.cs.umass.edu/kurose_ross/online_lectures.htm
  - a DNS query for $w$ is sent out first from the browser
  - the purpose of the subsequent conversations with that IP address of $w$ at port 443 are for viewing the webpages on $w$
  - the HTTP request and response can be identified since HTTP is a *lock-step* protocol
    - a complete request followed by a complete response
  -  the size of each returned document and the order in which they were fetched


🔭 Explore
- [ssl — TLS/SSL wrapper for socket objects](https://docs.python.org/3/library/ssl.html)



Python 3.4+ Default Contexts
---
- introduces ssl.create_default_context()
  - makes it easy to use TLS security in Python applications
- under this default contexts
  - Both the client and server will 
    - negotiate the TLS version to use
    - refuse to speak the old protocols SSLv2 and SSLv3 with known weaknesses
  - identity verification with signed certificate
    - client is usually not required by setting verify_mode to ssl.CERT_NONE
    - server is always required by setting verify_mode to ssl..CERT_REQUIRED
  - choice of ciphers
    - client supports  a larger list of possible ciphers
      - even down to the old RC4 stream cipher
    - server prefers modern ciphers that provide [Perfect Forward Security (PFS)](https://en.wikipedia.org/wiki/Forward_secrecy)
      - assures that session keys will not be compromised even if long-term secrets used in the session key exchange are compromised


🖊️ Practice
---
- Go through the source code of [safe_tls.py](./ss/safe_tls.py)

```bash
# open two terminals, and play with the following scenarios
# one terminal runs server, the other runs client
# 1. run the server
python3  safe_tls.py -s localhost.pem '' 1060

# 2.1 run the client without ca file
# both the client and server will be crashed
python3 safe_tls.py localhost 1060

# 2.2 run the client with ca file after rerun the server first
python3 safe_tls.py -a ca.crt localhost 1060

# 3. use wireshark to capture and analyze the whole communication
# or with tcpdump
tcpdump -n port 1060 -i lo –X
```


Variations on Socket Wrapping
---


Hand-Picked Ciphers and Perfect Forward Security


Protocol Support for TLS


Learning Details


# References
- [ITS350 Lab08: Public Key Infrastructure](https://github.com/ufidon/its350/tree/master/labs/lab08)