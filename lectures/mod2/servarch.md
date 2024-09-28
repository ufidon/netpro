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


## Message framing in asyncio
```bash
# 1. Length Prefixing
# server:
python3 ./srv/abs.py
# client:
python3 ./srv/abc.py

# 2. Delimiter-Based Framing
# server:
python3 ./srv/ads.py
# client:
python3 ./srv/adc.py

# 3. Fixed-Length Framing
# server:
python3 ./srv/afs.py
# client:
python3 ./srv/afc.py
```

##  **`asyncio` Module-Level Functions**

- Methods that are **coroutines** need to be awaited. 
  - These coroutines suspend execution of the calling function to allow other tasks to run concurrently. 
- Regular functions that return results immediately and do not need to be awaited.

| **Function**                        | **Signature**                                   | **Description**                                              | **Await Needed?** |
|-------------------------------------|-------------------------------------------------|--------------------------------------------------------------|-------------------|
| `asyncio.run()`                     | `asyncio.run(main, *, debug=False)`            | Runs the main coroutine, managing the event loop.           | No                |
| `asyncio.get_event_loop()`          | `asyncio.get_event_loop()`                     | Returns the current event loop or creates a new one.        | No                |
| `asyncio.set_event_loop()`          | `asyncio.set_event_loop(loop)`                 | Sets the event loop object to be used.                      | No                |
| `asyncio.new_event_loop()`          | `asyncio.new_event_loop()`                     | Creates a new event loop object.                            | No                |
| `asyncio.get_event_loop_policy()`   | `asyncio.get_event_loop_policy()`              | Returns the current event loop policy.                      | No                |
| `asyncio.set_event_loop_policy()`   | `asyncio.set_event_loop_policy(policy)`        | Sets the event loop policy.                                | No                |
| `asyncio.create_task()`             | `asyncio.create_task(coro, *, name=None)`      | Schedules the coroutine to be executed.                     | No                |
| `asyncio.sleep()`                  | `asyncio.sleep(delay, result=None)`            | Suspends execution of the coroutine for `delay` seconds.    | Yes               |
| `asyncio.wait()`                   | `asyncio.wait(fs, *, timeout=None, return_when=ALL_COMPLETED)` | Waits for the futures to be completed or timeout. | Yes               |
| `asyncio.wait_for()`               | `asyncio.wait_for(future, timeout)`            | Waits for the future to be completed or raises `TimeoutError`. | Yes            |
| `asyncio.shield()`                 | `asyncio.shield(aw, *, loop=None)`             | Protects the coroutine from being cancelled.               | Yes               |
| `asyncio.gather()`                 | `asyncio.gather(*tasks, return_exceptions=False)` | Runs multiple coroutines concurrently and waits for them. | Yes               |
| `asyncio.as_completed()`            | `asyncio.as_completed(pending, *, timeout=None)` | Returns an iterator that yields results as coroutines complete. | Yes            |
| `asyncio.ensure_future()`           | `asyncio.ensure_future(coro_or_future, *, loop=None)` | Wraps a coroutine or future into a Task.               | No                |
| `asyncio.current_task()`            | `asyncio.current_task(loop=None)`              | Returns the currently running task in the event loop.      | No                |
| `asyncio.all_tasks()`               | `asyncio.all_tasks(loop=None)`                 | Returns a set of all tasks currently scheduled.            | No                |
| `asyncio.get_running_loop()`        | `asyncio.get_running_loop()`                   | Returns the currently running event loop.                  | No                |
| `asyncio.run_coroutine_threadsafe()` | `asyncio.run_coroutine_threadsafe(coro, loop)` | Schedules the coroutine to be run in the event loop.        | No                |
| `asyncio.to_thread()`               | `asyncio.to_thread(func, *args, **kwargs)`     | Runs a function in a separate thread and returns a coroutine. | Yes            |
| `asyncio.open_connection()`         | `asyncio.open_connection(host=None, port=None, *, loop=None, timeout=None, ssl=None, **kwargs)` | Opens a network connection to a specified host and port.   | Yes               |
| `asyncio.start_server()`            | `asyncio.start_server(client_connected_cb, host=None, port=None, *, loop=None, ssl=None, **kwargs)` | Starts a TCP server.                                      | Yes               |
| `asyncio.start_unix_server()`       | `asyncio.start_unix_server(client_connected_cb, path, *, loop=None, ssl=None, **kwargs)` | Starts a Unix domain socket server.                       | Yes               |
| `asyncio.open_unix_connection()`    | `asyncio.open_unix_connection(path, *, loop=None, timeout=None, ssl=None, **kwargs)` | Opens a Unix domain socket connection.                    | Yes               |


