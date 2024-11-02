import socket, sys
import urllib

def read_http_request(sock):
    # Read headers until we find the empty line indicating the end of headers
    request = b""
    while b"\r\n\r\n" not in request:
        n = sock.recv(1)
        request += n
        if not n:
            return "", "", True

    print("\n============Raw request==========")
    print(request)

    headers, body = request.split(b"\r\n\r\n", 1)
    print("\n============Parsed request==========")
    print("Request Headers:\n", headers.decode())
    
    # Parse headers to find Content-Length or Transfer-Encoding
    headers_str = headers.decode()
    content_length = None
    is_chunked = False
    connection_close = False

    for line in headers_str.split("\r\n"):
        if line.lower().startswith("content-length"):
            content_length = int(line.split(":")[1].strip())
        elif line.lower().startswith("transfer-encoding") and "chunked" in line.lower():
            is_chunked = True
        elif line.lower().startswith("connection") and "close" in line.lower():
            connection_close = True

    if content_length is not None:
        # If Content-Length is found, read the exact amount of remaining bytes
        while len(body) < content_length:
            body += sock.recv(1024)
    elif is_chunked:
        # If Transfer-Encoding is chunked, handle it accordingly
        body += read_chunked_request(sock)

    return headers_str, body.decode(), connection_close

def read_chunked_request(sock):
    request = b""
    while True:
        chunk_size_str = b""

        # Read chunk size in hexadecimal
        while b"\r\n" not in chunk_size_str:
            chunk_size_str += sock.recv(1)
        chunk_size = int(chunk_size_str.strip(), 16)

        # End of the message when chunk size is 0
        if chunk_size == 0:
            break

        # Read the chunk data
        chunk_data = b''
        while len(chunk_data) < chunk_size:
          chunk_data += sock.recv(1)

        request += chunk_data

        # Read the trailing \r\n
        sock.recv(2) 

    return request

def handle_client_connection(client_socket):
    try:
        while True:
            # Read the HTTP request from the client
            headers, body, connection_close = read_http_request(client_socket)
            if not headers:
                break
            
            # favorite icon
            method, _ = headers.split('\r\n', 1)
            # for simplicity here
            if 'favicon.ico' in method:
              response = """
HTTP/1.1 404 Not Found
Content-Type: text/plain
Content-Length: 0
Connection: keep-alive\r\n\r\n
"""
              client_socket.sendall(response.encode())
              continue

            # Home page: index.html

                
            # For all other requests, 
            # Prepare a response showing the details of the request
            response_body = "<h1>Request Details</h1>"
            response_body += "<h2>Headers:</h2><pre>{}</pre>".format(headers.replace('\r\n', '<br/>'))
            response_body += "<h2>Body:</h2><pre>{}</pre>".format(body if body else "No body received.")

            response_headers = "HTTP/1.1 200 OK\r\n"
            response_headers += "Content-Type: text/html\r\n"
            response_headers += "Content-Length: {}\r\n".format(len(response_body))
            response_headers += "Connection: keep-alive\r\n\r\n"

            # Send the response back to the client
            client_socket.sendall(response_headers.encode() + response_body.encode())

            # If the request indicated to close the connection, break the loop
            if connection_close:
                print("Connection will be closed as per the request.")
                break
    except:
        print("\n🔗☠️ Connection closed.\n")
        client_socket.close()

def main():
    host = '127.0.0.1'  # Localhost
    port = int(sys.argv[1]) if len(sys.argv)>1 else 8080           # Port to listen on

    # Create a socket and bind it to the specified host and port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        server_socket.bind((host, port))
        server_socket.listen(5)  # Listen for incoming connections
        print(f"Listening on http://{host}:{port}")

        while True:
            # Accept a new client connection
            client_socket, addr = server_socket.accept()
            print(f"\n🕸️Accepted connection from {addr}")
            handle_client_connection(client_socket)

if __name__ == "__main__":
    main()
