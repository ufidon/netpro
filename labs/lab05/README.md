# Securing Socket Communication with SSL

## Overview
In this lab, you will enhance a toy FTP server and client from the provided reference code, understand the importance of securing data transmission, and implement SSL to protect data from being captured by tools like Wireshark. 

In your report, 
- 🎏 explain the code you added or modified
- 💻 illustrate with screenshots of corresponding outputs

---

## Get Familiar with FTP

**File Transfer Protocol (FTP)** is a standard network protocol used to transfer files between a client and a server over a TCP/IP-based network (like the Internet). FTP allows users to upload, download, rename, delete, and manipulate files and directories on a server. It was designed as an application-layer protocol within the Internet Protocol Suite, operating over TCP/IP.

FTP is defined in **RFC 959** and works based on a client-server architecture. A user (client) connects to an FTP server to perform various operations on files and directories.


**Key Concepts of FTP**

1. **Control and Data Connections**: FTP operates using two channels:
   - **Control Connection (Port 21)**: This connection is used for sending commands and receiving responses. The control connection stays open for the entire session.
   - **Data Connection (Port 20 or ephemeral port)**: This connection is used for transferring files and directory listings between the client and server. It can either be in **active** or **passive** mode.

2. **Active vs Passive Mode**
   - **Active Mode**: The client opens a port and waits for the server to connect back to it from the server’s data port (20). The client tells the server which port to use via the `PORT` command.
   - **Passive Mode (PASV)**: The server opens a random port and informs the client which port to use. The client then establishes the data connection to that server port.
     - `THIS MODE IS PREFERRED`.

3. **Authentication**
   - FTP allows for both **anonymous access** and **authenticated access**.
   - Anonymous access is often used for public FTP servers where users can log in using the username `anonymous` and an email address as a password or without a password.
   - For authenticated access, the client provides a username (`USER`) and password (`PASS`) to log in.


**FTP Communication Flow**

The communication between the FTP client and server typically involves the following steps:

1. **Client Establishes a Control Connection**:
   - The client initiates a connection to the FTP server on **port 21**.
   - The server replies with a status code `220` indicating that the FTP service is ready.

2. **Client Sends Login Credentials**:
   - The client sends the `USER` command followed by the username.
   - The server responds with `331` (User name okay, need password).
   - The client then sends the `PASS` command followed by the password.
   - If the credentials are valid, the server responds with `230` (User logged in, proceed).

3. **Client Issues Commands**:
   - The client issues FTP commands, such as `LIST` (to list files), `RETR` (to download a file), or `STOR` (to upload a file).
   - The server responds with status codes (e.g., `150` to indicate file status okay, or `226` to indicate transfer complete).

4. **Establishing Data Connections**:
   - When the client requests a file transfer (via `RETR`, `STOR`, etc.), the data connection is established:
     - **Active Mode**: The server connects to the client’s IP and port specified in the `PORT` command.
     - **Passive Mode**: The client connects to the server’s IP and port specified in the `PASV` command.

5. **Transferring Data**:
   - The actual file data or directory listing is sent over the data connection.
   - Once the transfer is complete, the data connection is closed.

6. **Closing the Connection**:
   - After all transfers and commands are complete, the client can close the session using the `QUIT` command.
   - The server responds with `221` (Service closing control connection) and terminates the control connection.


**FTP Modes of Transfer**

FTP supports two modes for transferring data:

- **ASCII Mode**: Used for text files. In this mode, FTP performs end-of-line character conversions as needed based on the client or server's system.
- **Binary Mode (Image Mode)**: Used for non-text files like images, videos, or software. In binary mode, the file is transferred byte-for-byte without any conversion.
  - `THIS MODE IS PREFERRED`.

**FTP Commands and Responses**

