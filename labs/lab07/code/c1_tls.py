import socket
import ssl, sys

def read_http_message(sock):
    # Read headers until we find the empty line indicating the end of headers
    response = b""
    while b"\r\n\r\n" not in response:
        response += sock.recv(1)

    headers, body = response.split(b"\r\n\r\n", 1)
    # print(headers.decode())
    
    # Parse headers to find Content-Length or Transfer-Encoding
    headers_str = headers.decode()
    content_length = None
    is_chunked = False

    for line in headers_str.split("\r\n"):
        if line.lower().startswith("content-length"):
            content_length = int(line.split(":")[1].strip())
        elif line.lower().startswith("transfer-encoding") and "chunked" in line.lower():
            is_chunked = True

    if content_length is not None:
        # If Content-Length is found, read the exact amount of remaining bytes
        while len(body) < content_length:
            body += sock.recv(1024)
    elif is_chunked:
        # If Transfer-Encoding is chunked, handle it accordingly
        body += read_chunked_response(sock)
    else:
        # If neither is present, read until the connection is closed
        body += read_until_close(sock)

    return headers_str, body.decode()

def read_chunked_response(sock):
    response = b""
    while True:
        chunk_size_str = b""
 
        # Read chunk size in hexadecimal
        while True:
            chunk_size_str += sock.recv(1)
            if chunk_size_str.endswith(b'\r\n'):
                break
        chunk_size = int(chunk_size_str.strip(), 16)  # Remove the \r\n and convert

        # End of the message when chunk size is 0
        if chunk_size == 0:
            break

        # Read the chunk data
        chunk_data = b''
        while len(chunk_data) < chunk_size:
          chunk_data += sock.recv(1)

        response += chunk_data

        # Read the trailing \r\n
        sock.recv(2) 

    return response

def read_until_close(sock):
    response = b""
    while True:
        chunk = sock.recv(1024)
        if not chunk:  # Server closed the connection
            break
        response += chunk
    return response

def main():
    host = sys.argv[1] if len(sys.argv)>1 else 'www.google.com'
    port = int(sys.argv[2]) if len(sys.argv)>2 else 443  # HTTPS uses port 443

    # Create a socket and wrap it with SSL
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Establish a connection
        sock.connect((host, port))
        
        # Wrap the socket with SSL
        context = ssl.create_default_context()
        context.load_verify_locations('server.crt')
        secure_sock = context.wrap_socket(sock, server_hostname=host)

        # Send a simple HTTP GET request
        request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        secure_sock.sendall(request.encode())

        # Read the complete HTTP message
        headers, body = read_http_message(secure_sock)

        # Print headers and body
        print("HTTP Headers:\n", headers)
        print("\nHTTP Body:\n", body)

if __name__ == "__main__":
    main()