## Peer-to-Peer (P2P) Programming

### Overview:
This lab introduces you to the fundamentals of peer-to-peer (P2P) networking by creating a simple file-sharing application using Python. You will incrementally implement a P2P program where multiple peers can connect, share files, and download files from each other.

In your report, 
- 🎏 explain the code you added or modified
- 💻 illustrate with screenshots of corresponding outputs


### Lab Objectives:
1. Understand how P2P networks work, their major components, and work flows.
2. Build a simple P2P system where peers share files.
3. Gracefully handle peer connections and disconnections.
4. Implement peer discovery, file searching, and file requests between peers.

---

### Task 1: **Get Familiar with P2P Programming for File Sharing**

In this task, you will study a basic P2P system where each peer (node) can act as both a client and a server. This will help you understand the flow of file sharing in a P2P network.

🎏 **Understand the key components**:
   - `Server`: Waits for incoming connections from other peers and responds to requests.
   - `Client`: Connects to a peer and downloads requested files.
   - `Shared files directory`: Each peer has a folder containing the files it is willing to share.
   - `Console`: Command-based user interface, supports the commands below

| Command | Description |
| --- | --- |
| `help` / `?` | Show usage of all commands |
| `scan` | Discover active peers. For demonstration, limit the peer_ids range from 5000 to 5009.  |
| `lp` | List connected peers. |
| `connect <peer_id>` | Connect to a peer |
| `disconnect <peer_id>` | Disconnect from a peer |
| `sf <filename>` | Search for files on all connected peers |
| `request <filename> <peer_id>` | Request a file from a peer |
| `quit` | Quit the program |


🎏 **Complete Task 1 in the basic P2P program**:  

- 🎏 Complete Task 1 in the basic P2P program [p2p0.py](./p2p0.py) provided.
  - 🎏 Implement command `help`, i.e. `?`, or newline only.
  - 🎏 Add usage to each command.
    ```python
    # Reference code, for example
    elif commands[0] == "connect":  # connect peer_id
        if len(commands) == 2:
            print(f'Connect to peer {commands[1]}')
        else:
            print('Usage: connect <peer_id>')
    ```
  - 🖥️ Explain your code in the report and illustrate with output screenshots
- 🎏 Describe the major components of this P2P program and how they work together
- 🎏 Describe a complete file request scenario:
  - start the program
  - find active peers
  - connect to active peers
  - search for files
  - request for files
  - disconnect from peers
  - quit the program

- 🖥️ Sample output
  ```
  python3 p2p1.py

    Enter your port (e.g., 5000, 5001, etc.): 5000
    >:Node listening on 127.0.0.1:5000


    help / ?: Show usage of all commands.
    scan: Discover active peers. For demonstration, limit the peer_id range from 5000 to 5009.
    lp: List connected peers.
    connect <peer_id>: Connect to a peer.
    disconnect <peer_id>: Disconnect from a peer.
    sf <filename>: Search for a file on all connected peers.
    request <filename> <peer_id>: Request a file from a peer.
    quit: Quit the program.

    >:help

    help / ?: Show usage of all commands.
    scan: Discover active peers. For demonstration, limit the peer_id range from 5000 to 5009.
    lp: List connected peers.
    connect <peer_id>: Connect to a peer.
    disconnect <peer_id>: Disconnect from a peer.
    sf <filename>: Search for a file on all connected peers.
    request <filename> <peer_id>: Request a file from a peer.
    quit: Quit the program.

    >:?

    help / ?: Show usage of all commands.
    scan: Discover active peers. For demonstration, limit the peer_id range from 5000 to 5009.
    lp: List connected peers.
    connect <peer_id>: Connect to a peer.
    disconnect <peer_id>: Disconnect from a peer.
    sf <filename>: Search for a file on all connected peers.
    request <filename> <peer_id>: Request a file from a peer.
    quit: Quit the program.

    >:scan
    Discover active peers.
    >:lp
    List connected peers.
    >:connect 
    Usage: connect <peer_id>
    >:connect 5001
    Connect to peer 5001
    >:disconnect
    Usage: disconnect <peer_id>
    >:disconnect 5001
    Disconnect from peer 5001
    >:sf
    Usage: sf <filename>
    >:sf SkyPalace.jpg
    Search for SkyPalace.jpg on all connected peers
    >:request SkyPalace.jpg
    Usage: request <filename> <peer_id>
    >:request SkyPalace.jpg 5001
    Request file SkyPalace.jpg from peer 5001.
    >:quit
    All sockets closed. Exiting program.
  ```

