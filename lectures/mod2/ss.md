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
---
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
tcpdump -n port 1060 -i lo -X
```


Best practice on Socket Wrapping
---
- create a configured SSLContext object 
  - that describes security requirements
- make the connection from client to server using a plain socket
- call the context’s wrap_socket() method to perform the actual TLS negotiation
- Alternatively, provide a prewrapped socket with do_handshake_on_connect keyword argument set to its default value of True
  - this is not suggested


Hand-Picked Ciphers and Perfect Forward Security
---
- Hand-Picked ciphers is preferred than default ciphers for 
  - strong security, or
  - security evaluation
- Perfect Forward Security (PFS) pushes the programmer to hand-specify the properties of the context object
-  if both the client and server are running on recent-enough versions of OpenSSL
   -  a PFS-capable cipher could be selected by default


🔭 Explore
---
- [Cipher suites](https://ciphersuite.info/cs/?sort=sec-desc)
- [Perfect Forward Secrecy and how to choose PFS based Cipher suites](https://blogs.sap.com/2018/12/09/perfect-forward-secrecy-and-how-to-choose-pfs-based-cipher-suites/)


💡 Demo
---
- Will the default context provide PFS?
  - Python will often make good choices without your having to be specific
  ```bash
  # open two terminal windows, one runs the server
  python3 safe_tls.py -s localhost.pem localhost 1234

  # the other runs the test with TLSv1.3
  python3 test_tls.py -a ca.crt localhost 1234

  # rerun the server, then run the test with TLSv1.2
  python3 test_tls.py -a ca.crt localhost 1234 -p TLSv1_2

  # rerun the server, then run the test with TLSv1.1
  python3 test_tls.py -a ca.crt localhost 1234 -p TLSv1_1
  ```
- Customize the context unless you know the ciphers, not suggested since 
  - cyber attack and defense evolve constantly
  - lacks flexibility
  ```python
  # the code snippet from the textbook FPNP e3
  # which was the latest when the book was writing
  # however it is deprecated today
  context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  context.verify_mode = ssl.CERT_NONE
  context.options |= ssl.OP_CIPHER_SERVER_PREFERENCE   # choose *our* favorite cipher
  context.options |= ssl.OP_NO_COMPRESSION             # avoid CRIME exploit
  context.options |= ssl.OP_SINGLE_DH_USE              # for PFS
  context.options |= ssl.OP_SINGLE_ECDH_USE            # for PFS
  context.set_ciphers('ECDH+AES128 ')                  # choose over AES256, says Schneier
  ```


Protocol Support for TLS
---
- Most of the widely used Internet protocols have by now added TLS support
- Important feature needed,  the TLS cipher and options can be configured to 
  - prevent peers from connecting with 
    - weak protocol versions, weak ciphers, 
    - or options such as compression that weaken the protocol
- TLS-aware protocols built in PSL
  - http.client, smtplib, poplib, imaplib, ftplib, nntplib can be used to build
    - HTTPSConnection object, SMTP_SSL object, POP3_SSL object, 
    - IMAP4_SSL object, FTP_TLS object, NNTP_SSL object respectively
  - their constructors ssl_context keyword can be set with an SSLContext of your own settings
  - support TLS in two ways
    - open the protocol’s new TLS port 
    - add TLS support atop the old plain-text protocol
      - except HTTP since it is stateless


Learning Details of the TLS protocol
---
- The PSL ssl module’s SSLSocket object can be used to 
  - introspect the state of the OpenSSL-powered connections 
  - see how they are configured
- SSLSocket object methods used for introspection

| method | description |
| --- | --- |
|  getpeercert() | returns a Python dictionary of fields picked out of the peer's X.509 certificate |
| cipher() | returns the name of the cipher that OpenSSL and the peer’s TLS implementation agreed over the TLS negotiation |
| compression() | returns the name of the compression algorithm in use or None |


🖊️ Practice
---
- [Connect to Any TLS Endpoint and Report the Cipher Negotiated](./ss/features.py)
  ```bash
  # 1. learn the parameters
  python3 features.py -h

  # 2.1 open two terminal windows, one runs the server
  python3 safe_tls.py -s localhost.pem '' 1060

  # 2.2 the other runs the client with a week cipher
  python3 test_tls.py -C 'RC4' -a ca.crt localhost 1060
  # try AES
  python3 test_tls.py -C 'AES' -a ca.crt localhost 1060 

  # 3.1 downgrade TLS test, open two terminal windows, 
  # one runs the server
  python3 test_tls.py -s localhost.pem localhost 1234 -C 'AES' -p TLSv1
  
  # the other runs
  python3 safe_tls.py -a ca.crt localhost 1234

  # 4. find the ciphers matching a specified cipher string supported by OpenSSL
  openssl ciphers -v 'ECDH+AES256'
  openssl ciphers -v 'ECDH+AES128'
  # the ciphers in the output list can be used in set_ciphers()
  # not suggested for manual setting
  ```


# References
- [ITS350 Lab08: Public Key Infrastructure](https://github.com/ufidon/its350/tree/master/labs/lab08)
- [Python3 "DeprecationWarning: ssl.PROTOCOL_TLSv1_2 is deprecated sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)" error](https://stackoverflow.com/questions/72306332/python3-deprecationwarning-ssl-protocol-tlsv1-2-is-deprecated-sslcontext-ssl)