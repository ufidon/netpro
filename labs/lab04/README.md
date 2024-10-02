### Building a Multithreaded Chat System

This lab will guide you through the implementation of a chat system using Python's `socketserver` framework and `ThreadingMixIn` to support multithreading. We'll build both the server and client applications with TCP stream framing and a command-based messaging protocol, as specified.

**Requirements**:

- **Chat Server**:
  - Manages chat rooms and clients using threading.
  - Each chat room can handle multiple users, and messages are broadcasted to all chatters in the room.
  - Supports the server-side commands for managing chat rooms, users, and shutting down the server.
  
- **Chat Client**:
  - Connects to the server and can join, start, list, and quit chat rooms using the commands defined in the protocol.
  - Messages are sent from the client to the server, which handles routing the messages based on the current chat room.
  - A client can only join one chat room at a time. It must quit the current chat room to join a new one.

- **Communication Protocol**:
  - The TCP stream is framed with the delimiter `\0`.
  - Client commands are prefixed with a backtick (`).
  - Normal chat messages do not require any prefix and are sent directly to the chat room the user is currently in.


**All commands for both the client and the server in the chat system:**

- **Client Commands**
  - The client commands are focused on room management and interaction. 
  - They allow users to control their experience in the chat system by joining, leaving, and managing chat rooms.
  - They are sent from the clients to the server for parsing and execution except `` `help`` and `` `exit`` processed in the client.

| Command                            | Description                                                   |
|------------------------------------|---------------------------------------------------------------|
| `help`                             | Show usage of all commands.                                   |
| `start <chatroom_id> <chatroom_name>` | Start a new chat room with the given ID and name.         |
| `list`                             | List all active chat rooms with their IDs, names, and chatters. |
| `join <chatroom_id> <chatter_name>` | Join the specified chat room. Each message must be prefixed with the chatter's name. |
| `quit`                             | Quit the current chat room.                                  |
| `exit`                             | Exit the client program. The server withdraws the client from its joined chat room if it is closed. |


- **Server Commands**
  - The server commands provide administrative control over the chat system, enabling the management of chat rooms and users.
  - This includes starting rooms, kicking users, and ending rooms as needed.

| Command                                 | Description                                                   |
|-----------------------------------------|---------------------------------------------------------------|
| `help`                                  | Show usage of all commands.                                   |
| `list`                                  | List all chat rooms and the chatters in each.                |
| `end <chatroom_id>`                    | Withdraw all chatters from the specified chat room and then end the room. |
| `start <chatroom_id> <chatroom_name>`  | Start a new chat room with the given ID and name.           |
| `kick <chatter_name> <chatroom_id>`    | Kick the specified chatter out of the given chat room.      |
| `quit`                                  | Clean all chat rooms and end all chatter connections. Quit the server.        |


---

### Lab Structure

- **Task 1**: TCP Server-Client Framework
- **Task 2**: Adding Multithreading and Handling Multiple Clients
- **Task 3**: Implementing Chat Rooms and Message Broadcasting
- **Task 4**: Implementing Client Commands and Managing Chat Rooms
- **Task 5**: Server Command Set and Server Console

- 🎏 For each task
  - explain **your code** in the report
  - 💻 confirm with program output
- ⚠️ Reference codes are for **reference only**, supplied for just hint
  - They have various subtle problem even though some of them work

---

### Task 1: TCP Server-Client Framework

#### Objective:
Start by building a simple TCP server that can accept connections from clients and allow basic message exchange.

- 🎏 Implement TCP stream framing

#### Steps:

1. **Create the Server:**
   - Use Python’s `socketserver` module to create a basic TCP server that listens for incoming connections.
   - When a client connects, the server should receive and print messages sent by the client.

2. **Create the Client:**
   - Use Python’s `socket` module to create a client that connects to the server.
   - The client should send messages to the server and display the server’s response.

#### Code Template:

**Server:**

```python
import socketserver

class SimpleTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Connection from {self.client_address}")
        while True:
            data = self.request.recv(1024).decode()
            if not data:
                break
            print(f"Received: {data}")
            self.request.sendall(b"Message received\0")

if __name__ == "__main__":
    with socketserver.TCPServer(("localhost", 9999), SimpleTCPHandler) as server:
        server.serve_forever()
```

**Client:**

```python
import socket

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9999))

    while True:
        message = input("😄 :> ")
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode()
        print(f"Server says: {response}")

