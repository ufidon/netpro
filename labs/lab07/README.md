# HTTP & HTTPS
This lab provides hands-on experience with building, testing, and securing a basic HTTP server in Python, along with client interactions using cURL. 

In your report, 
- 🎏 explain the code you added or modified
- 💻 illustrate with screenshots of corresponding outputs

---

## Get familiar with HTTP
Here’s an introduction to the HTTP protocol, along with a table listing all common HTTP methods, their descriptions, and typical usage.

---

### **Introduction to HTTP Protocol**

**HTTP (Hypertext Transfer Protocol)** is an application-layer protocol used for transmitting data over the web. It was designed for communication between web clients (browsers) and web servers, allowing the exchange of resources like HTML documents, images, videos, and other content. HTTP follows a client-server model, where a client makes a request to the server, and the server responds with the requested resource or information.

HTTP operates primarily over TCP (Transmission Control Protocol) and, in secure variations (HTTPS), over SSL/TLS (Secure Sockets Layer / Transport Layer Security). `It is a stateless protocol, meaning each request is independent, and the server doesn’t retain any information about previous requests unless explicitly stored (such as with cookies or session data)`.


### **HTTP Message Structure**
- 📑 Table 1

| Feature                       | HTTP Request Message                                   | HTTP Response Message                               |
|-------------------------------|-------------------------------------------------------|----------------------------------------------------|
| **Purpose**                   | Sent by the client to request a resource or action from the server. | Sent by the server to provide a response to the client's request. |
| **Structure**                 | Consists of a request line, headers, an empty line, and an optional body. | Consists of a status line, headers, an empty line, and an optional body. |
| **Request Line/Status Line**  | Includes the HTTP method, request URI, and HTTP version. | Includes the HTTP version, status code, and reason phrase. |
| **Example of Line**           | `GET /index.html HTTP/1.1`                           | `HTTP/1.1 200 OK`                                  |
| **Headers**                   | Contains headers that provide metadata about the request (e.g., `Host`, `User-Agent`, `Accept`). | Contains headers that provide metadata about the response (e.g., `Content-Type`, `Content-Length`, `Server`). |
| **Body**                      | (Optional) Contains data sent to the server (e.g., form data in POST requests). | (Optional) Contains data returned from the server (e.g., HTML, JSON). |
| **Content-Type**              | Indicates the media type of the request body (e.g., `application/json`). | Indicates the media type of the response body (e.g., `text/html`). |
| **Content-Length**            | Indicates the size of the request body in bytes (if present). | Indicates the size of the response body in bytes (if present). |
| **Transfer-Encoding**         | Can be included to indicate that the request body is sent in a specific encoding format, such as chunked (not commonly used). | Indicates that the response body is sent in a series of chunks, allowing for dynamic content generation. |
| **Examples of Methods**       | GET, POST, PUT, DELETE, HEAD, OPTIONS, PATCH        | N/A (Responses do not use methods, but status codes indicate success or failure of the requested method.) |
| **Connection Management**      | Can include `Connection: close` to indicate that the connection should be closed after the response. | May include `Connection: close` to indicate that the server will close the connection after sending the response. |

### **HTTP Message Framing**

HTTP message framing refers to the mechanism by which an HTTP message is delineated and understood in terms of its boundaries. It is essential for both the client and the server to understand when a complete HTTP message has been received to process it correctly.

- **Determining a Complete HTTP Message**

There are two primary methods used in HTTP to determine the length of a message and to delineate the boundaries of the request and response:

1. **Content-Length**:
   - The `Content-Length` header indicates the exact size of the body in bytes. This header allows the recipient to know how many bytes to read to consider the message complete. Once the specified number of bytes has been read, the message is considered complete.

2. **Transfer-Encoding**:
   - The `Transfer-Encoding` header is used to indicate that the message body is sent in a certain encoding. The most common value for this header is `chunked`, which means the message is sent in a series of chunks. Each chunk is preceded by its size in bytes (in hexadecimal), followed by the chunk data, and is terminated by a zero-length chunk, which indicates the end of the message.