1. **Client Commands**:
   - **USER**: Sends the username to the server for authentication.
   - **PASS**: Sends the password to the server for authentication.
   - **LIST**: Lists files and directories in the current directory.
   - **RETR**: Retrieves a file from the server.
   - **STOR**: Uploads a file to the server.
   - **DELE**: Deletes a file on the server.
   - **CWD**: Changes the current working directory.
   - **PWD**: Displays the current directory on the server.
   - **QUIT**: Terminates the connection.

2. **Server Responses** (Status Codes):
   - **1xx**: Positive Preliminary reply (e.g., `150` – File status okay, about to open data connection).
   - **2xx**: Positive Completion reply (e.g., `226` – Closing data connection, file transfer successful).
   - **3xx**: Positive Intermediate reply (e.g., `331` – Username okay, need password).
   - **4xx**: Transient Negative Completion reply (e.g., `421` – Service not available).
   - **5xx**: Permanent Negative Completion reply (e.g., `550` – File not available).

**Security in FTP**

FTP, in its basic form, is an **insecure protocol** because it transmits data (including usernames and passwords) in **plain text**. This makes it vulnerable to packet sniffing and Man-in-the-Middle (MITM) attacks.

To secure FTP:
- 🎏 **FTPS (FTP Secure)**: This is FTP over SSL/TLS. It encrypts the control and data channels, securing the connection.
- **SFTP (SSH File Transfer Protocol)**: This is a different protocol that runs over SSH (Secure Shell) and provides secure file transfer capabilities.


**FTP Commands & Status Codes**

- **Table 1: FTP Protocol Commands**

| **Command**  | **Description**                                               |
|--------------|---------------------------------------------------------------|
| `USER`       | Specifies the username for authentication.                    |
| `PASS`       | Specifies the password for authentication.                    |
| `LIST`       | Requests a list of files in the current directory.            |
| `RETR`       | Retrieves (downloads) a file from the server.                 |
| `STOR`       | Stores (uploads) a file on the server.                        |
| `DELE`       | Deletes a file from the server.                               |
| `CWD`        | Changes the working directory on the server.                  |
| `PWD`        | Displays the current working directory.                       |
| `MKD`        | Creates a new directory on the server.                        |
| `RMD`        | Removes a directory on the server.                            |
| `QUIT`       | Closes the connection to the FTP server.                      |
| `PORT`       | Specifies the port for the client to listen for data connections (active mode). |
| `PASV`       | Requests the server to enter passive mode for data connections. |
| `ABOR`       | Aborts the current file transfer.                             |
| `RNFR`       | Specifies the file to be renamed (from).                      |
| `RNTO`       | Renames a file (to).                                          |
| `NOOP`       | No operation; keeps the connection alive.                     |
| `SYST`       | Requests the operating system type of the server.             |
| `TYPE`       | Specifies the data type (ASCII or binary) for file transfers. |
| `HELP`       | Asks for help or information about FTP commands.              |


- **Table 2: FTP Status Codes**