if __name__ == "__main__":
    client_program()
```

#### Test:
Run the server and client in separate terminals. Ensure the client can send messages to the server and receive responses.

- 💻 sample output:

```
# 1. server output: python3 s1.py 

ChatServer is listening at (localhost, 9999)
Connection from client ('127.0.0.1', 40016)
Client (127.0.0.1:40016) says: Hello
Client (127.0.0.1:40016) says: hi
Client (127.0.0.1:40016) says: Good morning!

# 2. client output: python3 c1.py 
😄 :> Hello
Server says: Message received
😄 :> hi
Server says: Message received
😄 :> Good morning!
Server says: Message received
😄 :> 
```
---

### Task 2: Adding Multithreading and Handling Multiple Clients

#### Objective:
- Enable the server to handle multiple clients concurrently by adding multithreading using `ThreadingMixIn`.
- Enable the client to handle server response in a separate thread and handle user input in the main thread

#### Steps:

1. **Modify the Server:**
   - Use `ThreadingMixIn` to handle each client connection in a separate thread. This allows the server to manage multiple clients simultaneously.

2. **Test Multiple Clients:**
   - Run the server and launch multiple client instances to verify that each client can send messages without blocking others.

#### Code Updates:
- 🎏 Update your code completed in Task 1 with the reference code below

**Server (with Multithreading):**

```python
import socketserver
import threading

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class SimpleTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Connection from {self.client_address}")
        while True:
            data = self.request.recv(1024).decode()
            if not data:
                break
            print(f"Received: {data}")
            self.request.sendall(b"Message received")

if __name__ == "__main__":
    with ThreadedTCPServer(("localhost", 9999), SimpleTCPHandler) as server:
        server.serve_forever()
```

**Client (withh Multithreading):**

```python
import socket
import threading

def listen_to_server(client_socket):
    while True:
        response = client_socket.recv(1024).decode()
        print(f"Server says: {response}")
        
def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9999))

    # Start the thread to listen to server messages
    threading.Thread(target=listen_to_server, args=(client_socket,)).start()

    try:
        while True:
            message = input("😄 :> ")
            # Send the message with a newline delimiter
            client_socket.sendall(message.encode())
    except:
        pass
    finally:
        client_socket.close()

if __name__ == "__main__":
    client_program()
```    

#### Test:
Run the server, then open two clients and ensure they can communicate independently with the server.

- 💻 sample output:

```
# 1. server output: python3 s2.py 
ChatServer is listening at (localhost, 9999)
Connection from client ('127.0.0.1', 60484)
Connection from client ('127.0.0.1', 44820)
Client (127.0.0.1:60484) says: hello
Client (127.0.0.1:44820) says: Good morning!
Client (127.0.0.1:60484) says: hei
Client (127.0.0.1:44820) says: Good noon?
Client (127.0.0.1:60484) says: Greetings!
Client (127.0.0.1:44820) says: Good night!

# 2.1 client output: python3 c2.py 
😄 :> hello
Server says: Message received
😄 :> hei
Server says: Message received
😄 :> Greetings!
Server says: Message received
😄 :> 

