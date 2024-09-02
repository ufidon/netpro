# Client/Server applications

Simple client/server programs
---
- simple TCP client/server programs
  - [TCP echo server](./tcp/tes.py)
  - [TCP echo client](./tcp/tec.py)
- simple UDP client/server programs
  - [UDP echo server](./udp/ues.py)
  - [UDP echo client](./udp/uec.py)

## Function `socket.socket(family=-1, type=-1, proto=-1, fileno=None)`
- used to create a new socket object
  - which is an endpoint for sending and receiving data across a network. 
- provides low-level networking interfaces.


### **`socket.socket()` signature**

```python
socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)
```

### **Formal Arguments**

| **Argument** | **Description**      | **Common Values**     |
|--------------|--------------|--------------|
| **`family`** | Specifies the address family of the socket. This determines the type of addresses that the socket can communicate with.                                   | `AF_INET`, `AF_INET6`, `AF_UNIX`             |
| **`type`**   | Specifies the socket type, which determines the communication semantics (e.g., stream or datagram).                                                       | `SOCK_STREAM`, `SOCK_DGRAM`, `SOCK_RAW`      |
| **`proto`**  | Specifies the protocol to be used with the socket. The default is `0`, which lets the operating system select the appropriate protocol based on the type. | Usually set to `0`, or protocol-specific value |
| **`fileno`** | Can be used to wrap an existing socket file descriptor (optional). When `None`, a new socket is created.                                                  | `None` (default)                             |


### **Explanation and Usage**

- **`family`:** Determines the type of addresses your socket can communicate with. 
  - For most internet-based applications, you will use `AF_INET` for IPv4 or `AF_INET6` for IPv6.
- **`type`:** Determines the communication style. 
  - For example, `SOCK_STREAM` is used for TCP (reliable, connection-oriented) communications, 
  - while `SOCK_DGRAM` is used for UDP (unreliable, connectionless) communications.
- **`proto`:** This is usually left as `0` to allow the OS to choose the correct protocol based on the type. 
  - However, for specific applications like raw sockets, you might specify a protocol directly.
- **`fileno`:** Used in advanced scenarios where you want to wrap an existing file descriptor in a socket object.

### 🍎 **Example Usage**

```python
import socket

# Creating a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding the socket to an address and port
sock.bind(('localhost', 8080))

# Listening for incoming connections
sock.listen(5)

# Accept a connection
connection, client_address = sock.accept()

# Receive and send data
data = connection.recv(1024)
connection.sendall(data)

# Close the connection
connection.close()

# Close the socket
sock.close()
```


## `with` statement
- with objects that support the `context management protocol`
  - which implements the __enter__ and __exit__ methods

```python
with expression as variable: # 1. `expression` returns a context manager object
    # 2. Clause `as variable` is optional. The object returned by the __enter__ method is assigned to the variable. 
    #   This variable can then be used within the block
    # 3. Code block (body of the with statement)
    #   The variable can be used here
    # 4. When the block is exited, the __exit__ method is automatically called, 
    #   even if the block is exited due to an exception.

```

| **With `with` Statement** | **Without `with` Statement** |
|---------------------------|-----------------------------|
| ```python                  | ```python                    |
| import socket              | import socket                |
|                            |                              |
| with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: | s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) |
|  | try:                        |
| s.connect(('localhost', 65432))  |     s.connect(('localhost', 65432)) |
| s.sendall(b'Hello, world') |     s.sendall(b'Hello, world') |
| data = s.recv(1024) |     data = s.recv(1024)        |
| print('Received', repr(data)) |     print('Received', repr(data)) |
|                            | finally:                    |
| # The socket is automatically closed  |     s.close()               |
| ```                        | ```                         |


### **Comparison**

- **Resource Management:**
  - **With `with`:** The socket is automatically closed when the block is exited, ensuring proper resource management without needing to explicitly call `close()`.
  - **Without `with`:** You have to manually close the socket using `s.close()` in a `finally` block to ensure it is closed even if an exception occurs.