Yes, in HTTP/1.1 chunked transfer encoding, each chunk of data is indeed followed by a CRLF sequence (`\r\n`). Here’s how chunked transfer encoding works in detail:

   - **Chunked Transfer Encoding**
     1. **Chunk Structure**:
        - Each chunk consists of:
          - A **chunk size** (in hexadecimal) followed by `\r\n`.
          - The **actual chunk data**.
          - A trailing `\r\n` after the chunk data.

     2. **End of Message**:
        - The last chunk is indicated by a chunk size of `0`, followed by another `\r\n`. This signifies the end of the response body.

   - **Example**
   Here's a simple illustration of how a chunked response looks:

   ```
   HTTP/1.1 200 OK
   Transfer-Encoding: chunked
   Content-Type: text/plain

   4\r\n            # This is the size of the first chunk in hexadecimal
   Wiki\r\n        # This is the first chunk data
   5\r\n            # This is the size of the second chunk
   pedia\r\n       # This is the second chunk data
   0\r\n            # This indicates the end of the chunks
   \r\n            # This is the terminating CRLF
   ```

- **Comparison of `Content-Length` and `Transfer-Encoding`**
- 📑 Table 2

| Feature                      | Content-Length                                     | Transfer-Encoding                                     |
|------------------------------|---------------------------------------------------|------------------------------------------------------|
| **Definition**               | Indicates the size of the message body in bytes. | Indicates the encoding used for the message body.    |
| **Usage**                    | Used when the size of the body is known in advance. | Used when the body is sent in chunks, or when the size is not known in advance. |
| **How it Works**             | The sender specifies the exact number of bytes to expect. The receiver reads that many bytes to complete the message. | The body is sent in a series of chunks, each preceded by its size. The message ends with a zero-length chunk. |
| **Header Example**           | `Content-Length: 1234`                            | `Transfer-Encoding: chunked`                          |
| **Connection Closure**       | The connection can be closed or kept alive, depending on the `Connection` header. | The connection remains open until a zero-length chunk is received. |
| **Limitations**              | Cannot be used with `chunked` transfer encoding. | Can be used to send dynamically generated content.    |
| **Overhead**                 | Low overhead, as it requires only the length value. | May add overhead due to chunk sizes and formatting.   |
| **Common Use Cases**         | Used in most requests and responses when the content size is known (e.g., file uploads). | Useful for streaming data or when the final content length is unknown at the start of transmission. |

---

### **HTTP Methods Table**

The HTTP methods define the type of operation the client wants to perform on the server resource. Here is a list of common HTTP methods, with descriptions and examples of usage:

- 📑 Table 3

| **HTTP Method** | **Description**                                                                 | **Typical Usage**                                                                                 |
|-----------------|---------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| **GET**         | Retrieves data from the server.                                                 | Used to fetch resources (e.g., HTML pages, images). Safe and idempotent, as it does not modify data. |
| **POST**        | Sends data to the server to create a new resource or submit form data.          | Commonly used for form submissions, file uploads, and data creation. May change server state.    |
| **PUT**         | Replaces or updates a resource on the server with the data provided.            | Used for updating existing resources. Idempotent, meaning repeated requests yield the same result.|
| **DELETE**      | Deletes a specified resource on the server.                                     | Used to remove resources, such as files or records, from the server.                             |
| **PATCH**       | Partially updates a resource with only the data provided.                       | Useful for making partial modifications to a resource without sending the entire dataset.        |
| **HEAD**        | Similar to GET, but only retrieves headers (no body) for a resource.            | Used to check the existence or metadata of a resource, like its size or modification date.       |
| **OPTIONS**     | Returns HTTP methods supported by the server for a specific resource.           | Useful for checking server capabilities, such as supported methods and CORS (Cross-Origin Resource Sharing) configurations. |
| **CONNECT**     | Establishes a tunnel to the server, typically used for SSL/TLS connections.     | Commonly used for HTTPS connections by establishing a proxy tunnel.                              |
| **TRACE**       | Echoes the received request, allowing the client to see what changes are made along the request path. | Used mainly for debugging and diagnostics, though rarely used due to security concerns.          |

---

## How to test HTTP server using cURL
**cURL** (Client URL) is a command-line tool used to transfer data to and from a server, supporting a wide range of protocols, including HTTP, HTTPS, FTP, and more. It is especially useful for interacting with HTTP and HTTPS endpoints, making it a staple tool for developers and administrators to test APIs, download files, and perform network troubleshooting.

