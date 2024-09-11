import socket

def handle_client(conn):
    # Read the HTTP request headers
    headers = b''
    while b'\r\n\r\n' not in headers:
        headers += conn.recv(1)

    # Parse headers
    headers = headers.decode()
    print(f"Headers received:\n{headers}")

    # Extract Content-Length
    content_length = 0
    for line in headers.splitlines():
        if line.startswith("Content-Length"):
            content_length = int(line.split(":")[1].strip())
    
    # Read the body based on Content-Length
    body = conn.recv(content_length).decode()
    print(f"Body received: {body}")

    # Send HTTP response
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Content-Length: 13\r\n"
        "\r\n"
        "Hello, Client!"
    )
    conn.sendall(response.encode())
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