- **Code Simplicity:**
  - **With `with`:** The code is cleaner and more concise since it abstracts away the cleanup process.
  - **Without `with`:** The code requires additional boilerplate (`try`/`finally` block) to ensure proper resource management, making it more verbose.

- **Error Handling:**
  - **With `with`:** The `with` statement automatically handles the cleanup of the socket, even if an exception occurs within the block.
  - **Without `with`:** The `finally` block ensures that the socket is closed, but you have to explicitly write this, making it prone to errors if forgotten.

In general, using `with` is recommended for managing resources like sockets, files, and locks in Python because it simplifies code and reduces the risk of resource leaks.


## Python socket functions and attributes

### **0. Socket Enumerate Constants**

| **Functionality**   | **Symbol Name**  | **Description**   | **Numeric Value** |
|------|------|----|------|
| **Address Families**    | `AF_INET`    | IPv4 Internet protocols (TCP/UDP).                                                                             | 2                 |
|                              | `AF_INET6`                         | IPv6 Internet protocols (TCP/UDP).                                                                                                                          | 10                |
|                              | `AF_UNIX`                          | Local communication (Unix domain sockets).                                                                                                                  | 1                 |
|                              | `AF_PACKET`                        | Low-level packet interface. (Linux-specific)                                                                                                                | 17                |
|                              | `AF_BLUETOOTH`                     | Bluetooth protocol stack.                                                                                                                                   | 31                |
| **Socket Types**              | `SOCK_STREAM`                      | Provides sequenced, reliable, two-way, connection-based byte streams (TCP).                                                                                 | 1                 |
|                              | `SOCK_DGRAM`                       | Supports datagrams (connectionless, unreliable messages) (UDP).                                                                                             | 2                 |
|                              | `SOCK_RAW`                         | Provides raw network protocol access.                                                                                                                       | 3                 |
|                              | `SOCK_SEQPACKET`                   | Provides sequenced, reliable, two-way connection-based transmission with a fixed maximum length of packet boundaries preserved.                             | 5                 |
|                              | `SOCK_RDM`                         | Provides a reliable datagram layer that does not guarantee ordering (Linux-specific).                                                                        | 4                 |
| **Protocol Numbers**          | `IPPROTO_TCP`                      | TCP protocol number.                                                                                                                                        | 6                 |
|                              | `IPPROTO_UDP`                      | UDP protocol number.                                                                                                                                        | 17                |
|                              | `IPPROTO_IP`                       | IP protocol number (used for raw sockets).                                                                                                                  | 0                 |
|                              | `IPPROTO_ICMP`                     | ICMP protocol number.                                                                                                                                       | 1                 |
| **Socket Options**            | `SO_REUSEADDR`                     | Allows the socket to bind to an address that is in a TIME_WAIT state.                                                                                        | 2                 |
|                              | `SO_KEEPALIVE`                     | Sends keepalive messages on the connection.                                                                                                                 | 9                 |
|                              | `SO_BROADCAST`                     | Allows transmission of broadcast messages.                                                                                                                  | 6                 |
|                              | `SO_LINGER`                        | Controls the action taken when unsent messages are queued on a socket and a `close()` is performed.                                                         | 13                |
|                              | `SO_SNDBUF`                        | Sets the size of the socket’s send buffer.                                                                                                                  | 7                 |
|                              | `SO_RCVBUF`                        | Sets the size of the socket’s receive buffer.                                                                                                               | 8                 |
| **Socket Levels**             | `SOL_SOCKET`                       | Socket options at the socket level.                                                                                                                         | 1                 |
|                              | `SOL_IP`                           | Socket options at the IP level.                                                                                                                             | 0                 |
|                              | `SOL_TCP`                          | Socket options at the TCP level.                                                                                                                            | 6                 |
| **Control Messages (Ancillary Data)** | `SCM_RIGHTS`                  | Transfer file descriptors between processes.                                                                                                                | 1                 |
|                              | `SCM_CREDENTIALS`                  | Transfer user credentials between processes (Linux-specific).                                                                                               | 2                 |
| **Socket Modes**              | `MSG_OOB`                          | Process out-of-band data.                                                                                                                                   | 1                 |
|                              | `MSG_PEEK`                         | Peek at the incoming message without removing it from the queue.                                                                                            | 2                 |
|                              | `MSG_WAITALL`                      | Wait for full request or error.                                                                                                                             | 256               |
|                              | `MSG_DONTROUTE`                    | Do not route; send the message directly to the interface.                                                                                                   | 4                 |
| **Address Information Flags** | `AI_PASSIVE`                       | The returned address is suitable for `bind()`.                                                                                                              | 1                 |
|                              | `AI_CANONNAME`                     | Return the canonical name of the host.                                                                                                                      | 2                 |
|                              | `AI_NUMERICHOST`                   | Return the numeric form of the host’s address.                                                                                                              | 4                 |



