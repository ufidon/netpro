# Peer-to-peer programming

Peer-to-peer (P2P) network
---
- a type of network architecture without a central server
  - nodes are connected directly to each other 
  - each node acts as both a client and a server
  - nodes share resources and information mutually
- usage
  - file sharing such as BitTorrent, Gnutella, eDonkey2000
  - communication such as Skype, Tox, IRC (Internet Relay Chat)
  - blockchain supported cryptocurrency such Bitcoin, Etherium
- advantages
  - decentralized so no single point of failure
  - not controlled by a single authority or organization
  - efficient since resources and information are shared directly with each other
- disadvantages
  - no central authority to filter out malicious content
  - security and privacy concerns due direct sharing of information
  - can be more vulnerable to spam and malware


🔭 Explore
---
- [List of P2P protocols](https://en.wikipedia.org/wiki/List_of_P2P_protocols)
- [Peer-to-peer file sharing](https://en.wikipedia.org/wiki/Peer-to-peer_file_sharing)


P2P programs
---
- the programs for the client and server in the CS network are usually different
  - the server provides services at specified port number
  - the client requests for services by connecting to the server
- the program for each node in P2P network is usually identical
  - or similar but different for different groups of P2P nodes with different roles
  - serve as both client and server
- handle issues like
  - connectivity
    - how to find and connect to other P2P Nodes?
  - instability
    - nodes frequently join and leave the network
  - message routing
    - how messages are routed from one node to another which may not know each other directly?
  - searching
    - how to find desired information from other nodes?
  - security
    - how nodes trust each other?
    - how to identify and remove malicious nodes?
    - how to send and receive information anonymously and securely?


The typical components of a P2P program
---
- user interface, uses the node as a client
  - configure and interact with the node
  - search and connect to other nodes
  - communicate with or find information from other nodes
- main loop, uses the node as a server
  - listens on a port 
  - accepts connections from other peers
  - starts handle threads to communicate with the accepted peers
- data contained in each node
  - a list of peers
  - peer information
  - data, message, or file to be shared


💡 Demo
---
- A simple p2p example using [python-p2p](https://github.com/GianisTsol/python-p2p)
  ```bash
  # install python-p2p and its dependency pycryptodome
  pip install pycryptodome
  pip install pythonp2p
  ```
- [twonodes.py](./p2p/twonodes.py)


🔭 Explore
---
- [A simple p2p network in Python twisted](https://benediktkr.github.io/dev/2016/02/04/p2p-with-twisted.html)



# References
- [Peer-to-Peer Programming](https://cs.berry.edu/~nhamid/p2p/)
- [A simple p2p network in Python twisted](https://benediktkr.github.io/dev/2016/02/04/p2p-with-twisted.html)
  - [Twisted: An event-driven networking engine written in Python](https://twisted.org/)
- [Blockchain from scratch – Creating a Peer-to-Peer network using Python](https://laconicml.com/create-blockchain-scratch-network-python/)
- [ØMQ - The Guide](https://zguide.zeromq.org/)
- [p2p-python](https://pypi.org/project/p2p-python/)
  - [source](https://github.com/GianisTsol/python-p2p)