# 2.2 client output: python3 c2.py 
😄 :> Good morning!
Server says: Message received
😄 :> Good noon?
Server says: Message received
😄 :> Good night!
Server says: Message received
😄 :>
```
---

### Task 3: Implementing Chat Rooms and Message Broadcasting

#### Objective:
Create chat rooms where clients can join, send messages, and have their messages broadcast to all members in the room.

#### Steps:

1. **Define a ChatRoom Class:**
   - Create a `ChatRoom` class that maintains a list of connected clients and handles broadcasting messages to all clients in the room.

2. **Modify the Server:**
   - Add functionality for clients to join a room.
   - When a client sends a message, it should be broadcast to all other clients in the same room.

3. **Modify the Client:**
   - Command `` `help``  shows usage of all commands.
   - Command `` `exit `` exits the client program. The server withdraws the client from its joined chat room if it is closed.

#### Code Updates:
- 🎏 Update your code completed in Task 2 with the **reference** code below
- 🎏 The client side must finalized now
- 🎏 A lock is needed for shared data structures such as chat rooms updated by multiple threads at the server side

**ChatRoom Class:**

```python
class ChatRoom:
    def __init__(self, room_id, room_name='Food'):
        self.room_id = room_id
        self.room_name = room_name
        self.clients = []

    def add_client(self, client):
        self.clients.append(client)

    def remove_client(self, client):
        self.clients.remove(client)

    def broadcast(self, message):
        for client in self.clients:
            client.sendall(f"{message}\0".encode())
```

**Server Updates (Join Room and Broadcast):**
- [complete code](./is3.py)

```python
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
  allow_reuse_address = True


class ChatHandler(socketserver.BaseRequestHandler):
    rooms = {}

    def handle(self):
        self.room = None
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            data = data.decode().strip()
            if data.startswith('`join'):
                _, room_id, chatter_name = data.split()
                self.join_room(room_id, chatter_name)
            elif data.startswith('`exit'):
                self.request.close()
                break
            else:
                self.send_message(data)

    def join_room(self, room_id, chatter_name):
        if room_id not in self.rooms:
            self.rooms[room_id] = ChatRoom(room_id)
        self.room = self.rooms[room_id]
        self.room.add_client(self.request)
        self.room.broadcast(f"A new client {chatter_name} has joined chat_room {room_id}.")

    def send_message(self, message):
        if self.room:
            self.room.broadcast(message)
        else:
            self.request.sendall(b"Join a room first!\0")
```

**Client Updates**

```python
import socket
import threading
import time

def listen_to_server(client_socket):
    while True:
        response = client_socket.recv(1024).decode()
        if not response:
            break
        
        print(f"Server says: {response}")
        
def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9999))

    # Start the thread to listen to server messages
    tRec = threading.Thread(target=listen_to_server, args=(client_socket,))
    tRec.start()

    try:
        while True:
            message = input("😄 :> ")

            # Send the message with a newline delimiter
            if message.strip() == '`exit':
                print("quitting...")
                client_socket.sendall((message + '\0').encode())
                time.sleep(1)
                break
            elif message.strip() == '`help':
                print("Show the usages of all commands")
            else:
                client_socket.sendall((message + '\0').encode())

    except:
        pass
    finally:
        client_socket.close()

    tRec.join()
    
if __name__ == "__main__":
    client_program()
```

#### Test:
Run the server and multiple clients. Use the command `` `join <room_id> <chatter_name>`` to join rooms and test message broadcasting.

- 💻 sample output:

```
# 1. server output: python3 s3.py 
ChatServer is listening at (localhost, 9999)...
Received message from ('127.0.0.1', 47482): hello
Send to ('127.0.0.1', 47482): Join a room first!
Received message from ('127.0.0.1', 47482): `join 1 Alice
Send to ('127.0.0.1', 47482): A new client Alice has joined chat_room 1.
Received message from ('127.0.0.1', 47482): hi, I am Alice.
Send to ('127.0.0.1', 47482): hi, I am Alice.
Received message from ('127.0.0.1', 36106): `join 1 Bob
Send to ('127.0.0.1', 47482): A new client Bob has joined chat_room 1.
Send to ('127.0.0.1', 36106): A new client Bob has joined chat_room 1.
Received message from ('127.0.0.1', 36106): Hello, I'm Bob
Send to ('127.0.0.1', 47482): Hello, I'm Bob
Send to ('127.0.0.1', 36106): Hello, I'm Bob
Received message from ('127.0.0.1', 47482): Hi, Bob, I'm Alice. Nice to meet you!
Send to ('127.0.0.1', 47482): Hi, Bob, I'm Alice. Nice to meet you!
Send to ('127.0.0.1', 36106): Hi, Bob, I'm Alice. Nice to meet you!
Received message from ('127.0.0.1', 36106): Hi Alice, nice to meet you!
Send to ('127.0.0.1', 47482): Hi Alice, nice to meet you!
Send to ('127.0.0.1', 36106): Hi Alice, nice to meet you!


# 2.1 client output: python3 c3.py 
😄 :> hello
Server says: Join a room first!
`help