### `asyncio` classes


| **Class**                   | **Description**                                                                                                              | **Usage**                                                                                                    |
|-----------------------------|------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| `asyncio.AbstractEventLoop`  | The base class for event loops. It manages and handles the asynchronous operations in `asyncio`.                             | Manages task execution, I/O events, and signal handling.                                                      |
| `asyncio.EventLoop`          | A concrete implementation of the event loop for running asynchronous tasks.                                                  | Created using `asyncio.get_event_loop()` or `asyncio.run()`. Handles scheduling of tasks and callbacks.       |
| `asyncio.Task`               | A wrapper for coroutines that run asynchronously in the event loop.                                                          | Created via `asyncio.create_task()` or `asyncio.ensure_future()` to schedule the execution of coroutines.     |
| `asyncio.Future`             | Represents a result that will be available in the future. Similar to `concurrent.futures.Future`.                            | Used in coordination with `asyncio.Task` to handle results or exceptions of asynchronous operations.          |
| `asyncio.Queue`              | A queue-like data structure for managing tasks in a producer-consumer model asynchronously.                                  | Supports operations like `put()`, `get()`, and `task_done()` for task coordination between coroutines.        |
| `asyncio.StreamReader`       | Used to read data from streams, such as socket connections, in an asynchronous manner.                                       | Used in TCP communication (e.g., `await reader.read()`).                                                      |
| `asyncio.StreamWriter`       | Used to write data to streams asynchronously.                                                                                | Used in TCP communication (e.g., `writer.write(data)`).                                                       |
| `asyncio.Lock`               | An asynchronous lock primitive that allows coroutines to wait for the lock to be acquired.                                   | Allows mutual exclusion between coroutines (similar to threading locks but for async).                        |
| `asyncio.Condition`          | Allows coroutines to wait until a specific condition is met.                                                                 | Similar to traditional condition variables but in an asynchronous context.                                    |
| `asyncio.Semaphore`          | Manages an internal counter, blocking access when the counter reaches zero. Used for limiting concurrent access.             | Used to limit the number of coroutines that can access a resource concurrently.                               |
| `asyncio.Event`              | A synchronization primitive that allows coroutines to wait for an event to be set before continuing.                         | Useful for controlling task flow by waiting for a specific event to be triggered.                             |
| `asyncio.Subprocess`         | A class for launching subprocesses asynchronously.                                                                           | Used to create, monitor, and control subprocesses asynchronously via `asyncio.create_subprocess_exec()` etc.  |
| `asyncio.StreamReaderProtocol` | Protocol class for handling streams of data, often used with `StreamReader` and `StreamWriter`.                            | Useful when working with custom protocols or processing data streams.                                         |
| `asyncio.Server`             | A class representing a server that listens for incoming connections.                                                         | Used in conjunction with `asyncio.start_server()` to handle multiple client connections asynchronously.       |
| `asyncio.Transport`          | An abstraction for handling underlying communication channels (e.g., sockets) in asyncio.                                    | Provides methods like `write()` and `close()` for low-level I/O operations.                                   |
| `asyncio.Protocol`           | Base class for implementing application-level protocols for communication, typically used with `Transport`.                  | Defines methods like `connection_made()`, `data_received()`, `connection_lost()`.                             |
| `asyncio.DatagramTransport`  | A transport class specifically for handling datagrams (UDP).                                                                 | Used for sending/receiving UDP data asynchronously.                                                          |
| `asyncio.DatagramProtocol`   | Protocol class for handling UDP communication. Similar to `Protocol` but for datagrams.                                       | Implements methods like `datagram_received()` for processing UDP packets.                                     |
| `asyncio.BaseEventLoop`      | A base class for event loops, from which concrete event loop implementations inherit.                                        | Provides low-level event loop behavior, used internally by asyncio.                                           |
| `asyncio.LimitOverrunError`  | Exception raised when reading from a stream and a buffer limit is exceeded.                                                  | Raised by `StreamReader.read()` when trying to read more data than allowed.                                   |
| `asyncio.IncompleteReadError`| Exception raised when `StreamReader.read()` reads less data than expected.                                                   | Commonly encountered in TCP streams when reading from incomplete data.                                        |
| `asyncio.TimeoutError`       | Exception raised when a timeout occurs.                                                                                      | Used with functions like `asyncio.wait_for()` to set time limits for task execution.                          |
| `asyncio.CancelledError`     | Exception raised when a task is canceled.                                                                                    | Raised when a task or coroutine is canceled (e.g., via `task.cancel()`).                                      |
| `asyncio.BoundedSemaphore`   | A version of `Semaphore` with a maximum upper bound.                                                                         | Used to restrict access to a resource, but with an upper limit for the semaphore counter.                     |



