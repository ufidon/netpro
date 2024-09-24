## Stream Framing in TCP Socket Programming

### Introduction

TCP (Transmission Control Protocol) is a reliable, connection-oriented protocol. Unlike UDP, which works with discrete packets, TCP treats data as a continuous stream of bytes. This means that if you send a message "Hello" followed by "World", the receiver may receive "HelloWorld" or "Hell" and "oWorld", depending on network conditions. This can lead to problems when parsing messages, as the boundaries between messages can become unclear.


**Stream Framing** is the method used to ensure that messages are properly delimited and interpreted as discrete entities. There are several techniques to frame TCP messages:

1. **Delimiter-Based Framing**: Each message ends with a special delimiter (e.g., `'\n'` or `'\0'`).
2. **Length-Prefix Framing**: Each message is prefixed with its length, so the receiver knows how many bytes to read for each message.

⚠️: **Required screenshots are noted with 💻**

### Lab Tasks

This lab consists of four tasks that will demonstrate the need for stream framing and three common framing techniques.

---

### Task 1: Problematic programs

- In this task, you'll run the simple chat server and client below to observe how messages are received with problems, i.e. the boundaries between messages are unclear.

#### 1.1 Server Code
```python
import socket

def chat_server(host='127.0.0.1', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server started at {host}:{port}, waiting for connections...")
        
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode('utf-8')}")
                conn.sendall(data)

if __name__ == "__main__":
    chat_server()
```

#### 1.2 Client code
```python
import socket

def chat_client(host='127.0.0.1', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        
        messages = ["Hello", "World", "How are you?"]
        for msg in messages:
            client_socket.sendall(msg.encode('utf-8'))
            
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode('utf-8')}")

if __name__ == "__main__":
    chat_client()
```