`help`: Show usage of all commands.
`start <chatroom_id> <chatroom_name>`: Start a new chat room with the given ID and name.
`list`: List all active chat rooms with their IDs, names, and chatters.
`join <chatroom_id> <chatter_name>`: Join the specified chat room. Each message must be prefixed with the chatter's name.
`quit`: Quit the current chat room.
`exit`: Exit the client program. The server withdraws the client from its joined chat room if it is closed.

😄 :> `join 1 Alice
😄 :> Server says: A new client Alice has joined chat_room 1.
hi, I am Alice.
😄 :> Server says: hi, I am Alice.
Server says: A new client Bob has joined chat_room 1.
Server says: Hello, I'm Bob
Hi, Bob, I'm Alice. Nice to meet you!
😄 :> Server says: Hi, Bob, I'm Alice. Nice to meet you!
Server says: Hi Alice, nice to meet you!

# 2.2 client output: python3 c3.py 
😄 :> `join 1 Bob
Server says: A new client Bob has joined chat_room 1.
😄 :> Hello, I'm Bob
😄 :> Server says: Hello, I'm Bob
Server says: Hi, Bob, I'm Alice. Nice to meet you!
Hi Alice, nice to meet you!
😄 :> Server says: Hi Alice, nice to meet you!
😄 :> `exit
quitting...
```

---

### Task 4: Implementing Client Commands and Managing Chat Rooms

#### Objective:
Add support for client commands such as listing, creating, joining, and quitting chat rooms. 

#### Steps:

1. **Extend Client Command Support:**
   - Implement remaining client commands like `start`, `list`, `join`, and `quit` on the server side.


#### Code Updates:
- 🎏 Update your code completed in Task 3 with the reference code below

**Server Command Handling:**

```python
class ChatHandler(socketserver.BaseRequestHandler):
    rooms = {}

    def handle(self):
        self.room = None
        self.username = None
        self.request.sendall(b"Welcome! Type `help for commands.\0")
        
        while True:
            data = self.request.recv(1024).decode().strip()
            if data.startswith('`'):
                self.handle_command(data)
            else:
                self.send_message(data)

    def handle_command(self, command):
        parts = command[1:].split()
        if parts[0] == "start":
            room_id, room_name = parts[1], parts[2]
            self.start_room(room_id, room_name)
        elif parts[0] == "join":
            room_id, username = parts[1], parts[2]
            self.join_room(room_id, username)
        elif parts[0] == "list":
            self.list_rooms()
        elif parts[0] == "quit":
            self.quit_room()
        elif parts[0] == "exit":
            self.quit_room()
            self.request.sendall(b"Goodbye!\0")
            return

    def start_room(self, room_id, room_name):
        if room_id not in self.rooms:
            self.rooms[room_id] = ChatRoom(room_id, room_name)
            self.request.sendall(f"Room {room_name} started.\0".encode())
        else:
            self.request.sendall(b"Room ID already exists.\0")

    def join_room(self, room_id, username):
        if room_id in self.rooms:
            self.room = self.rooms[room_id]
            self.room.add_client(self.request)
            self.username = username
            self.room.broadcast(f"{self.username} has joined {self.room.room_name}.")
            self.request.sendall(f"Joined room {self.room.room_name} as {self.username}\0".encode())
        else:
            self.request.sendall(b"Room ID not found.\0")

    def list_rooms(self):
        room_list = "\0".join([f"{room_id}: {room.room_name}" for room_id, room in self.rooms.items()])
        self.request.sendall(f"Active rooms:\0{room_list}\0".encode())

    def quit_room(self):
        if self.room:
            self.room.remove_client(self.request)
            self.room.broadcast(f"{self.username} has left the room.")
            self.room = None