###  **`asyncio.AbstractEventLoop` Class Methods**
- Defines the abstract methods for event loop operations; not used directly.

| **Member**                           | **Await Required?** | **Notes**                                                                                           |
|--------------------------------------|---------------------|-----------------------------------------------------------------------------------------------------|
| `run_forever()`                      | No                  | Starts the event loop indefinitely, not awaited.                                                     |
| `run_until_complete(future)`         | No                  | Runs until a future completes, not awaited.                                                          |
| `create_task(coro)`                  | No                  | Schedules a coroutine as a task, does not need to be awaited.                                        |
| `call_later(delay, callback)`        | No                  | Schedules a callback, does not need `await`.                                                         |
| `call_soon(callback)`                | No                  | Schedules a callback, no need to await.                                                              |
| `stop()`                             | No                  | Stops the event loop, not awaited.                                                                   |
| `time()`                             | No                  | Returns the internal event loop time, no need to await.                                              |


### **`asyncio.BaseEventLoop` Class**
- A concrete implementation of AbstractEventLoop and the default event loop in asyncio.

| **Member**                           | **Type**   | **Description**                                                                                         | **Await Needed?** |
|--------------------------------------|------------|---------------------------------------------------------------------------------------------------------|-------------------|
| `run_forever()`                      | Method     | Runs the event loop indefinitely until `stop()` is called.                                              | No                |
| `run_until_complete(future)`         | Method     | Runs the event loop until the `future` is done and returns the result.                                  | No                |
| `create_task(coro)`                  | Method     | Schedules a coroutine to be executed and returns a `Task` object.                                        | No                |
| `call_later(delay, callback)`        | Method     | Schedules a callback to be called after a delay.                                                        | No                |
| `call_soon(callback)`                | Method     | Schedules a callback to be called as soon as possible.                                                   | No                |
| `stop()`                             | Method     | Stops the event loop after the current iteration completes.                                              | No                |
| `is_running()`                       | Method     | Returns `True` if the event loop is currently running.                                                   | No                |
| `time()`                             | Method     | Returns the current event loop time.                                                                     | No                |
| `add_reader(fd, callback)`           | Method     | Adds a callback to be invoked when reading from the file descriptor `fd` is possible.                    | No                |
| `add_writer(fd, callback)`           | Method     | Adds a callback to be invoked when writing to the file descriptor `fd` is possible.                      | No                |
| `remove_reader(fd)`                  | Method     | Removes a reader callback for the file descriptor `fd`.                                                  | No                |
| `remove_writer(fd)`                  | Method     | Removes a writer callback for the file descriptor `fd`.                                                  | No                |