### **1. Create and Close Sockets**

| **Function**   | **Description**    | **Applicability (TCP/UDP)** |
|-----------|-----------|----------|
| **`socket.socket()`**             | Creates a new socket object. Takes parameters like address family (e.g., `AF_INET`), socket type (e.g., `SOCK_STREAM`). | TCP and UDP                  |
| **`socket.close()`**              | Closes the socket, freeing up the resources.                                                                     | TCP and UDP                  |
| **`socket.dup()`**                | Duplicates the socket. Returns a new socket object with a new file descriptor.                                    | TCP and UDP                  |
| **`socket.shutdown(how)`**        | Shuts down the socket’s receive (`SHUT_RD`), send (`SHUT_WR`), or both (`SHUT_RDWR`) operations.                 | TCP (not typically used in UDP) |

### **2. Create Servers**

| **Function**   | **Description**    | **Applicability (TCP/UDP)** |
|-----------|-----------|----------|
| **`socket.bind(address)`**        | Binds the socket to a specific address and port. Used for server sockets.                                         | TCP and UDP                  |
| **`socket.listen(backlog)`**      | Enables the server to accept connections. `backlog` specifies the maximum number of queued connections.           | TCP (not applicable to UDP)  |
| **`socket.accept()`**             | Accepts a connection from a client. Returns a new socket object and the address of the client.                     | TCP (not applicable to UDP)  |

### **3. Create Clients**

| **Function**   | **Description**    | **Applicability (TCP/UDP)** |
|-----------|-----------|----------|
| **`socket.connect(address)`**     | Connects the socket to a remote address (server). Used in client sockets.                                         | TCP and UDP (optional for UDP) |
| **`socket.connect_ex(address)`**  | Similar to `connect()`, but returns an error code instead of raising an exception on failure.                     | TCP and UDP (optional for UDP) |

### **4. Send Messages**

| **Function**   | **Description**    | **Applicability (TCP/UDP)** |
|-----------|-----------|----------|
| **`socket.send(bytes)`**          | Sends data to the connected socket. Used in TCP connections.                                                      | TCP                          |
| **`socket.sendall(bytes)`**       | Sends all data to the connected socket, ensuring that all bytes are transmitted.                                  | TCP                          |
| **`socket.sendto(bytes, address)`**| Sends data to a specific address. Used for UDP connections.                                                       | UDP                          |
| **`socket.sendmsg(buffers)`**     | Sends a message containing multiple buffers.                                                                     | TCP and UDP                  |

### **5. Receive Messages**

