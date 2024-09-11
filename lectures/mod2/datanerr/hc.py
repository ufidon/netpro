import socket

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    # Create an HTTP request
    body = "Hello, Server!"
    request = (
        "POST / HTTP/1.1\r\n"
        "Host: localhost\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        f"{body}"
    )

    # Send the HTTP request
    client_socket.sendall(request.encode())

    # Receive the HTTP response
    response = b''
    while True:
        part = client_socket.recv(1024)
        if not part:
            break
        response += part

    print(f"Response received:\n{response.decode()}")
    client_socket.close()

client()