### **`asyncio.EventLoop` Class**
- A more abstract interface; generally used as a proxy to BaseEventLoop.

| **Member**                           | **Type**   | **Description**                                                                                         | **Await Needed?** |
|--------------------------------------|------------|---------------------------------------------------------------------------------------------------------|-------------------|
| `run_forever()`                      | Method     | Runs the event loop indefinitely until `stop()` is called.                                              | No                |
| `run_until_complete(future)`         | Method     | Runs the event loop until the `future` is done and returns the result.                                  | No                |
| `create_task(coro)`                  | Method     | Schedules a coroutine to be executed and returns a `Task` object.                                        | No                |
| `call_later(delay, callback)`        | Method     | Schedules a callback to be called after a delay.                                                        | No                |
| `call_soon(callback)`                | Method     | Schedules a callback to be called as soon as possible.                                                   | No                |
| `stop()`                             | Method     | Stops the event loop after the current iteration completes.                                              | No                |
| `is_running()`                       | Method     | Returns `True` if the event loop is currently running.                                                   | No                |
| `time()`                             | Method     | Returns the current event loop time.                                                                     | No                |
| `add_reader(fd, callback)`           | Method     | Adds a callback to be invoked when reading from the file descriptor `fd` is possible.                    | No                |
| `add_writer(fd, callback)`           | Method     | Adds a callback to be invoked when writing to the file descriptor `fd` is possible.                      | No                |
| `remove_reader(fd)`                  | Method     | Removes a reader callback for the file descriptor `fd`.                                                  | No                |
| `remove_writer(fd)`                  | Method     | Removes a writer callback for the file descriptor `fd`.                                                  | No                |



### **`asyncio.Task` Class Methods**

| **Member**                           | **Await Required?** | **Notes**                                                                                           |
|--------------------------------------|---------------------|-----------------------------------------------------------------------------------------------------|
| `cancel()`                           | No                  | Cancels the task, not awaited.                                                                       |
| `done()`                             | No                  | Checks if the task is done, no need to await.                                                        |
| `result()`                           | No                  | Gets the result of the task if completed, not awaited.                                               |
| `exception()`                        | No                  | Gets the exception raised by the task, not awaited.                                                  |
| `add_done_callback(callback)`        | No                  | Schedules a callback for when the task is done, not awaited.                                         |



### **`asyncio.Future` Class Methods**

| **Member**                           | **Await Required?** | **Notes**                                                                                           |
|--------------------------------------|---------------------|-----------------------------------------------------------------------------------------------------|
| `cancel()`                           | No                  | Cancels the future, not awaited.                                                                     |
| `done()`                             | No                  | Checks if the future is done, no need to await.                                                      |
| `result()`                           | No                  | Gets the result of the future if completed, not awaited.                                             |
| `exception()`                        | No                  | Gets the exception raised by the future, not awaited.                                                |
| `set_result(result)`                 | No                  | Sets the result of the future, not awaited.                                                          |



### **`asyncio.StreamReader` Class Methods**

| **Member**                           | **Await Required?** | **Notes**                                                                                           |
|--------------------------------------|---------------------|-----------------------------------------------------------------------------------------------------|
| `read(n=-1)`                         | **Yes**             | Reads data from the stream.                                                                          |
| `readexactly(n)`                     | **Yes**             | Reads exactly `n` bytes from the stream.                                                             |
| `readline()`                         | **Yes**             | Reads a line from the stream.                                                                        |
| `at_eof()`                           | No                  | Checks if the stream has reached EOF, no need to await.                                              |



### **`asyncio.StreamWriter` Class Methods**