| **Function**   | **Description**    | **Applicability (TCP/UDP)** |
|-----------|-----------|----------|
| **`socket.recv(bufsize)`**        | Receives data from the socket. `bufsize` specifies the maximum amount of data to be received at once.             | TCP                          |
| **`socket.recvfrom(bufsize)`**    | Receives data from the socket, along with the address of the sender. Used for UDP sockets.                        | UDP                          |
| **`socket.recv_into(buffer)`**    | Receives data and stores it directly into a buffer rather than creating a new string.                             | TCP and UDP                  |

### **6. Set and Get Options**
| **Function**   | **Description**    | **Applicability (TCP/UDP)** |
|-----------|-----------|----------|
| **`socket.setblocking(flag)`**    | Sets the socket to blocking (`True`) or non-blocking (`False`) mode.                                             | TCP and UDP                  |
| **`socket.settimeout(timeout)`**  | Sets a timeout for blocking operations. A timeout of `None` means no timeout; a timeout of `0` is non-blocking.  | TCP and UDP                  |
| **`socket.gettimeout()`**         | Returns the timeout associated with socket operations.                                                           | TCP and UDP                  |
| **`socket.getsockopt(level, optname)`** | Returns the value of the given socket option.                                                              | TCP and UDP                  |
| **`socket.setsockopt(level, optname, value)`** | Sets the value of the given socket option.                                                            | TCP and UDP                  |

### **7. Set and Get Attributes**

| **Function/Attribute**   | **Description**    | **Applicability (TCP/UDP)** |
|-----------|-----------|----------|
| **`socket.getsockname()`**        | Returns the socket’s own address (typically used after `bind()`).                                                | TCP and UDP                  |
| **`socket.getpeername()`**        | Returns the address of the remote socket (used in connected sockets).                                            | TCP                          |
| **`socket.family`**               | Attribute that returns the address family of the socket (e.g., `AF_INET`).                                       | TCP and UDP                  |
| **`socket.type`**                 | Attribute that returns the socket type (e.g., `SOCK_STREAM`).                                                    | TCP and UDP                  |
| **`socket.proto`**                | Attribute that returns the protocol number used by the socket.                                                   | TCP and UDP                  |
| **`socket.fileno()`**             | Returns the socket’s file descriptor (an integer).                                                               | TCP and UDP                  |
| **`socket.makefile(mode)`**       | Returns a file-like object associated with the socket, which can be used for reading or writing.                 | TCP (rarely used with UDP)   |
| **`socket.get_inheritable()`**    | Returns `True` if the socket is inheritable by child processes, `False` otherwise.                               | TCP and UDP                  |
| **`socket.set_inheritable(flag)`**| Sets whether the socket is inheritable by child processes.                                                       | TCP and UDP                  |


## Blocking and Non-Blocking Modes

- **Blocking Mode**: Functions typically wait until the operation can be completed (e.g., until data is received, a connection is made, etc.).
- **Non-Blocking Mode**: Functions return immediately and may raise a `BlockingIOError` exception if the operation would block. This allows the program to continue running other tasks while waiting for the socket operation to complete.