```

- 💻 sample output:

```
# 1. server output: python3 s4.py 
ChatServer is listening at (localhost, 9999)...
Received message from ('127.0.0.1', 59110): `start 1 swimming
Send to ('127.0.0.1', 59110): Chatroom 1 started!
Received message from ('127.0.0.1', 59110): `join 1 Alice
Send to ('127.0.0.1', 59110): You join @chatroom 1
Received message from ('127.0.0.1', 59110): `list
Send to ('127.0.0.1', 59110): 
swimming@1: Alice@('127.0.0.1', 59110) 

Received message from ('127.0.0.1', 46454): `list
Send to ('127.0.0.1', 46454): 
swimming@1: Alice@('127.0.0.1', 59110) 

Received message from ('127.0.0.1', 46454): `join 1 Harris
Send to ('127.0.0.1', 59110): Harris: joined us @chatroom 1.
Send to ('127.0.0.1', 46454): You join @chatroom 1
Received message from ('127.0.0.1', 50092): `list
Send to ('127.0.0.1', 50092): 
swimming@1: Alice@('127.0.0.1', 59110) Harris@('127.0.0.1', 46454) 

Received message from ('127.0.0.1', 50092): `join 1 Trump
Send to ('127.0.0.1', 59110): Trump: joined us @chatroom 1.
Send to ('127.0.0.1', 46454): Trump: joined us @chatroom 1.
Send to ('127.0.0.1', 50092): You join @chatroom 1
Received message from ('127.0.0.1', 50092): `list
Send to ('127.0.0.1', 50092): 
swimming@1: Alice@('127.0.0.1', 59110) Harris@('127.0.0.1', 46454) Trump@('127.0.0.1', 50092) 

Received message from ('127.0.0.1', 50092): `quit
Send to ('127.0.0.1', 59110): Server: Trump quitted.
Send to ('127.0.0.1', 46454): Server: Trump quitted.
Send to ('127.0.0.1', 50092): You quitted from chatroom swimming@1
Received message from ('127.0.0.1', 50092): 
Send to ('127.0.0.1', 50092): Join a room first!
Received message from ('127.0.0.1', 59110): Hello, I am Alice
Send to ('127.0.0.1', 46454): Alice: Hello, I am Alice
Received message from ('127.0.0.1', 50092): `start 2 Food
Send to ('127.0.0.1', 50092): Chatroom 2 started!
Received message from ('127.0.0.1', 50092): `list
Send to ('127.0.0.1', 50092): 
swimming@1: Alice@('127.0.0.1', 59110) Harris@('127.0.0.1', 46454) 
Food@2: no chatters!

Received message from ('127.0.0.1', 50092): `join 3 Trump
Send to ('127.0.0.1', 50092): Chatroom 3 NOT exist!
Received message from ('127.0.0.1', 50092): `join 2 Trump
Send to ('127.0.0.1', 50092): You join @chatroom 2
Received message from ('127.0.0.1', 50092): `join 1 Trump
Send to ('127.0.0.1', 50092): You must quit your current chatroom 2 first.
Received message from ('127.0.0.1', 50092): `quit
Send to ('127.0.0.1', 50092): You quitted from chatroom Food@2
Received message from ('127.0.0.1', 50092): `join 1 Trump
Send to ('127.0.0.1', 59110): Trump: joined us @chatroom 1.
Send to ('127.0.0.1', 46454): Trump: joined us @chatroom 1.
Send to ('127.0.0.1', 50092): You join @chatroom 1
Received message from ('127.0.0.1', 46454): `list
Send to ('127.0.0.1', 46454): 
swimming@1: Alice@('127.0.0.1', 59110) Harris@('127.0.0.1', 46454) Trump@('127.0.0.1', 50092) 
Food@2: no chatters!

Received message from ('127.0.0.1', 46454): Hello Trump, let's have a debate!
Send to ('127.0.0.1', 59110): Harris: Hello Trump, let's have a debate!
Send to ('127.0.0.1', 50092): Harris: Hello Trump, let's have a debate!
Received message from ('127.0.0.1', 50092): `quit
Send to ('127.0.0.1', 59110): Server: Trump quitted.
Send to ('127.0.0.1', 46454): Server: Trump quitted.
Send to ('127.0.0.1', 50092): You quitted from chatroom swimming@1
Received message from ('127.0.0.1', 50092): `exit


# 2.1 client output: python3 c4.py  # Alice
😄 :> `start 1 swimming
Server: Chatroom 1 started!
😄 :> `join 1 Alice
😄 :> Server: You join @chatroom 1
`list
😄 :> Server: 
swimming@1: Alice@('127.0.0.1', 59110) 

