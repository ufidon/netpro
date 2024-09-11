import socket

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    # Create an HTTP request with chunked transfer encoding
    request = (
        "POST / HTTP/1.1\r\n"
        "Host: localhost\r\n"
        "Transfer-Encoding: chunked\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        "5\r\nHello\r\n7\r\n, Chunked\r\n0\r\n\r\n"
    )

    # Send the HTTP request
    client_socket.sendall(request.encode())

    # Receive the HTTP response
    response = b''
    while True:
        try:
            part = client_socket.recv(1024)
            if not part:
                break  # No more data to receive
            response += part
        except ConnectionResetError:
            print("Connection closed by server.")
            break

    print(f"Response received:\n{response.decode()}")
    client_socket.close()

client()