With cURL, you can send various HTTP methods to an HTTP server, inspect responses, and use options to customize requests with headers, authentication, and data payloads.

---

### **Basic Syntax of cURL**

The general syntax for a cURL command is:
```bash
curl [options] <URL>
```

### **HTTP Method Examples with cURL**

Here is a table listing each HTTP method and how to send it to an HTTP server using cURL.

📑 Table 4

| **HTTP Method** | **cURL Command**                                                                                                  | **Description**                                                                                   |
|-----------------|--------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| **GET**         | `curl -X GET <URL>` or simply `curl <URL>`                                                                       | Retrieves a resource from the server. By default, cURL uses GET if no method is specified.       |
| **POST**        | `curl -X POST -d "key=value" <URL>`                                                                               | Sends data to the server, typically to create a resource. `-d` specifies the data payload.       |
| **PUT**         | `curl -X PUT -d "key=value" <URL>`                                                                                | Updates or replaces a resource on the server.                                                    |
| **DELETE**      | `curl -X DELETE <URL>`                                                                                            | Deletes a specified resource from the server.                                                    |
| **PATCH**       | `curl -X PATCH -d "key=value" <URL>`                                                                              | Partially updates a resource with only the data provided.                                        |
| **HEAD**        | `curl -I <URL>`                                                                                                   | Retrieves only the headers for a resource, without the response body.                            |
| **OPTIONS**     | `curl -X OPTIONS <URL>`                                                                                           | Requests the HTTP methods supported by the server for a specific resource.                       |
| **CONNECT**     | `curl -X CONNECT <URL>`                                                                                           | Used to establish a tunnel, primarily for SSL/TLS connections. Not typically used directly in cURL.|
| **TRACE**       | `curl -X TRACE <URL>`                                                                                             | Echoes the request, used mainly for debugging and diagnostics.                                   |

---

### **Examples of Common cURL Commands**

- **GET Example**:
  ```bash
  curl https://jsonplaceholder.typicode.com/posts/1
  ```
  Retrieves the post with ID 1 from the specified URL.

- **POST Example**:
  ```bash
  curl -X POST -d "title=Sample Title&body=This is a sample post" https://jsonplaceholder.typicode.com/posts
  ```
  Sends a POST request with form-encoded data to create a new resource.

- **PUT Example**:
  ```bash
  curl -X PUT -d "title=Updated Title" https://jsonplaceholder.typicode.com/posts/1
  ```
  Updates the title of the post with ID 1.

- **DELETE Example**:
  ```bash
  curl -X DELETE https://jsonplaceholder.typicode.com/posts/1
  ```
  Deletes the post with ID 1.

---

## Why Browser Is Not A Good Choice?
A web browser can send certain HTTP methods, but its capability is somewhat limited due to security policies and typical use cases. While browsers support sending **GET** and **POST** requests directly, they can send **PUT**, **DELETE**, **PATCH**, **HEAD**, and **OPTIONS** indirectly via JavaScript (typically using the `fetch` API or `XMLHttpRequest`). However, direct user interaction with these methods is limited, and security policies like CORS (Cross-Origin Resource Sharing)  control their use for cross-origin requests. Direct access to **CONNECT** and **TRACE** is typically restricted due to security risks.

### **HTTP Methods Commonly Supported by Browsers**

1. **GET**: 
   - **Description**: Browsers use GET to retrieve resources, such as HTML pages, images, and other static assets.
   - **How**: Automatically sent when loading pages, clicking links, or entering URLs in the address bar.
   
2. **POST**:
   - **Description**: Used to send data to the server, often via forms (e.g., form submissions and file uploads).
   - **How**: Triggered when a user submits an HTML form with the method set to `POST`.

### **Other Methods with Limited Support or Restrictions**

3. **PUT, DELETE, PATCH**:
   - **Description**: These methods are typically used in APIs for creating, updating, and deleting resources.
   - **Browser Limitations**: While technically possible, browsers restrict these methods in standard form submissions. They can only be sent via JavaScript, such as using the `fetch` API or `XMLHttpRequest`.
   - **Security Considerations**: Browsers enforce CORS policies when using these methods, often requiring preflight `OPTIONS` requests to check server permissions.