| **Status Code** | **Description**                                               |
|-----------------|---------------------------------------------------------------|
| **1xx**         | **Positive Preliminary Reply**: The command is accepted and is being processed, but further action is needed to complete it. |
| **110**         | Restart marker reply.                                          |
| **120**         | Service ready in n minutes.                                    |
| **125**         | Data connection already open; transfer starting.               |
| **150**         | File status okay; about to open data connection.               |
| **2xx**         | **Positive Completion Reply**: The requested action has been successfully completed. |
| **200**         | Command okay.                                                  |
| **202**         | Command not implemented, but not needed.                      |
| **211**         | System status, or system help reply.                           |
| **212**         | Directory status.                                              |
| **213**         | File status.                                                   |
| **214**         | Help message.                                                  |
| **215**         | NAME system type (e.g., UNIX).                                 |
| **220**         | Service ready for new user.                                    |
| **221**         | Service closing control connection (Goodbye).                  |
| **225**         | Data connection open; no transfer in progress.                 |
| **226**         | Closing data connection; requested file action successful.     |
| **230**         | User logged in, proceed.                                       |
| **250**         | Requested file action okay, completed.                         |
| **257**         | "PATHNAME" created.                                            |
| **3xx**         | **Positive Intermediate Reply**: The command has been accepted, but further information is needed from the client to complete the action. |
| **331**         | User name okay, need password.                                 |
| **332**         | Need account for login.                                        |
| **350**         | Requested file action pending further information.             |
| **4xx**         | **Transient Negative Completion Reply**: The command failed but may succeed if reattempted later. |
| **421**         | Service not available, closing control connection.             |
| **425**         | Can't open data connection.                                    |
| **426**         | Connection closed; transfer aborted.                           |
| **450**         | Requested file action not taken (e.g., file unavailable).      |
| **451**         | Requested action aborted: local error in processing.           |
| **452**         | Requested action not taken: insufficient storage.              |
| **5xx**         | **Permanent Negative Completion Reply**: The command failed and should not be reattempted. |
| **500**         | Syntax error, command unrecognized.                            |
| **501**         | Syntax error in parameters or arguments.                       |
| **502**         | Command not implemented.                                       |
| **503**         | Bad sequence of commands.                                      |
| **504**         | Command not implemented for that parameter.                    |
| **530**         | Not logged in.                                                 |
| **532**         | Need account for storing files.                                |
| **550**         | Requested action not taken (e.g., file unavailable).           |
| **551**         | Requested action aborted: page type unknown.                   |
| **552**         | Requested file action aborted: exceeded storage allocation.    |
| **553**         | Requested action not taken: invalid file name.                 |


---

# **Objective**
By the end of this lab, you will:
1. Learn about ftp protocol.
2. Understand how packet sniffing can expose unencrypted data, such as an image file.
3. Implement SSL encryption in Python sockets to secure FTP communications.
4. Observe the difference between sniffing unencrypted and encrypted traffic.

- ⚠️ All reference codes are provided for reference only!
---

# **Task 1: Improve the Toy FTP Server and Client**

- Based on the supplied reference code
  - [FTP server](./code/ftpServer.py)
  - [FTP client](./code/ftpClient.py)

- 🎏 Improve the USER and PASS command so that the user can enter them in the console
  - Handle wrong user name and password correspondingly
- 💻 Sample output:

```
# Server output: python3 ftpServer.py 
FTP server listening on 0.0.0.0:2121
Accepted connection from ('127.0.0.1', 46500)
Received command: USER Alice
Received command: USER user
Received command: PASS 123
Received command: PASS password
Received command: LIST
Received command: PASV
Received command: RETR to.txt
Received command: RETR todown.txt
Received command: PASV
Received command: STOR toup.txt
Received command: PASV
Received command: QUIT

# Client output:  python3 ftpClient.py 
Server: 220 Welcome to Simple FTP Server
ftp>  
ftp> HELP
Invalid command before authenticated. Available commands: USER username, PASS password
ftp> USER
Illegal USER command.
ftp> USER Alice
Server response: 332 Username incorrect.
ftp> USER user
Server response: 331 Username okay, need password.
ftp> PASS
Illegal PASS command.
ftp> PASS 123
Server response: 530 Password incorrect.
ftp> PASS password
Server response: 230 User logged in, proceed.
ftp> HELP
Invalid command after authenticated. Available commands: LIST, RETR <filename>, STOR <filename>, QUIT
ftp> LIST
Server response: 150 Here comes the directory listing.
Server response: 227 Entering Passive Mode (0,0,0,0,168,231)
Directory listing:
test_file.txt
secret.txt

sec.txt
SpacePalace.jpg

todown.txt

Server response: 226 Directory send OK.
ftp> RETR to.txt
Server response: 550 File not found.
ftp> RETR todown.txt
Server response: 150 File status okay; about to open data connection.
Server response: 227 Entering Passive Mode (0,0,0,0,169,59)
Downloaded todown.txt
Server response: 226 Transfer complete.
ftp> STOR toup.txt
Server response: 150 Ready to receive data.
Server response: 227 Entering Passive Mode (0,0,0,0,229,105)
Uploaded toup.txt
Server response: 226 Transfer complete.
ftp> QUIT
Server response: 221 Goodbye.
Connection closed. Exiting.
```

