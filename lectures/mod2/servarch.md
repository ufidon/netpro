# Server Architectures
FPNP Ch 7


The aphorisms of the Zen of Python
---
- a poem about the inner consistent design of the Python language
- Run Python and type import this to show it


A Simple Protocol
---
- the client asks one of three plain-text ASCII questions 
   -  then waits for the server to complete its answer
- The end of each question is delimited with the ASCII question mark character ?
- the end of each answer is delimited with a period .
- close the connection without any warning when it has no more questions
- Each of the three question-and-answer pairs is based on 
  - one of the aphorisms of the Zen of Python


A Single-Threaded Server
---
- The server can only handle a single connection at a time


🖊️ Practice
---
- Play with the [single-threaded server in tcp](./srv/zens.py)
  - and the [respective client in tcp](./srv/zenc.py)
  
```bash
# open two terminals, one runs the server
python3 zens.py
# the other runs the client
python3 zenc.py
```

🖊️ Practice
---
- Play with the [single-threaded server in udp](./srv/zus.py)
  - and the [respective client in udp](./srv/zuc.py)
  
```bash
# open two terminals, one runs the server
python3 zus.py
# the other runs the client
python3 zuc.py
```


Threaded and Multiprocess Servers
---
- serve multiple clients simultaneously
  - by exploiting OS builtin support for multiprocess and multithread
  - a master thread with an accept() loop that hands off the new client sockets to  waiting queue of workers (thread pool)
- advantage:
  - simple: launch several copies of the single-threaded server
  - suitable for in-house services without resource coordination between threads
- disadvantage:
  - the OS concurrency mechanisms scale is limited
  - OSes rarely scale well to thousands or more threads running concurrently


🖊️ Practice
---
- Play with [multithreaded tcp server](./srv/mzts.py)

```bash
# open two terminals, one runs the server
python3 mzts.py
# in the other terminal, run multiple clients simultaneously
for i in {1..3}; do (python3 zenc.py &); done && wait
```

🖊️ Practice
---
- Play with [multithread udp server](./srv/mzus.py)

```bash
# open two terminals, one runs the server
python3 mzus.py
# in the other terminal, run multiple clients simultaneously
for i in {1..5}; do (python3 zuc.py &); done && wait
```

## 👁️ Review: [Python Parallel Programming](./code/ppp.ipynb)