| **Function/Attribute**       | **Blocking Mode Behavior**      | **Non-Blocking Mode Behavior**   |
|---------|----|-----|
| **`socket.socket()`**             | Creates a socket object in blocking mode by default.                                                            | Can be set to non-blocking mode using `setblocking(False)` or `settimeout(0)`.                                  |
| **`socket.bind(address)`**        | Binds the socket to a specific address and port. Operation is immediate.                                         | Same as blocking mode; binding is a non-blocking operation.                                                     |
| **`socket.listen(backlog)`**      | Sets up the socket to listen for incoming connections. Operation is immediate.                                   | Same as blocking mode; listening is a non-blocking operation.                                                   |
| **`socket.accept()`**             | Blocks until a new connection is accepted.                                                                      | Raises `BlockingIOError` if no connections are pending.                                                         |
| **`socket.connect(address)`**     | Blocks until the connection to the server is established.                                                       | Immediately returns and continues in the background; raises `BlockingIOError` if the connection isn't ready.    |
| **`socket.connect_ex(address)`**  | Similar to `connect()`, but returns an error code instead of raising an exception. Blocks until connected.       | Returns error codes like `EINPROGRESS` if the connection attempt is still in progress.                          |
| **`socket.send(bytes)`**          | Blocks until all the data is sent or the connection is closed.                                                   | Sends as much data as possible; raises `BlockingIOError` if it cannot send data immediately.                    |
| **`socket.sendall(bytes)`**       | Blocks until all the data is sent.                                                                               | Continues sending until all data is sent; may raise `BlockingIOError` if interrupted.                           |
| **`socket.sendto(bytes, address)`**| Blocks until the data is sent to the specified address.                                                          | Sends as much data as possible to the address; raises `BlockingIOError` if it cannot send immediately.          |
| **`socket.recv(bufsize)`**        | Blocks until at least one byte is received, up to `bufsize`.                                                     | Raises `BlockingIOError` if no data is available to read immediately.                                           |
| **`socket.recvfrom(bufsize)`**    | Blocks until data is received from a remote socket, up to `bufsize`.                                             | Raises `BlockingIOError` if no data is available to read immediately.                                           |
| **`socket.recv_into(buffer)`**    | Blocks until data is received and copied into the buffer.                                                        | Raises `BlockingIOError` if no data is available to read immediately.                                           |
| **`socket.sendmsg(buffers)`**     | Blocks until the message containing multiple buffers is sent.                                                    | Raises `BlockingIOError` if it cannot send immediately.                                                         |
| **`socket.close()`**              | Closes the socket immediately.                                                                                   | Same as blocking mode; closing is a non-blocking operation.                                                     |
| **`socket.shutdown(how)`**        | Shuts down the socket’s receive, send, or both operations. Operation is immediate.                               | Same as blocking mode; shutting down is a non-blocking operation.                                               |
| **`socket.setblocking(flag)`**    | Sets the socket to blocking mode if `True`.                                                                      | Sets the socket to non-blocking mode if `False`.                                                                |
| **`socket.settimeout(timeout)`**  | Sets a timeout for blocking operations. If the operation exceeds the timeout, an exception is raised.            | Timeout of `0` is equivalent to non-blocking mode.                                                              |
| **`socket.gettimeout()`**         | Returns the timeout value for blocking operations.                                                               | Returns `None` for blocking mode, `0` for non-blocking mode.                                                    |
| **`socket.getsockname()`**        | Returns the socket’s own address. Operation is immediate.                                                        | Same as blocking mode; non-blocking operation.                                                                  |
| **`socket.getpeername()`**        | Returns the address of the remote socket. Operation is immediate.                                                | Same as blocking mode; non-blocking operation.                                                                  |
| **`socket.getsockopt(level, optname)`** | Returns the value of the given socket option. Operation is immediate.                                          | Same as blocking mode; non-blocking operation.                                                                  |
| **`socket.setsockopt(level, optname, value)`** | Sets the value of the given socket option. Operation is immediate.                                             | Same as blocking mode; non-blocking operation.                                                                  |
| **`socket.fileno()`**             | Returns the socket’s file descriptor. Operation is immediate.                                                    | Same as blocking mode; non-blocking operation.                                                                  |
| **`socket.dup()`**                | Duplicates the socket. Operation is immediate.                                                                   | Same as blocking mode; non-blocking operation.                                                                  |
| **`socket.makefile(mode)`**       | Returns a file-like object associated with the socket. The operation depends on the mode specified.              | Non-blocking mode affects read/write operations; may raise `BlockingIOError` if data isn't immediately available. |
| **`socket.get_inheritable()`**    | Returns `True` if the socket is inheritable by child processes. Operation is immediate.                          | Same as blocking mode; non-blocking operation.                                                                  |
| **`socket.set_inheritable(flag)`**| Sets whether the socket is inheritable by child processes. Operation is immediate.                               | Same as blocking mode; non-blocking operation.                                                                  |