Harris: joined us @chatroom 1.
Trump: joined us @chatroom 1.
Server: Trump quitted.
Hello, I am Alice
😄 :> Trump: joined us @chatroom 1.
Harris: Hello Trump, let's have a debate!
Server: Trump quitted.


# 2.2 client output: python3 c4.py  # Harris
😄 :> `list
Server: 
swimming@1: Alice@('127.0.0.1', 59110) 

😄 :> `join 1 Harris
😄 :> Server: You join @chatroom 1
Trump: joined us @chatroom 1.
Server: Trump quitted.
Alice: Hello, I am Alice
Trump: joined us @chatroom 1.
`list
😄 :> Server: 
swimming@1: Alice@('127.0.0.1', 59110) Harris@('127.0.0.1', 46454) Trump@('127.0.0.1', 50092) 
Food@2: no chatters!

Hello Trump, let's have a debate!
😄 :> Server: Trump quitted.


# 2.3 client output: python3 c4.py  # Trump
😄 :> `list
Server: 
swimming@1: Alice@('127.0.0.1', 59110) Harris@('127.0.0.1', 46454) 

😄 :> `join 1 Trump
😄 :> Server: You join @chatroom 1
`list
😄 :> Server: 
swimming@1: Alice@('127.0.0.1', 59110) Harris@('127.0.0.1', 46454) Trump@('127.0.0.1', 50092) 

`quit
😄 :> Server: You quitted from chatroom swimming@1

😄 :> Server: Join a room first!
`help

`help`: Show usage of all commands.
`start <chatroom_id> <chatroom_name>`: Start a new chat room with the given ID and name.
`list`: List all active chat rooms with their IDs, names, and chatters.
`join <chatroom_id> <chatter_name>`: Join the specified chat room. Each message must be prefixed with the chatter's name.
`quit`: Quit the current chat room.
`exit`: Exit the client program. The server withdraws the client from its joined chat room if it is closed.

😄 :> `start 2 Food
😄 :> Server: Chatroom 2 started!
`list
😄 :> Server: 
swimming@1: Alice@('127.0.0.1', 59110) Harris@('127.0.0.1', 46454) 
Food@2: no chatters!

`join 3 Trump
😄 :> Server: Chatroom 3 NOT exist!
`join 2 Trump
😄 :> Server: You join @chatroom 2
`join 1 Trump
😄 :> Server: You must quit your current chatroom 2 first.
`quit
😄 :> Server: You quitted from chatroom Food@2
`join 1 Trump
😄 :> Server: You join @chatroom 1
Harris: Hello Trump, let's have a debate!
`quit
😄 :> Server: You quitted from chatroom swimming@1
`exit
quitting...
```

---

### Task 5: Final Touches – Full Command Set and Server Console