- 🎏 💻 server and client output
- 🎏 point out and analyze the problems 
- 🎏 💻 In the client, change the receive buffer `1024` to be `1, 10, 20, 100` separately and run the programs, i.e. run 4 times, one for each modification, describe and analyze the output. (Meanwhile, keep the server's receive buffer unchanged as 1024)
- 🎏 💻 Repeat the modification in the server, run the programs, describe and analyze the output. (Meanwhile, keep the client's receive buffer unchanged as 1024)

---

### Task 2: Chat Server/Client With Ping-pong Style

In this task, you'll create a simple chat server and client to observe how messages are received with ping-pong, i.e. framing stream in both directions alternatively.

#### 2.1 Server Code

The server will accept connections from clients and simply echo back any data it receives.

```python
import socket

def chat_server(host='127.0.0.1', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server started at {host}:{port}, waiting for connections...")
        
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                
                print(f"Received: {data.decode('utf-8')}")
                conn.sendall(data)

if __name__ == "__main__":
    chat_server()
```

#### 2.2 Client Code

The client will connect to the server and send multiple messages sequentially.

```python
import socket

def chat_client(host='127.0.0.1', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        
        messages = ["Hello", "World", "How are you?"]
        for msg in messages:
            client_socket.sendall(msg.encode('utf-8'))
            
            
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode('utf-8')}")

if __name__ == "__main__":
    chat_client()
```

#### Modification

- 🎏 Modify the server and then the client to generate the following sample output 💻
- 🎏 Explain the ping-pong framing with your code added

- server output
```
python3 s1.py 
Server started at 127.0.0.1:12345, waiting for connections...
Connected by Client (127.0.0.1:36504)
Server (127.0.0.1:12345) received from Client (127.0.0.1:36504): Beautiful is better than ugly
Server (127.0.0.1:12345) sent to Client (127.0.0.1:36504): BEAUTIFUL IS BETTER THAN UGLY
Server (127.0.0.1:12345) received from Client (127.0.0.1:36504): Explicit is better than implicit
Server (127.0.0.1:12345) sent to Client (127.0.0.1:36504): EXPLICIT IS BETTER THAN IMPLICIT
Server (127.0.0.1:12345) received from Client (127.0.0.1:36504): Simple is better than complex?
Server (127.0.0.1:12345) sent to Client (127.0.0.1:36504): SIMPLE IS BETTER THAN COMPLEX?
```
- client output
```
python3 c1.py 
Client (127.0.0.1:36504) sent to Server (127.0.0.1:12345): Beautiful is better than ugly
Client (127.0.0.1:36504) received from Server (127.0.0.1:12345): BEAUTIFUL IS BETTER THAN UGLY
Client (127.0.0.1:36504) sent to Server (127.0.0.1:12345): Explicit is better than implicit
Client (127.0.0.1:36504) received from Server (127.0.0.1:12345): EXPLICIT IS BETTER THAN IMPLICIT
Client (127.0.0.1:36504) sent to Server (127.0.0.1:12345): Simple is better than complex?
Client (127.0.0.1:36504) received from Server (127.0.0.1:12345): SIMPLE IS BETTER THAN COMPLEX?
```

---

### Task 3: Delimiter-Based Framing

In this task, you'll modify the server and client to use a delimiter (e.g., newline `\n`) to frame messages.

#### 3.1 Server Code with Delimiter Framing

```python
import socket

def chat_server_delimiter(host='127.0.0.1', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server started at {host}:{port}, waiting for connections...")
        
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            buffer = ""
            while True:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                buffer += data

            print(f"Received: {buffer}")
            conn.sendall((buffer + "\n").encode('utf-8'))

if __name__ == "__main__":
    chat_server_delimiter()
```

#### 3.2 Client Code with Delimiter Framing

```python
import socket

def chat_client_delimiter(host='127.0.0.1', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        
        messages = ["Hello\n", "World\n", "How are you?\n"]
        for msg in messages:
            client_socket.sendall(msg.encode('utf-8'))

        client_socket.shutdown(socket.SHUT_WR)
        
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received from server: {data.strip()}")

if __name__ == "__main__":
    chat_client_delimiter()
```

#### Modification

- 🎏 Modify the server and then the client to generate the following sample output 💻
- 🎏 Explain the delimiter-based framing with your code added
  - use `\n` as the delimiter

- server output
```
python3 s2.py 
Server started at 127.0.0.1:12345, waiting for connections...
Connected by Client (127.0.0.1:60336)
Server (127.0.0.1:12345) received from Client (127.0.0.1:60336): Beautiful is better than ugly
Server (127.0.0.1:12345) sent to Client (127.0.0.1:60336): BEAUTIFUL IS BETTER THAN UGLY
Server (127.0.0.1:12345) received from Client (127.0.0.1:60336): Explicit is better than implicit
Server (127.0.0.1:12345) sent to Client (127.0.0.1:60336): EXPLICIT IS BETTER THAN IMPLICIT
Server (127.0.0.1:12345) received from Client (127.0.0.1:60336): Simple is better than complex?
Server (127.0.0.1:12345) sent to Client (127.0.0.1:60336): SIMPLE IS BETTER THAN COMPLEX?
```

- client output
```
python3 c2.py 
Client (127.0.0.1:60336) sent to Server (127.0.0.1:12345): Beautiful is better than ugly
Client (127.0.0.1:60336) received from Server (127.0.0.1:12345): BEAUTIFUL IS BETTER THAN UGLY
Client (127.0.0.1:60336) sent to Server (127.0.0.1:12345): Explicit is better than implicit
Client (127.0.0.1:60336) received from Server (127.0.0.1:12345): EXPLICIT IS BETTER THAN IMPLICIT
Client (127.0.0.1:60336) sent to Server (127.0.0.1:12345): Simple is better than complex?
Client (127.0.0.1:60336) received from Server (127.0.0.1:12345): SIMPLE IS BETTER THAN COMPLEX?
```

---

### Task 4: Length-Prefix Framing

In this task, you'll modify the server and client to use a length-prefix framing method, where each message is prefixed with its length in bytes.

#### 4.1 Server Code with Length-Prefix Framing

```python
import socket
import struct

def chat_server_length_prefix(host='127.0.0.1', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server started at {host}:{port}, waiting for connections...")
        
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            buffer = b""
            message = ""
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                buffer += data
                while len(buffer) >= 4:
                    # Read message length
                    length = struct.unpack('!I', buffer[:4])[0]
                    if len(buffer) < 4 + length:
                        break
                    message += buffer[4:4 + length].decode('utf-8')
                    buffer = buffer[4 + length:]

            print(f"Received: {message}")
            response = message.encode('utf-8')
            conn.sendall(struct.pack('!I', len(response)) + response)

if __name__ == "__main__":
    chat_server_length_prefix()
```

#### 4.2 Client Code with Length-Prefix Framing

```python
import socket
import struct

def chat_client_length_prefix(host='127.0.0.1', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        
        messages = ["Hello", "World", "How are you?"]
        for msg in messages:
            # Pack message with length prefix
            encoded_msg = msg.encode('utf-8')
            length_prefix = struct.pack('!I', len(encoded_msg))
            client_socket.sendall(length_prefix + encoded_msg)

        client_socket.shutdown(socket.SHUT_WR)
        
        # Receive message back with length prefix
        length_prefix = client_socket.recv(4)
        length = struct.unpack('!I', length_prefix)[0]
        data = client_socket.recv(length)
        print(f"Received from server: {data.decode('utf-8')}")

if __name__ == "__main__":
    chat_client_length_prefix()
```

#### Modification

- 🎏 Modify the server and then the client to generate the following sample output 💻
- 🎏 Explain the length-prefixing framing with your code added

- Server output
```
python3 s3.py 
Server started at 127.0.0.1:12345, waiting for connections...
Connected by Client (127.0.0.1:41358)
Server (127.0.0.1:12345) received from Client (127.0.0.1:41358): Beautiful is better than ugly
Server (127.0.0.1:12345) sent to Client (127.0.0.1:41358): BEAUTIFUL IS BETTER THAN UGLY
Server (127.0.0.1:12345) received from Client (127.0.0.1:41358): Explicit is better than implicit
Server (127.0.0.1:12345) sent to Client (127.0.0.1:41358): EXPLICIT IS BETTER THAN IMPLICIT
Server (127.0.0.1:12345) received from Client (127.0.0.1:41358): Simple is better than complex?
Server (127.0.0.1:12345) sent to Client (127.0.0.1:41358): SIMPLE IS BETTER THAN COMPLEX?
```

- Client output
```
python3 c3.py 
Client (127.0.0.1:41358) sent to Server (127.0.0.1:12345): Beautiful is better than ugly
Client (127.0.0.1:41358) received from Server (127.0.0.1:12345): BEAUTIFUL IS BETTER THAN UGLY
Client (127.0.0.1:41358) sent to Server (127.0.0.1:12345): Explicit is better than implicit
Client (127.0.0.1:41358) received from Server (127.0.0.1:12345): EXPLICIT IS BETTER THAN IMPLICIT
Client (127.0.0.1:41358) sent to Server (127.0.0.1:12345): Simple is better than complex?
Client (127.0.0.1:41358) received from Server (127.0.0.1:12345): SIMPLE IS BETTER THAN COMPLEX?
```

---

### Summary

This lab demonstrated why stream framing is essential in TCP programming and showed three common techniques: ping-pong style, delimiter-based and length-prefix framing. Understanding and implementing these techniques ensures that your TCP-based applications can correctly parse and process messages.

- 🎏 compare the advantages and disadvantages of the 3 framing schemes you implemented