Socket names and DNS (**optional**)
---
- [dns.ipynb](./dns/dns.ipynb)


⭐ Network data and network errors
---
- [datanerr.ipynb](./datanerr/datanerr.ipynb)


## **Common Python Socket Errors**

| **Error**      | **Cause**       | **Potential Solution**    |
|-------|---------|-------------|
| `socket.timeout`              | Operation exceeds the set time limit.                        | Adjust timeout settings or handle with a retry mechanism. |
| `socket.gaierror`             | Failure in address-related operations (e.g., DNS resolution).| Check the domain name and network configuration.          |
| `socket.error`  | General error, such as connection refused.                   | Ensure the server is running and accessible.              |
| `socket.herror`               | Host-related errors, often due to an unknown host.           | Verify the host address and network connection.           |

---

## Common `errno` values for `socket.error` in Python

| **Error Number (`errno`)** | **Error Name**   | **Numerical Value** | **Description**       |
|----------|-------|--------|---------|
| `errno.EACCES`             | Permission Denied       | 13                  | The operation requires higher privileges (e.g., binding to a port < 1024).      |
| `errno.EADDRINUSE`         | Address Already in Use  | 98                  | The specified address is already in use by another socket.                      |
| `errno.EADDRNOTAVAIL`      | Address Not Available   | 99                  | The specified address is not available on the local machine.                    |
| `errno.ECONNABORTED`       | Connection Aborted      | 103                 | The connection was aborted by the operating system.                             |
| `errno.ECONNREFUSED`       | Connection Refused      | 111                 | The target machine actively refused the connection (no service on the port).    |
| `errno.ECONNRESET`         | Connection Reset        | 104                 | The connection was reset by the peer (often due to network issues).             |
| `errno.EHOSTUNREACH`       | Host Unreachable        | 113                 | The target host is unreachable, possibly due to network or routing issues.      |
| `errno.ENETDOWN`           | Network Down            | 100                 | The local network interface is down.                                            |
| `errno.ENETUNREACH`        | Network Unreachable     | 101                 | The network is unreachable, possibly due to routing issues.                     |
| `errno.ENOTCONN`           | Socket Not Connected    | 107                 | An operation was attempted on a socket that is not connected.                   |
| `errno.ETIMEDOUT`          | Connection Timed Out    | 110                 | The connection attempt timed out.                                               |
| `errno.EPIPE`              | Broken Pipe             | 32                  | The connection was broken by the remote peer, typically while writing data.     |

---

## **Socket Errors Common to Client and Server**

```python
import socket

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(('example.com', 80))  # Or s.bind(('localhost', 8080)) for server
    # Simulate sending/receiving data...
except socket.timeout:
    print("The connection timed out!")
except socket.gaierror as e:
    print(f"Address-related error occurred: {e}")
except socket.error as e:
    if e.errno == socket.errno.ECONNRESET:
        print("Connection reset by the peer.")
    else:
        print(f"Socket error occurred: {e}")
finally:
    s.close()
```

---

## **Server-Specific Socket Errors**

```python
import socket

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)
    print("Server is listening...")
except socket.error as e:
    if e.errno == socket.errno.EADDRINUSE:
        print("Port is already in use. Please choose another port.")
    else:
        print(f"Socket error occurred: {e}")
finally:
    server_socket.close()
```

---

## **Client-Specific Socket Errors**

```python
import socket

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('invalid-domain', 80))
    # Simulate sending/receiving data...
except socket.gaierror as e:
    print(f"Address-related error occurred: {e}")
except socket.herror as e:
    print(f"Host-related error occurred: {e}")
finally:
    client_socket.close()
```


🍎 Handle socket errors
---
- [code](./code/herr.py)


# Reference
- [socket — Low-level networking interface](https://docs.python.org/3/library/socket.html)