The [*SocketServer* Framework](https://docs.python.org/3/library/socketserver.html)
---
- builtin in Python's standard library
- provides a convenient and flexible way to create network servers
  - It abstracts many of the lower-level details involved in handling network connections, 
  - making it easier to implement TCP, UDP, and Unix domain socket servers. 
- highly extensible, supporting the creation of custom request handlers 
  - and providing options for handling multiple clients concurrently through threading or forking.


### **Key Components of the `SocketServer` Framework**

1. **Base Classes for Servers:**
   - `TCPServer`: A base class for creating TCP servers.
   - `UDPServer`: A base class for creating UDP servers.
   - `UnixStreamServer`: A base class for creating Unix domain socket servers using stream sockets.
   - `UnixDatagramServer`: A base class for creating Unix domain socket servers using datagram sockets.

2. **Request Handler Classes:**
   - `BaseRequestHandler`: The base class for all request handlers. 
     - You subclass this to create your custom handler for processing incoming requests.
   - The `handle()` method is the key method in this class, 
     - where you define the logic to process the client's request.

3. **Mix-In Classes:**
   - `ThreadingMixIn`: A mix-in class that, when combined with a server class (e.g., `TCPServer`), 
     - allows the server to handle each client request in a separate thread.
   - `ForkingMixIn`: Similar to `ThreadingMixIn`, 
     - but uses forking (creating new processes) instead of threading to handle each client.

4. **Utility Methods:**
   - `serve_forever()`: 
     - is called on the server object to start the server 
     - and make it listen for incoming connections or datagrams indefinitely.
   - `shutdown()`: 
     - stops the server from handling any more requests and allows it to shut down gracefully.
   - `handle_request()`: 
     - processes a single request and then returns. 
     - useful for testing or when you want to control the server loop manually.

### **How `SocketServer` Works**

- **Server Lifecycle:**
  - A `SocketServer`-based server is initialized with a specific server address (host and port) and a request handler class.
  - When `serve_forever()` is called, the server enters an infinite loop, waiting for incoming connections (for TCP) or datagrams (for UDP).
  - When a client connects or sends data, the server instantiates the request handler class and calls its `handle()` method to process the request.

- **Request Handling:**
  - The `BaseRequestHandler` class is the core of request processing. 
    - It provides access to the client’s data and the server's socket.
  - In the `handle()` method, you define how the server should respond to incoming requests. 
    - This method is automatically invoked for each request.
  - The handler can access the request data through the `self.request` attribute. 
    - For TCP, this is a socket object; 
    - for UDP, it’s a tuple containing the data and the client address.

- **Concurrency with Mix-Ins:**
  - To handle multiple clients simultaneously, you can combine a server class with `ThreadingMixIn` or `ForkingMixIn`.
  - `ThreadingMixIn` creates a new thread for each client request, 
    - allowing the server to handle multiple clients concurrently within the same process.
  - `ForkingMixIn` forks a new process for each client request, 
    - providing process-level isolation but with a higher resource cost compared to threading.

### 🍎 **TCP Server with `SocketServer`**

```python
import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Receive and process data from the client
        self.data = self.request.recv(1024).strip()
        print(f"{self.client_address[0]} wrote: {self.data}")
        # Send back the same data to the client
        self.request.sendall(self.data)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
```

### **Limitations**

- **Performance:** The framework is suitable for small to medium-sized applications, 
  - but for high-performance or highly scalable servers, other frameworks (like `asyncio`, `Twisted`, or `gevent`) might be more appropriate.
- **Resource Management:** When using `ForkingMixIn`, managing system resources like memory and file descriptors becomes important, 
  - as forking creates new processes.


🖊️ Practice
---
- Play with [socketserver framework tcp](./srv/sszt.py)

```bash
# open two terminals, one runs the server
python3 sszt.py
# in the other terminal, run multiple clients simultaneously
for i in {1..3}; do (python3 zenc.py &); done && wait
```

🖊️ Practice
---
- Play with [socketserver framework udp](./srv/sszu.py)

```bash
# open two terminals, one runs the server
python3 sszu.py
# in the other terminal, run multiple clients simultaneously
for i in {1..5}; do (python3 zuc.py &); done && wait
```


### **Async Network Servers**

- designed to handle multiple client connections concurrently without the need for multiple threads or processes
  - by leveraging non-blocking I/O and event-driven programming, 
  - allowing a server to respond to whichever client is ready at a given moment without getting stuck waiting on any one client.

#### **Core Concept of Async Servers**

- **Hear from a List of Waiting Client Sockets:**
  - Async servers monitor multiple client sockets simultaneously.
  - The server responds as soon as any one of these clients is ready for interaction, without waiting for others.

- **Non-Blocking I/O:**
  - In non-blocking mode, a socket operation (like `send()` or `recv()`) always returns immediately, 
    - whether it succeeded, failed, or would have blocked.
  - This allows the server to continue processing other tasks or clients while waiting for a particular socket to be ready.

#### **Supporting Features of Modern OS Network Stacks**

- **System Calls for Waiting on Multiple Sockets:**
  - Modern operating systems provide system calls that allow a process to block and wait for multiple client sockets to become ready for I/O.
  - This is crucial for asynchronous servers, as it lets them efficiently manage multiple clients within a single thread.

- **Non-Blocking Mode:**
  - Sockets can be configured to operate in non-blocking mode, meaning any attempt to read from or write to a socket will return immediately.
  - If a `recv()` call would normally block because there is no data available, 
    - it simply returns an empty result or an error code indicating that the operation would block.

#### **Asynchronous Operation**

- **What Asynchronous Means:**
  - Asynchronous servers do not wait for any particular client to be ready.
  - Instead, they switch freely between all connected clients, serving whichever client is ready at the moment.
  - This approach avoids the overhead of managing multiple threads or processes 
    - and instead focuses on efficiently managing I/O events.

- **System Calls Supporting Asynchronous Mode:**
  - **`select()`** (POSIX): 
    - an older system call that allows a process to monitor multiple file descriptors, including sockets, 
      - to see if they are ready for reading, writing, or have an error condition. 
    - It’s generally considered inefficient for large numbers of sockets 
      - because it requires scanning through all file descriptors each time it is called.
  - **`poll()`**: 
    - Similar to `select()`, 
    - `poll()` allows monitoring multiple file descriptors but with improved performance and flexibility. 
    - It uses a more efficient data structure, making it more scalable than `select()`.
  - **`epoll()`** (Linux) and **`kqueue()`** (BSD): 
    - more modern and efficient mechanisms provided by Linux and BSD, respectively. 
    - They scale well with a large number of sockets and are more suitable for high-performance async servers.

#### **How Async Servers Work in Practice**

1. **Socket Setup:**
   - The server creates a listening socket and configures it for `non-blocking` I/O.
   - As new client connections are accepted, they are also set to `non-blocking mode`.

2. **Event Loop:**
   - The server enters an event loop where it continually checks which client sockets are ready for reading or writing.
   - This is typically done using one of the aforementioned system calls (`select()`, `poll()`, `epoll()`, etc.).

3. **Handling Clients:**
   - When a client socket is ready, the server performs the appropriate I/O operation (e.g., reading a request, sending a response).
   - Since the operations are non-blocking, the server can quickly move on to the next ready client.

4. **Efficient Use of Resources:**
   - Because the server doesn't block on any single operation, 
     - it can efficiently manage many client connections within a single thread or process, 
     - minimizing resource usage.

### **Advantages of Async Servers**

- **Scalability:** Async servers can handle a large number of connections efficiently without the overhead of creating and managing multiple threads or processes.
- **Resource Efficiency:** Non-blocking I/O and event-driven design reduce the need for CPU time and memory, 
  - especially in high-load scenarios.
- **Responsiveness:** By not waiting on any one client, async servers can respond more quickly to whichever clients are ready, 
  - improving overall responsiveness.

### **Considerations and Challenges**

- **Complexity:** Writing and debugging asynchronous code can be more complex compared to traditional synchronous code.
- **Limited Portability:** While the basic concepts are portable, specific system calls like `epoll()` or `kqueue()` are platform-specific, 
  - requiring care if your code needs to run on different operating systems.


🖊️ Practice
---
- Play with [Asynchronous server tcp - select](./srv/tas.py)

```bash
# open two terminals, one runs the server
python3 tas.py # or tap.py, or tae.py
# in the other terminal, run a client
# how?
```

🖊️ Practice
---
- Play with [Asynchronous server udp - select](./srv/uas.py)

```bash
# open two terminals, one runs the server
python3 uas.py # or uap.py, or uae.py
# in the other terminal, run a client
# how?
```


[Asyncio framework - Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)
---
- a powerful library introduced in Python 3.4 (with significant enhancements in later versions) 
- provides infrastructure for writing single-threaded concurrent code using coroutines, 
  - multiplexing I/O access over sockets and other resources, 
  - running network clients and servers, and other related primitives. 
- especially well-suited for I/O-bound and high-level structured network code.

#### **Overview of `asyncio`**

- **Asynchronous I/O:** 
  - `asyncio` enables writing code that performs non-blocking operations, 
  - allowing your program to handle multiple tasks seemingly at the same time without the overhead of threading or multiprocessing.
- **Event Loop:** 
  - At the heart of `asyncio` is the event loop, which manages and dispatches events and tasks. 
  - It monitors I/O events and schedules coroutines or callbacks to run when those events occur.
- **Coroutines and Tasks:** 
  - Coroutines are special functions defined with `async def` that can pause and resume their execution, 
    - allowing other coroutines to run in the meantime. 
  - Tasks are wrappers around coroutines that are scheduled to run on the event loop.

---

### **`asyncio` Programming Styles**

- `asyncio` supports two primary programming styles:
  1. **Callback Style**
  2. **Coroutine Style**
- Both styles leverage the event loop 
  - but differ in how asynchronous operations are handled and how the flow of control is managed.

#### **1. Callback Style**
- you define `functions (callbacks)` that the event loop will call 
  - when specific events occur (e.g., when data is received on a socket). 
- This style is reminiscent of traditional event-driven programming 
  - and is lower-level compared to coroutine style.
- Useful when dealing with legacy code or when a finer control over event handling is required.

**Characteristics:**

- **Event-Driven:** Relies on registering callbacks for specific events.
- **Less Readable:** Can lead to "callback hell" where callbacks are nested within callbacks, making the code harder to read and maintain.
- **Manual Control:** Requires explicit management of the event loop and callbacks.

#### **2. Coroutine Style**
- utilizes `async` and `await` syntax to define coroutines, 
  - which are special functions that can suspend and resume their execution. 
- This style allows writing asynchronous code that looks and behaves more like synchronous code, 
  - improving readability and maintainability.
- Preferred for new asynchronous code due to its readability and maintainability.

**Characteristics:**

- **Structured Concurrency:** Coroutines can await other coroutines, allowing for a clear and linear flow of control.
- **Easier to Read and Write:** The code structure is more straightforward, resembling synchronous code.
- **Higher-Level Abstractions:** Facilitates composing complex asynchronous operations without deeply nested callbacks.

---

🖊️ Practice
---
- TCP Echo Server Using [Callback Style](./srv/tacb.py)
- TCP Echo Server Using [Coroutine Style](./srv/tacr.py)
- TCP [Echo Client](./srv/tacbc.py)
- UDP Echo Server Using [Callback Style](./srv/uacb.py)
- UDP [Echo Client](./srv/uacbc.py)

---

### **Callback Style vs. Coroutine Style**

| Aspect                | Callback Style                                      | Coroutine Style                                      |
|-----------------------|-----------------------------------------------------|------------------------------------------------------|
| **Syntax**            | Relies on callback functions and event handlers     | Utilizes `async`/`await` keywords for coroutines    |
| **Readability**       | Can become nested and harder to read                 | More linear and readable, resembling synchronous code|
| **Control Flow**     | Event-driven, managed via callbacks                 | Structured, managed via coroutines                   |
| **Error Handling**   | Requires handling within callbacks                   | Can use `try-except` blocks within coroutines        |
| **Ease of Use**      | More complex for intricate workflows                 | Simpler for most asynchronous tasks                   |

---

### `asyncio.Protocol` vs. `asyncio.DatagramProtocol` 

| Feature/Aspect                | `asyncio.Protocol`                              | `asyncio.DatagramProtocol`                        |
|-------------------------------|-------------------------------------------------|----------------------------------------------------|
| **Purpose**                   | Stream-based, connection-oriented protocols (e.g., TCP). | Datagram-based, connectionless protocols (e.g., UDP). |
| **Connection Model**          | Connection-oriented (requires establishing a connection). | Connectionless (no connection setup required).    |
| **Main Methods**              | - `connection_made(transport)`<br>- `data_received(data)`<br>- `error_received(exception)`<br>- `connection_lost(exc)` | - `connection_made(transport)`<br>- `datagram_received(data, addr)`<br>- `error_received(exception)`<br>- `connection_lost(exc)` |
| **Data Handling**             | Handles continuous streams of data.            | Handles discrete datagrams (packets) of data.      |
| **Connection Management**     | Manages and maintains a persistent connection. | No connection management; each datagram is handled independently. |
| **Data Transmission**         | Use `transport.write(data)` to send data.       | Use `transport.sendto(data, addr)` to send data.   |
| **Data Reception**            | Use `data_received(data)` to handle incoming data. | Use `datagram_received(data, addr)` to handle incoming datagrams. |
| **Error Handling**            | Handled by `error_received(exception)`.         | Handled by `error_received(exception)`.            |
| **Connection Closure**        | Managed by `connection_lost(exc)`.               | Managed by `connection_lost(exc)`.                 |
| **Typical Use Cases**         | TCP-based protocols, where a continuous, reliable stream is needed. | UDP-based protocols, where packet-based, connectionless communication is used. |
| **Transport Type**            | Stream-oriented (`StreamReader` and `StreamWriter`). | Datagram-oriented (`Transport` with direct datagram handling). |


🖊️ Practice
---
- [TCP Echo Server by asyncio.Protocol](./srv/asynpro.py)
- [UDP Echo Server by asyncio.DatagramProtocol](./srv/asyndg.py)


Summary
---
-  Multithreading and multiprocessing run single-threaded code without modification
-  An asynchronous approach breaks up code into little pieces that can each run without ever blocking
   -  A callback style wraps each unblockable code snippet inside a method
   -  A coroutine style encloses each basic unblockable operation in between yield or yield from statements
- An asynchronous server 
  - can serve clients with far less expense without context switch
  - but is limited by the capability of the OS thread since it does all of its work within a single thread
    - overcomed by using asynchronous callback object or coroutine and launch it under an asynchronous framework
- Deployment of servers is another big topic



# References
- [asyncio — Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)
- [Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/)
- [Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html)
  - [How to Use Generators and yield in Python](https://realpython.com/introduction-to-python-generators/)
- [Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/)