| **Member**                           | **Await Required?** | **Notes**                                                                                           |
|--------------------------------------|---------------------|-----------------------------------------------------------------------------------------------------|
| `write(data)`                        | No                  | Writes data to the stream, no need to await.                                                         |
| `drain()`                            | **Yes**             | Waits until it’s appropriate to resume writing to the stream.                                        |
| `close()`                            | No                  | Closes the stream, but does not need to be awaited.                                                  |


### **`asyncio.Subprocess` Class**

| **Member**                           | **Type**   | **Description**                                                                                         | **Await Needed?** |
|--------------------------------------|------------|---------------------------------------------------------------------------------------------------------|-------------------|
| `stdin`                              | Attribute  | A `StreamWriter` for standard input.                                                                     | No                |
| `stdout`                             | Attribute  | A `StreamReader` for standard output.                                                                    | No                |
| `stderr`                             | Attribute  | A `StreamReader` for standard error.                                                                     | No                |

### **`asyncio.StreamReaderProtocol` Class**

| **Member**                           | **Type**   | **Description**                                                                                         | **Await Needed?** |
|--------------------------------------|------------|---------------------------------------------------------------------------------------------------------|-------------------|
| `connection_made(transport)`         | Method     | Called when a connection is made.                                                                       | No                |
| `data_received(data)`                | Method     | Called when data is received.                                                                          | No                |
| `connection_lost(exc)`               | Method     | Called when the connection is closed or lost.                                                            | No                |

### **`asyncio.StreamWriterProtocol` Class**

| **Member**                           | **Type**   | **Description**                                                                                         | **Await Needed?** |
|--------------------------------------|------------|---------------------------------------------------------------------------------------------------------|-------------------|
| `connection_made(transport)`         | Method     | Called when a connection is made.                                                                       | No                |
| `data_received(data)`                | Method     | Called when data is received.                                                                          | No                |
| `connection_lost(exc)`               | Method     | Called when the connection is closed or lost.                                                            | No                |

### **`asyncio.DatagramTransport` Class**

| **Member**                           | **Type**   | **Description**                                                                                         | **Await Needed?** |
|--------------------------------------|------------|---------------------------------------------------------------------------------------------------------|-------------------|
| `sendto(data, addr)`                 | Method     | Sends `data` to the address `addr`.                                                                     | No                |
| `get_extra_info(name)`               | Method     | Retrieves extra information, such as `sockname` or `peername`.                                          | No                |
| `close()`                            | Method     | Closes the transport.                                                                                   | No                |

### **`asyncio.DatagramProtocol` Class**

| **Member**                           | **Type**   | **Description**                                                                                         | **Await Needed?** |
|--------------------------------------|------------|---------------------------------------------------------------------------------------------------------|-------------------|
| `connection_made(transport)`         | Method     | Called when a connection is made.                                                                       | No                |
| `datagram_received(data, addr)`      | Method     | Called when a datagram is received from the address `addr`.                                             | No                |
| `error_received(exc)`                | Method     | Called when an error is received.                                                                       | No                |
| `connection_lost(exc)`               | Method     | Called when the connection is closed or lost.                                                            | No                |


### **`asyncio.Lock` Class Methods**

| **Member**                           | **Await Required?** | **Notes**                                                                                           |
|--------------------------------------|---------------------|-----------------------------------------------------------------------------------------------------|
| `acquire()`                          | **Yes**             | Awaits until the lock is acquired.                                                                   |
| `release()`                          | No                  | Releases the lock, no need to await.                                                                 |
| `locked()`                           | No                  | Checks if the lock is currently acquired, no need to await.                                          |



### **`asyncio.Condition` Class**

| **Member**                           | **Type**   | **Description**                                                                                         | **Await Needed?** |
|--------------------------------------|------------|---------------------------------------------------------------------------------------------------------|-------------------|
| `acquire()`                          | Method     | Acquires the condition’s lock, waiting if necessary.                                                    | Yes               |
| `release()`                          | Method     | Releases the condition’s lock.                                                                          | No                |
| `wait()`                             | Method     | Waits until notified or cancelled.                                                                      | Yes               |
| `notify(n=1)`                        | Method     | Wakes up `n` waiting coroutines.                                                                        | No                |
| `notify_all()`                       | Method     | Wakes up all waiting coroutines.                                                                        | No                |