# **Task 2: Use FTP Client to Download an Image and Sniff with Wireshark**
- Put a JPEG image in the the `ftp_root` folder
- Download the JPEG image file from the FTP server and capture the network traffic using Wireshark.

## **Instructions**:
1. **Run Wireshark**:
   - Capture traffic on the network interface used by the FTP server and client.
   - Filter traffic using:
     ```plaintext
     tcp.port == 21
     ```

2. **Download an Image**:
   - Use the FTP client to download an image from the server (`SpacePalace.jpg`).

3. **Analyze the Packets**:
   - 🎏 Find the user name and password in the captured packets
   - 🎏 Analyze the captured packets to locate the image data. 
     - Reconstruct the image by extracting the raw bytes.

👉 How to retrieve a JPEG image from sniffed TCP raw packets?

- **1. Identify the Image Data in Wireshark**
  - Look for the data transfer where the image is being downloaded, which might be indicated by a `RETR` command in FTP or by packets carrying a large amount of data.

  - **Identify JPEG Headers and Trailers**:
    - JPEG files always start with a specific **file signature** known as the "Start of Image" (SOI) marker `0xFFD8`
    - end with the **End of Image** (EOI) marker `0xFFD9`.

- **2. Follow the TCP Stream**
  - In Wireshark, the best way to extract the data is by reconstructing the TCP stream.
  1. **Right-click** on any packet related to the data transfer (in this case, the `RETR` response or a data packet from the server).
  2. Choose **"Follow" > "TCP Stream"**.
  3. Wireshark will show you the entire conversation between the client and server in that TCP stream. Look for the image data starting from `FFD8` and ending with `FFD9`.

- **3. Extract only the image data**
   - In the TCP Stream view, the entire conversation will include both FTP commands and image data. 🎏 You need to isolate the raw binary data of the image (between the `FFD8` and `FFD9` markers).
   - Copy all the binary data starting from `FFD8` to `FFD9`.

- **4. Save the Raw Data to a File**
  - Once you've isolated the binary data from the TCP stream:
  - **Save it as binary data to a file** with a `.jpg` extension.
  
- **5. Convert Hex to Binary (Optional)**
  - If the data is represented in hexadecimal format (which it often is in Wireshark), you may need to convert it into binary before saving it.
  - You can use a Python script to convert the hex to binary and save it as a `.jpg` file:

    ```python
        # Convert the hex string to binary data
        binary_data = bytes.fromhex(hex_string)

        # Write the binary data to a file
        with open(output_filename, 'wb') as file:
            file.write(binary_data)
    ```

- **6. Verify the Image**
  - After saving the file, open it to verify that the image is intact and correct.
  - If the image does not open, double-check that you have accurately copied the binary data from the TCP stream and that you haven't included extra characters (e.g., FTP protocol information).

---

# **Task 3: Secure the FTP Server and Client with SSL**

SSL ensures that the data sent over the network is encrypted, making it unreadable to anyone intercepting the packets.
- 🎏 Improve on the code your completed in Task 1.

## **Instructions**:
1. **Modify the Server**:
   - 🎏 Use Python’s `ssl` library to wrap the server socket with SSL.
   - SSL-Wrapped Server Reference Code:
      ```python
      import socket
      import ssl
      import os
      import struct

      class SimpleFTPServer:
          def __init__(self, host='127.0.0.1', port=21):
              self.host = host
              self.port = port
              self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
              self.server_socket.bind((self.host, self.port))
              self.server_socket.listen(5)
              self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
              self.context.load_cert_chain(certfile="server.crt", keyfile="server.key")
              print(f"SSL-secured FTP Server started on {self.host}:{self.port}")

          def handle_client(self, client_socket):
              client_socket.send(b"220 Simple FTP Server Ready\r\n")
              # Rest of the server code from Task 1 remains unchanged

          def start(self):
              while True:
                  client_socket, addr = self.server_socket.accept()
                  secure_socket = self.context.wrap_socket(client_socket, server_side=True)
                  print(f"Accepted SSL connection from {addr}")
                  self.handle_client(secure_socket)
      ```