### Task 2: **Discover and Connect Peers in a P2P Framework**

Finding peers in a Peer-to-Peer (P2P) network is a crucial step in establishing connections between 
nodes. Typically peers can be found starting from a bootstrap list of peers. This list typically contains a small number 
of well-connected and stable peers in the network. Once connected to a seed peer, you discover other peers in the network by querying the seed peer for 
information about nearby peers. This can be done using a protocol such as:

- DHT (Distributed Hash Table) queries
- Peer-to-peer gossip protocols
- Social networking-style updates

Then, you store the discovered peers locally and update the local peer list periodically to reflect changes in the 
network.

For simplicity, you run all nodes on the same computer so you use `port number` as `node/peer id`, and the node ids range from `5000 to 5009`. 

In real-world P2P networks:
- The number of nodes are not limited
- The `id` of a node is NOT bound to its port number. IP addresses and GUIDs (Globally Unique Identifications) may be used.

🎏 Complete Task 2 on the basic P2P program `p2p1.py` you completed in Task 1.
  - 🎏 Discover active peers, i.e. implement command `scan`.
  - 🎏 List connected peers, i.e. implement command `lp`.
  - 🎏 Connect to selected peers, update the list of connected peers, i.e. implement command `connect <peer_id>`.
  - 🎏 Disconnect from selected peers, update the list of connected peers as well, i.e. implement command `disconnect <peer_id>`.
  - 🖥️ Explain your code in the report and illustrate with output screenshots

#### Reference code:
```python
# 1. Function to find active peers
def scan_peers(self, peer_port):
    scan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scan_socket.settimeout(1) # avoid long waits
    print(f'Scanning peer {peer_port}...')
    try:
        scan_socket.connect((self.host, peer_port))
        print(f'Peer {peer_port} is active.')
        scan_socket.close()
        return (peer_port, True)
    except (socket.timeout, socket.error):
        print(f'Peer {peer_port} is inactive.')
        return (peer_port, False) 

# 2. List connected peers
print('List connected peers:')
with self.lock:
    if not self.request_sockets:
        print(f'Node {self.port} has no connected peers.')
    else:
        print(f'Node {self.port} has connected peers: ', end='')
        for p in self.request_sockets:
            print(f'{p} ', end='')
        print()

# 3. connect peer_id
print(f'Connect to peer {peer_id}:')
hint = ''
with self.lock:
    if peer_id in self.request_sockets:
        hint = f'Peer {peer_id} is already connected.'
    else:
        request_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            request_socket.connect((self.host, peer_id))
            hint = f'Peer {peer_id} connected.'
            self.request_sockets[peer_id] = request_socket
        except socket.error as e:
            # print(f'{e=}')                     
            hint = f'Peer {peer_id} is inactive.'
print(hint)

# 4. disconnect peer_id
print(f'Disconnect from peer {peer_id}:')
hint = ''
with self.lock:
    if peer_id not in self.request_sockets:
        hint = f'Peer {peer_id} is NOT connected.'
    else:
        self.request_sockets[peer_id].close()
        hint = f'Peer {peer_id} disconnected.'
        self.request_sockets.pop(peer_id)
print(hint)
```