4. **HEAD**:
   - **Description**: Retrieves only the headers for a resource without the body, which can be useful for checking resource metadata.
   - **Browser Support**: Typically used in the background, as with `fetch` or `XMLHttpRequest`.

5. **OPTIONS**:
   - **Description**: Used by browsers to determine which HTTP methods and headers a server supports, especially for cross-origin requests.
   - **Browser Role**: Browsers send automatic OPTIONS requests (preflight requests) before certain cross-origin requests to ensure the server permits the main request.

6. **CONNECT, TRACE**:
   - **Description**: `CONNECT` is used to establish a network tunnel, often for HTTPS connections, while `TRACE` echoes the received request.
   - **Browser Restriction**: Browsers generally do not allow direct use of `CONNECT` or `TRACE`, as these could pose security risks by exposing internal details or allowing unwanted tunneling.

---

## **Lab Tasks**

### **Task 1: Exploring HTTP Requests and Responses with Curl**
1. **Goal**: To understand how different HTTP methods work and how servers respond to them, from the `perspective of client`, you will use curl to send requests with various HTTP methods to a public website and document the responses.
#### Instructions

1. **Choose a Website**  
   Select a public website that allows for different HTTP methods. You could use a test API service, such as `https://httpbin.org`, which responds to all HTTP methods. *Note: Avoid sending requests with non-standard HTTP methods to production websites, as they may block or restrict such traffic.*

2. **Send HTTP Requests**  
   Use `curl` to send HTTP requests with each of the following HTTP methods:
   
   - `GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTIONS`, `PATCH`
   - `TRACE`

3. **Investigate the Responses**  
   For each request, observe and record:
   
   - **Status Code**: The HTTP status code returned (e.g., 200 OK, 405 Method Not Allowed).
   - **Response Headers**: Headers returned by the server (e.g., `Content-Type`, `Allow`).
   - **Response Body**: 
     - Body content if available. Save it in a HTML file, show the rendered page.
     - Some methods, like `HEAD`, should not return a body.
   - **Description of Findings**: Note any patterns, unique responses, or error messages encountered.

4. **Document Your Findings**  
   Organize your results in a table format, like this:

    -  📑 Table 5

   | HTTP Method | Status Code | Response Headers                | Response Body     | Notes/Observations                       |
   |-------------|-------------|---------------------------------|-------------------|------------------------------------------|
   | GET         | 200         | Content-Type, Content-Length    | HTML or JSON data | Commonly used to retrieve information.   |
   | POST        | 200         | Content-Type                    | Confirmation data | Used to create resources on the server.  |
   | PUT         | 405         | Allow: GET, POST                | N/A               | Method not allowed for most websites.    |
   | DELETE      | 405         | Allow: GET, POST                | N/A               | Not allowed for public sites.            |
   | HEAD        | 200         | Content-Type, Content-Length    | None              | Similar to GET but without body content. |
   | OPTIONS     | 200         | Allow: GET, POST, HEAD, OPTIONS | Methods supported | Indicates allowed methods on the server. |
   | PATCH       | 405         | Allow: GET, POST                | N/A               | Not often supported on public servers.   |
   | TRACE       | 405         | N/A                             | N/A               | Typically disabled for security reasons. |

5. **Questions to Answer**  

   - Which methods are supported by most websites?  
   - Why do some methods (like DELETE or TRACE) return a `405 Method Not Allowed`?  
   - What response headers are unique to certain HTTP methods?  
   - What is the purpose of the `OPTIONS` method, and how does the server respond to it?


#### Curl Commands for Each HTTP Method

Here’s a sample `curl` command for each method:

```bash
# GET request
curl -v -X GET https://httpbin.org/get

# POST request
curl -v -X POST https://httpbin.org/post -d "param1=value1&param2=value2"

# PUT request
curl -v -X PUT https://httpbin.org/put -d "param=value"

# DELETE request
curl -v -X DELETE https://httpbin.org/delete

# HEAD request
curl -v -I https://httpbin.org/get

# OPTIONS request
curl -v -X OPTIONS https://httpbin.org/get -i

# PATCH request
curl -v -X PATCH https://httpbin.org/patch -d "param=value"

# TRACE request
curl -v -X TRACE https://httpbin.org/trace
```