#### Objective:
1. **Server-Side Room Management:**
   - Implement server commands in the server’s console to list rooms, kick users, or shut down rooms.
   - Implement all server commands, finalize the command set, and create a server console to manage rooms and users.

#### Steps:

1. **Finalize Server Command Handling:**
   - Ensure all server commands (`help`, `start`,  `list`, `end`, `kick`, `quit`) work as expected.

2. **Server Console for Room Management:**
   - Add a server-side console that allows the server administrator to manage chat rooms, kick users, and list all active rooms and users.

**Server Console:**

```python
def server_console(server):
    while True:
        command = input("Server Command: ").strip().

split()
        if command[0] == 'list':
            for room_id, room in server.rooms.items():
                print(f"Room {room_id}: {room.room_name} with {len(room.clients)} clients.")
        elif command[0] == 'end':
            room_id = command[1]
            if room_id in server.rooms:
                room = server.rooms[room_id]
                room.broadcast("Room is closing.")
                del server.rooms[room_id]
                print(f"Room {room_id} closed.")
        elif command[0] == 'kick':
            chatter_name, room_id = command[1], command[2]
            # Logic to kick the user by name from a room
```

- 💻 sample output: Refer to the final output below

---

### Testing and Submission

1. **Testing the Complete Chat System:**
   - Run the server and multiple clients. 
     - Test all client commands such as starting, joining, listing, and quitting rooms. 
     - Test all server console commands.
     - Test the interaction of the administrator and all client with all commands.

2. **Final Output:**
   - Ensure all commands and features work as expected.
   - 💻 sample output:

```
# 1. server output: python3 s5.py #
System: ChatServer is listening at (localhost, 9999)...
Chat administration:> System: new connection from ('127.0.0.1', 50768)
System: new connection from ('127.0.0.1', 50772)
System: new connection from ('127.0.0.1', 50788)
`help