- 🖥️ Sample output
  - Run at least 4 instances, i.e. nodes, to test your code.
  - ⚠️ System assigned ephemeral port numbers shown as peer ids below just for debug purpose
  ```
  # node 5000
  python3 p2p2.py 
    Enter your port (e.g., 5000, 5001, etc.): 5000
    >:Node listening on 127.0.0.1:5000


    help / ?: Show usage of all commands.
    scan: Discover active peers. For demonstration, limit the peer_id range from 5000 to 5009.
    lp: List connected peers.
    connect <peer_id>: Connect to a peer.
    disconnect <peer_id>: Disconnect from a peer.
    sf <filename>: Search for a file on all connected peers.
    request <filename> <peer_id>: Request a file from a peer.
    quit: Quit the program.

    >:scan
    Discover active peers:
    Scanning peer 5001...
    Peer 5001 is inactive.
    Scanning peer 5002...
    Peer 5002 is inactive.
    Scanning peer 5003...
    Peer 5003 is active.
    Scanning peer 5004...
    Peer 5004 is inactive.
    Scanning peer 5005...
    Peer 5005 is active.
    Scanning peer 5006...
    Peer 5006 is inactive.
    Scanning peer 5007...
    Peer 5007 is inactive.
    Scanning peer 5008...
    Peer 5008 is inactive.
    Scanning peer 5009...
    Peer 5009 is active.
    >:lp
    List connected peers:
    Node 5000 has no connected peers.
    >:Connection established with peer 37402
    connect 5003
    Connect to peer 5003:
    Peer 5003 connected.
    >:ls
    Unknown command.
    >:lp
    List connected peers:
    Node 5000 has connected peers: 5003 
    >:connect 5005
    Connect to peer 5005:
    Peer 5005 connected.
    >:lp
    List connected peers:
    Node 5000 has connected peers: 5003 5005 
    >:connect 5009
    Connect to peer 5009:
    Peer 5009 connected.
    >:lp
    List connected peers:
    Node 5000 has connected peers: 5003 5005 5009 
    >:disconnect 5003
    Disconnect from peer 5003:
    Peer 5003 disconnected.
    >:lp
    List connected peers:
    Node 5000 has connected peers: 5005 5009 
    >:quit
    All sockets closed. Exiting program.

  # node 5003
  python3 p2p2.py
    Enter your port (e.g., 5000, 5001, etc.): 5003
    >:Node listening on 127.0.0.1:5003
    Connection established with peer 38736
    Connection established with peer 46286
    Connection established with peer 51100
    lp
    List connected peers:
    Node 5003 has no connected peers.
    >:quit
    All sockets closed. Exiting program.

  # node 5005
  python3 p2p2.py
    Enter your port (e.g., 5000, 5001, etc.): 5005
    >:Node listening on 127.0.0.1:5005
    Connection established with peer 54210
    Connection established with peer 35266
    Connection established with peer 44274
    lp
    List connected peers:
    Node 5005 has no connected peers.
    >:quit
    All sockets closed. Exiting program.

  # node 5009
  python3 p2p2.py
    Enter your port (e.g., 5000, 5001, etc.): 5009
    >:Node listening on 127.0.0.1:5009
    Connection established with peer 57946
    lp
    List connected peers:
    Node 5009 has no connected peers.
    >:scan
    Discover active peers:
    Scanning peer 5000...
    Peer 5000 is active.
    Scanning peer 5001...
    Peer 5001 is inactive.
    Scanning peer 5002...
    Peer 5002 is inactive.
    Scanning peer 5003...
    Peer 5003 is active.
    Scanning peer 5004...
    Peer 5004 is inactive.
    Scanning peer 5005...
    Peer 5005 is active.
    Scanning peer 5006...
    Peer 5006 is inactive.
    Scanning peer 5007...
    Peer 5007 is inactive.
    Scanning peer 5008...
    Peer 5008 is inactive.
    >:Connection established with peer 57384
    lp
    List connected peers:
    Node 5009 has no connected peers.
    >:quit
    All sockets closed. Exiting program.
  ```

### Task 3: **Search for Shared Files**

In this task, you will 
- 🎏 implement functionality to search for specified shared files on the connected peers.
- 🎏 handle `search requests` from peers.

Since each peer maintains a list of known peers (IP and port), port (peer id) only in this simplified lab, to connect to, you can implement a mechanism to ask for a shared file from its connected peers only for simplicity.

#### Reference Code:

```python
# Function to handle file searches and requests from connected peers
# - SRCH filename
# - REQ filename
def handle_peer(self, response_socket, peer_id):
    while not self.evExit.is_set():
        msg = response_socket.recv(1024)
        if not msg:
            print(f'Peer {peer_id} closed connection.')
            with self.lock:
                self.response_sockets.pop(peer_id)
            break
        print(f"Received message from {peer_id}: {msg}")
        cmds = msg.decode().strip().split()

        # 1. handle SRCH filename
        if (len(cmds) == 0) or (not cmds[0]):
            print('Empty message.')
        elif (cmds[0] == 'SRCH') and cmds[1]:
            filename = cmds[1]
            file_path = os.path.join(self.shared_dir, filename)
            if os.path.exists(file_path):
                hint = f'150 {filename} found.'   
            else:
                hint = f'450 {filename} not found.'
            print(f"Response to peer {peer_id}:  {hint}")
            response_socket.sendall(hint.encode())             

        # 2. handle REQ file name
        elif (cmds[0] == 'REQ') and cmds[1]:
          pass
        else:
            print('Unknown message.')
            pass

# Function to search for a file from another peer
def search_file(self, filename):
    # you search among the connected peers only
    msg = f'SRCH {filename}'
    lostconnections = []
    for pid, psock in self.request_sockets.items():
        psock.sendall(msg.encode())

        # Receive response
        data = psock.recv(1024)
        if not data:
            print(f'Peer {pid} disconnected.')
            lostconnections.append[pid]
            break
        response = data.decode().strip()
        print(f"{response[4:-1]} on {pid}")
    
    # remove peers disconnected
    with self.lock:
        for p in lostconnections:
            self.request_sockets.pop(p)
```

- 🖥️ Sample output:
  - Run at least 4 nodes, put an image file in the shared folders in two of them
  ```
  # node 5000 connects to other 3 nodes and looks a file
  python3 p2p3.py 
    Enter your port (e.g., 5000, 5001, etc.): 5000
    >:Node listening on 127.0.0.1:5000
    connect 5003
    Connect to peer 5003:
    Peer 5003 connected.
    >:connect 5005
    Connect to peer 5005:
    Peer 5005 connected.
    >:connect 5009
    Connect to peer 5009:
    Peer 5009 connected.
    >:lp
    List connected peers:
    Node 5000 has connected peers: 5003 5005 5009 
    >:sf SkyShip.jpg
    Search for SkyShip.jpg on all connected peers:
    SkyShip.jpg found on 5003
    SkyShip.jpg not found on 5005
    SkyShip.jpg found on 5009
    >:quit
    All sockets closed. Exiting program.

  # node 5003
  python3 p2p3.py 
    Enter your port (e.g., 5000, 5001, etc.): 5003
    >:Node listening on 127.0.0.1:5003
    Connection established with peer 40730
    Received message from 40730: b'SRCH SkyShip.jpg'
    Response to peer 40730:  150 SkyShip.jpg found.
    Peer 40730 closed connection.
    quit
    All sockets closed. Exiting program.

  # node 5005
  python3 p2p3.py 
    Enter your port (e.g., 5000, 5001, etc.): 5005
    >:Node listening on 127.0.0.1:5005
    Connection established with peer 48486
    Received message from 48486: b'SRCH SkyShip.jpg'
    Response to peer 48486:  450 SkyShip.jpg not found.
    Peer 48486 closed connection.
    quit
    All sockets closed. Exiting program.

  # node 5009
  python3 p2p3.py 
    Enter your port (e.g., 5000, 5001, etc.): 5009
    >:Node listening on 127.0.0.1:5009
    Connection established with peer 39962
    Received message from 39962: b'SRCH SkyShip.jpg'
    Response to peer 39962:  150 SkyShip.jpg found.
    Peer 39962 closed connection.
    quit
    All sockets closed. Exiting program.
  ```

### Task 4: **Download Files from Peers**

In this task, you will implement the file download functionality, where one peer can request a file from another peer and download it.

- 🎏 **File Request**:  
   Implement a function that requests a specific file from a peer.

- 🎏 **Send File**:  
   When a peer requests a file, the other peer should send the file over the connection.

- 🎏 **Receive and Save the File**:  
   The requesting peer should receive the file data and save it in its shared directory.

#### Reference Code:

```python
# Handle REQ file name in `handle_peer`
file_path = os.path.join(self.shared_dir, filename)
if os.path.exists(file_path):
    # let's use TCP stream framing `Length-prefix` here
    # since you don't close the connection after each request
    hint = f'250 {filename} found.'
    lhint = f'{hint:40}' # 40 bytes for the response
    data = b''
    with open(file_path, 'rb') as f:
        data = f.read()
    data_length = len(data)
    msg = lhint.encode() + struct.pack('!I', data_length) + data               
    print(f"Response to peer {peer_id}:  {hint} Length in bytes: {data_length}")
    response_socket.sendall(msg)
else:
    hint = f'550 {filename} not found.'
    lhint = f'{hint:40}' # 40 bytes for the response
    print(f"Response to peer {peer_id}:  {hint}")
    response_socket.sendall(lhint.encode())


# Function to request a file from another peer
def request_file(self, peer_id, filename):
    msg = f'REQ {filename}'
    # requests a specific file from a peer.
    self.request_sockets[peer_id].sendall(msg.encode())
    
    # Receive response
    # Receive and Save the File
    response = self.recvall(peer_id, 40)
    if response[:3] == b'250':
        prefix = self.recvall(peer_id, 4)
        data_length = struct.unpack('!I', prefix)[0]
        data = self.recvall(peer_id, data_length)

        file_path = os.path.join(self.shared_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(data)        
        print(f"{response[4:-1].decode().strip()[:-1]} on {peer_id}. {data_length} bytes received.")
    else:
        print(f"{response[4:-1].decode().strip()[:-1]} on {peer_id}.")
# receive a block of message with specified length
def recvall(self, peer_id, length):
    blocks = []
    while length:
        block = self.request_sockets[peer_id].recv(length)
        if not block:
            print(f'Peer {peer_id} disconnected.')
            # remove peers disconnected
            with self.lock:
                self.request_sockets.pop(peer_id)

            raise EOFError('socket closed with {} bytes left'
                        ' in this block'.format(length))
        length -= len(block)
        blocks.append(block)
    return b''.join(blocks)
```

- 🖥️ Sample output:
  - Run at least 2 nodes, put an image file in the shared folders in one of them
  ```
  # node 5000 as the file requester
  python3 p2p4.py 
    Enter your port (e.g., 5000, 5001, etc.): 5000
    >:Node listening on 127.0.0.1:5000
    connect 5003
    Connect to peer 5003:
    Peer 5003 connected.
    >:sf SkyShip.jpg
    Search for SkyShip.jpg on all connected peers:
    SkyShip.jpg found on 5003
    >:sf SkyPalace.jpg
    Search for SkyPalace.jpg on all connected peers:
    SkyPalace.jpg not found on 5003
    >:request SkyPalace.jpg 5003
    Request file SkyPalace.jpg from peer 5003:
    SkyPalace.jpg not found on 5003.
    >:request SkyShip.jpg 5003
    Request file SkyShip.jpg from peer 5003:
    SkyShip.jpg found on 5003. 85021 bytes received.
    >:quit
    All sockets closed. Exiting program.

  # node 5003 as the file provider  
  python3 p2p4.py 
    Enter your port (e.g., 5000, 5001, etc.): 5003
    >:Node listening on 127.0.0.1:5003
    Connection established with peer 33228
    Received message from 33228: sendalSRCH SkyShip.jpg.
    Response to peer 33228:  150 SkyShip.jpg found.
    Received message from 33228: sendalSRCH SkyPalace.jpg.
    Response to peer 33228:  450 SkyPalace.jpg not found.
    Received message from 33228: sendalREQ SkyPalace.jpg.
    Response to peer 33228:  550 SkyPalace.jpg not found.
    Received message from 33228: sendalREQ SkyShip.jpg.
    Response to peer 33228:  250 SkyShip.jpg found. Length in bytes: 85021
    quit
    All sockets closed. Exiting program.
  ```

---

### Lab Conclusion:
In this lab, you learned how to create a simple P2P file-sharing system in Python. You implemented console-based interaction, peer discovery, file requests, and graceful shutdown of peers. This lab provides a foundation for more advanced P2P concepts, such as peer discovery protocols and distributed file systems.

---

### Optional Improvements
- Connection pooling and caching
- Peer reputation systems
- Network topology management
- Authenticate and Authorize
  * Username/password authentication
  * Digital certificates or public key infrastructure (PKI)
  * Token-based authentication
- Discover Other Peers
  * DHT (Distributed Hash Table) queries
  * Peer-to-peer gossip protocols
  * Social networking-style updates
- Store and Update Local Peer List
  - Store the discovered peers locally and update the local peer list periodically to reflect changes in the network.
- Handle various exceptions
- Search for files recursively like a web crawler?