> **Note**: Some public websites or APIs may block certain HTTP methods like `TRACE` for security reasons, which is a good learning point about real-world HTTP configurations.


---

### **Task 2: Investigating HTTP Messages From the Perspective of Server**
1. **Goal**: Given the HTTP server [s1.py](./code/s1.py) that receives raw HTTP requests, displays them in the console, and sends a formatted HTML table back to the client with details of the request. Investigate http messages from the perspective of server.
   - ⚠️ Don't open the HTTP server in multiple browsers or tabs.

2. **Instructions**:

   For each step below, investigate the output on both the client and the server, describe your findings.
   - Run `s1.py`, access it from a browser such as Google Chrome with url: `http://127.0.0.1:8080`.
     - What is the HTTP method sent to the server? Describe the interesting headers you found.
     - Can you send HTTP methods other than GET through the browser without client-side script?
     - POST methods are usually sent using HTML forms. Modify `s1.py` so that it can respond with a login page [index.html](./code/index.html) when access `http://127.0.0.1:8080/index.html`.
       - Fill the login page then submit
   - Browser restricted methods can only be sent via JavaScript, such as using the fetch API or XMLHttpRequest. forms. Modify `s1.py` so that it can respond with a full methods page [allmethods.html](./code/allmethods.html) when access `http://127.0.0.1:8080/allmethods.html`.
     - Click each button and explained what you observed
     - Which methods are successful? Which methods are failed? Why?
       - 👉 Hint: Use WireShark to find out failed methods are NOT sent out by the browser at all.
       - Or watch browser's console of `Developers tools`.

### **Task 3: Secure the HTTP Server with SSL/TLS**
1. **Goal**: Add SSL/TLS encryption to `the server you updated in Task 2` using the `ssl` library to transform it into an HTTPS server.
2. **Instructions**:
   - Create or obtain a self-signed SSL certificate and private key
     - use OpenSSL for simplicity:
     ```bash
     openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt -days 365 -nodes
     ```
   - Wrap the socket with SSL/TLS using Python's `ssl` library.
   - Ensure the server listens securely on a new port, like 8443.

   **Sample code for reference only**:

```python
   import ssl

   def secure_http_server():
       server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       server_socket.bind(('127.0.0.1', 8443))
       server_socket.listen(5)
       print("HTTPS Server running on port 8443...")

       # Wrap the socket with SSL
       context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
       context.load_cert_chain(certfile="path/to/cert.pem", keyfile="path/to/key.pem")
       secure_socket = context.wrap_socket(server_socket, server_side=True)

       while True:
           client_socket, addr = secure_socket.accept()
           print(f"Secure connection from {addr}")
           request_data = client_socket.recv(1024).decode()
           print("Raw HTTPS Request:")
           print(request_data)

           # Respond with a table of details
           response = f"""HTTP/1.1 200 OK
Content-Type: text/html

<html>
<body>
<h2>Request Details (HTTPS)</h2>
<table border="1">
<tr><th>Raw Request</th><td>{request_data.replace('<', '&lt;').replace('>', '&gt;')}</td></tr>
</table>
</body>
</html>"""
           client_socket.sendall(response.encode())
           client_socket.close()

   secure_http_server()
```

### **Task 4: Test the HTTPS Server with cURL**
1. **Goal**: Test the HTTPS server’s functionality and SSL/TLS security using cURL and browsers.
2. **Instructions**:
   - Change line 28 `const url = 'http://127.0.0.1:8080';` in `allmethods.html` to 
   - `const url = 'http://127.0.0.1:8443';`
   - Describe the different between the following two commands
     - `curl -v https://127.0.0.1:8443`
     - `curl -v -k https://127.0.0.1:8443`
   - Redo `all cURL commands listed in Task 1` in the successful way.
     - **Note**: Use `-k` to allow cURL to accept a self-signed certificate for testing purposes.
   - Access `https://127.0.0.1:8443` with a browser.
     - Can it access `https://127.0.0.1:8443` fluently? Why?
     - Make the access painlessly.
     - Access `https://127.0.0.1:8443/index.html` then submit the login credential.
     - Access `https://127.0.0.1:8443/allmethods.html` then click each button separately.
   - Compare your findings with those from Task 2. Explain the differences.

# References
- [Favicon generator](https://realfavicongenerator.net/)