### **`asyncio.Semaphore` Class**

| **Member**                           | **Type**   | **Description**                                                                                         | **Await Needed?** |
|--------------------------------------|------------|---------------------------------------------------------------------------------------------------------|-------------------|
| `acquire()`                          | Method     | Acquires a semaphore, waiting if necessary.                                                             | Yes               |
| `release()`                          | Method     | Releases the semaphore, increasing the count.                                                           | No                |
| `locked()`                           | Method     | Returns `True` if the semaphore is currently locked.                                                    | No                |

### **`asyncio.Event` Class**

| **Member**                           | **Type**   | **Description**                                                                                         | **Await Needed?** |
|--------------------------------------|------------|---------------------------------------------------------------------------------------------------------|-------------------|
| `set()`                              | Method     | Sets the event, waking all coroutines waiting for it.                                                   | No                |
| `clear()`                            | Method     | Clears the event, so coroutines will wait again.                                                        | No                |
| `wait()`                             | Method     | Waits until the event is set.                                                                           | Yes               |
| `is_set()`                           | Method     | Returns `True` if the event is set.                                                                      | No                |


### **`asyncio.Queue` Class Methods**

| **Member**                           | **Await Required?** | **Notes**                                                                                           |
|--------------------------------------|---------------------|-----------------------------------------------------------------------------------------------------|
| `put(item)`                          | **Yes**             | Puts an item into the queue.                                                                         |
| `get()`                              | **Yes**             | Retrieves an item from the queue.                                                                    |
| `empty()`                            | No                  | Checks if the queue is empty, no need to await.                                                      |
| `full()`                             | No                  | Checks if the queue is full, no need to await.                                                       |



### **`asyncio.Server` Class Methods**

| **Member**                           | **Await Required?** | **Notes**                                                                                           |
|--------------------------------------|---------------------|-----------------------------------------------------------------------------------------------------|
| `start()`                            | **Yes**             | Starts accepting connections asynchronously.                                                         |
| `close()`                            | No                  | Closes the server, no need to await.                                                                 |
| `wait_closed()`                      | **Yes**             | Awaits until the server is completely closed.                                                        |



### **`asyncio.Protocol` Class Methods**

| **Member**                           | **Await Required?** | **Notes**                                                                                           |
|--------------------------------------|---------------------|-----------------------------------------------------------------------------------------------------|
| `connection_made(transport)`         | No                  | Called when a connection is made, no need to await.                                                  |
| `data_received(data)`                | No                  | Called when data is received, not awaited.                                                           |
| `connection_lost(exc)`               | No                  | Called when the connection is lost, not awaited.                                                     |



### **`asyncio.Transport` Class Methods**

| **Member**                           | **Await Required?** | **Notes**                                                                                           |
|--------------------------------------|---------------------|-----------------------------------------------------------------------------------------------------|
| `write(data)`                        | No                  | Writes data to the transport, no need to await.                                                      |
| `close()`                            | No                  | Closes the transport, no need to await.                                                              |
| `get_extra_info(name)`               | No                  | Retrieves extra information, no need to await.                                                       |



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


## Third-party Asynchronous Libraries
- [Curio - a coroutine-based library](https://github.com/dabeaz/curio)
- [Trio – a friendly Python library for async concurrency and I/O](https://github.com/python-trio/trio)
- [uvloop - a fast, drop-in replacement of the built-in asyncio event loop](https://github.com/MagicStack/uvloop)


# References
- [asyncio — Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)
- [Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/)
- [Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html)
  - [How to Use Generators and yield in Python](https://realpython.com/introduction-to-python-generators/)
- [Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/)