`help`: Show usage of all commands.
`list`: List all chat rooms and the chatters in each.
`end <chatroom_id>`: Withdraw all chatters from the specified chat room and then end the room.
`start <chatroom_id> <chatroom_name>: Start a new chat room with the given ID and name.
`kick <chatter_name> <chatroom_id>`: Kick the specified chatter out of the given chat room.
`quit`:  Clean all chat rooms and end all chatter connections. Quit the server.

Chat administration:> `list
Administrator: No chatroom exists!
Chat administration:> `start 1 Swimming
Administrator: Chatroom 1 started!
Chat administration:> `start 1 Running
Administrator: Chatroom 1 exists!
Chat administration:> `list

Administrator: Swimming@1: no chatters!

Chat administration:> Received message from ('127.0.0.1', 50768): `join 1 Alice
Send to ('127.0.0.1', 50768): You join @chatroom 1
Received message from ('127.0.0.1', 50772): `join 1 Bob
Send to ('127.0.0.1', 50768): Bob: joined us @chatroom 1.
Send to ('127.0.0.1', 50772): You join @chatroom 1
Received message from ('127.0.0.1', 50788): `join 1 Cathy
Send to ('127.0.0.1', 50768): Cathy: joined us @chatroom 1.
Send to ('127.0.0.1', 50772): Cathy: joined us @chatroom 1.
Send to ('127.0.0.1', 50788): You join @chatroom 1
Received message from ('127.0.0.1', 50788): `list
Send to ('127.0.0.1', 50788): 
Swimming@1: Alice@('127.0.0.1', 50768) Bob@('127.0.0.1', 50772) Cathy@('127.0.0.1', 50788) 

`kick Bob 1
Send to ('127.0.0.1', 50772): You were kicked out from chatroom Swimming@1 by the Administrator!
Send to ('127.0.0.1', 50768): Administrator: Bob was kicked out.
Send to ('127.0.0.1', 50788): Administrator: Bob was kicked out.
Administrator: Bob was kicked from chatroom 1.
Chat administration:> Received message from ('127.0.0.1', 50768): `list
Send to ('127.0.0.1', 50768): 
Swimming@1: Alice@('127.0.0.1', 50768) Cathy@('127.0.0.1', 50788) 

Received message from ('127.0.0.1', 50772): `join 1 Bob
Send to ('127.0.0.1', 50768): Bob: joined us @chatroom 1.
Send to ('127.0.0.1', 50788): Bob: joined us @chatroom 1.
Send to ('127.0.0.1', 50772): You join @chatroom 1
Received message from ('127.0.0.1', 50772): `list
Send to ('127.0.0.1', 50772): 
Swimming@1: Alice@('127.0.0.1', 50768) Cathy@('127.0.0.1', 50788) Bob@('127.0.0.1', 50772) 

Received message from ('127.0.0.1', 50772): Hello, I'm Bob.
Send to ('127.0.0.1', 50768): Bob: Hello, I'm Bob.
Send to ('127.0.0.1', 50788): Bob: Hello, I'm Bob.
`end
Unknown commands.
Chat administration:> `end 1
Send to ('127.0.0.1', 50768): Administrator: chatroom is being closed by the Administrator.
Send to ('127.0.0.1', 50788): Administrator: chatroom is being closed by the Administrator.
Send to ('127.0.0.1', 50772): Administrator: chatroom is being closed by the Administrator.
Administrator: chatroom 1 closed.
Chat administration:> Received message from ('127.0.0.1', 50768): `list
Send to ('127.0.0.1', 50768): No room exists!
`quit
Administrator: notify clients about shutting down server...
System: please terminate the console
Administrator: Shutting down server console...
System: Shutting down server...


# 2.1 client output: python3 c3.py  # Alice
😄 :> `join 1 Alice
Server: You join @chatroom 1
😄 :> Bob: joined us @chatroom 1.
Cathy: joined us @chatroom 1.
Administrator: Bob was kicked out.
`list
😄 :> Server: 
Swimming@1: Alice@('127.0.0.1', 50768) Cathy@('127.0.0.1', 50788) 

Bob: joined us @chatroom 1.
Bob: Hello, I'm Bob.
Administrator: chatroom is being closed by the Administrator.
`list
😄 :> Server: No room exists!
Administrator: Chatserver is going to shutdown...
`exit
quitting...


# 2.2 client output: python3 c3.py  # Bob
😄 :> `join 1 Bob
Server: You join @chatroom 1
😄 :> Cathy: joined us @chatroom 1.
Server: You were kicked out from chatroom Swimming@1 by the Administrator!
`join 1 Bob
😄 :> Server: You join @chatroom 1
`list
😄 :> Server: 
Swimming@1: Alice@('127.0.0.1', 50768) Cathy@('127.0.0.1', 50788) Bob@('127.0.0.1', 50772) 

Hello, I'm Bob.
😄 :> Administrator: chatroom is being closed by the Administrator.
Administrator: Chatserver is going to shutdown...
`exit
quitting...


# 2.3 client output: python3 c3.py  # Cathy
😄 :> `join 1 Cathy
Server: You join @chatroom 1
😄 :> `list
😄 :> Server: 
Swimming@1: Alice@('127.0.0.1', 50768) Bob@('127.0.0.1', 50772) Cathy@('127.0.0.1', 50788) 

Administrator: Bob was kicked out.
Bob: joined us @chatroom 1.
Bob: Hello, I'm Bob.
Administrator: chatroom is being closed by the Administrator.
Administrator: Chatserver is going to shutdown...
`exit
quitting...

```

---

### Optional enhancements
- Think about exception handling for various cases
- A client can 
  - Start without connecting a server
  - Connect to a server `` `connect server_ip port``
  - Join several chat rooms at the same time
  - Switch chat rooms `` `switch chatroom_id``
  - Broadcast message to a chat room: `` `broadcast chtroom_id message``
  - Message to another chatter directly and secretly: `` `secret chatter_name message``
- A server can 
  - group chatters `` `group chatroom_id list_of_chatters``
- Add whatever functions with your imagination