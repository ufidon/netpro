import socket

def handle_client(conn):
    # Read the HTTP request headers
    headers = b''
    while b'\r\n\r\n' not in headers:
        headers += conn.recv(1)

    # Parse headers
    headers = headers.decode()
    print(f"Headers received:\n{headers}")

    # Read the body chunk by chunk
    body = ''
    while True:
        # Read chunk size (in hex)
        chunk_size_line = b''
        while b'\r\n' not in chunk_size_line:
            chunk_size_line += conn.recv(1)

        # Convert chunk size from hex to integer
        try:
            chunk_size = int(chunk_size_line.decode().strip(), 16)
        except ValueError:
            break

        if chunk_size == 0:
            # Final chunk (size 0) marks the end of the body
            conn.recv(2)  # Consume the trailing \r\n after the last chunk
            break

        # Read the chunk data (until chunk_size)
        chunk_data = b''
        while len(chunk_data) < chunk_size:
            chunk_data += conn.recv(chunk_size - len(chunk_data))

        body += chunk_data.decode()

        # Read the trailing \r\n after each chunk
        conn.recv(2)

    print(f"Body received (chunked): {body}")

    # Send HTTP response
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Content-Length: 13\r\n"
        "\r\n"
        "Hello, Client!"
    )
    conn.sendall(response.encode())
    
    # Shutdown the connection gracefully
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)
    print("Server is listening on port 8080...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        handle_client(conn)

server()