2. **Modify the Client**:
   - 🎏 Wrap the client’s socket with SSL as well.
   - SSL-Wrapped Client Reference Code:
      ```python
      import socket
      import ssl
      import struct

      class SimpleFTPClient:
          def __init__(self, server_ip='127.0.0.1', server_port=21):
              self.server_ip = server_ip
              self.server_port = server_port
              self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
              self.context = ssl.create_default_context()
          
          def connect(self):
              self.client_socket = self.context.wrap_socket(self.client_socket)
              self.client_socket.connect((self.server_ip, self.server_port))
              # Rest of the client code from Task 1 remains unchanged
      ```

👉 **Create self-signed certificates for the server**:
 
  ```bash
  openssl req -new -x509 -days 365 -nodes -out server.crt -keyout server.key
  ```

---

# **Task 4: Repeat Task 2 with SSL**

## **Instructions**:
1. Repeat the process of downloading the image as Task 2.
2. Capture the network traffic with Wireshark.
3. Attempt to reconstruct the image from the sniffed packets.
4. 🎏 Decrypting SSL-secured traffic between the FTP client and server

Decrypting any SSL-encrypted communication requires access to the **SSL/TLS session keys** or the server's **private key**. This is because SSL/TLS encrypts the data using a combination of public-key cryptography and symmetric encryption, which makes the traffic unreadable unless you have access to the keys used during the SSL handshake.


**Using SSL Session Keys for Ephemeral Key Exchanges (ECDHE/DHE)**

If you are using **ephemeral key exchanges (DHE or ECDHE)** (which is more common in modern SSL setups), the server’s private key cannot be used to decrypt traffic. Instead, you need access to the **SSL session keys**, which are temporarily generated during the session.

The easiest way to decrypt the traffic in this case is to log the session keys using an environment variable on the client or server.

- **Steps to Decrypt SSL Traffic Using SSL Session Keys**:

1. **Enable SSL Key Logging in the Client or Server**:
   Modern SSL libraries (like OpenSSL or `ssl` in Python) allow logging the session keys used in the encryption. Here’s how you can do that.

   - Set the `SSLKEYLOGFILE` environment variable on the client-side before running the FTP client.
     ```bash
     export SSLKEYLOGFILE=/path/to/sslkeys.log
     ```
2. **Run the FTP Client**:
   Run the FTP client as usual. This will generate a log file `sslkeys.log` containing the session keys for the encrypted traffic.

3. **Capture the Traffic with Wireshark**:
   - Use Wireshark to capture the encrypted traffic during the FTP session.
   - Save the capture file.

4. **Configure Wireshark to Decrypt SSL Using Session Keys**:
   - Open Wireshark and load the capture file.
   - Go to **"Edit" > "Preferences"**.
   - Expand **"Protocols"** and find **"TLS"**.
   - In the **(Pre)-Master-Secret log filename** field, browse and select the `sslkeys.log` file that was generated.

5. **Analyze the Traffic**:
   - Wireshark should now use the session keys to decrypt the SSL/TLS traffic.
   - You can view the plaintext data, including the user credential and the image.

---

# **Conclusion**
By completing this lab, you will:
- Gain an understanding of TCP framing for more reliable communication.
- Realize the risks of unencrypted data transmission.
- Learn to implement SSL to secure communications and protect sensitive data from interception.


# **Optional: Further improvement**
- Implement all popular **FTP protocol commands**, **FTP status codes** and **modes**.

