import socket
import base64
import hashlib

def generate_websocket_key():
    """Generate a random WebSocket key."""
    return base64.b64encode(hashlib.sha1().digest()).decode().strip()

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    # Perform WebSocket handshake
    websocket_key = generate_websocket_key()
    handshake_request = (
        "GET / HTTP/1.1\r\n"
        "Host: localhost\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Key: " + websocket_key + "\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "\r\n"
    )
    client_socket.sendall(handshake_request.encode())

    # Receive WebSocket handshake response
    response = client_socket.recv(1024).decode()
    print(f"Handshake response:\n{response}")

    # Send a WebSocket frame
    message = "Hello, Server!"
    payload = message.encode()
    payload_length = len(payload)

    frame = bytearray()
    frame.append(0x81)  # Text frame opcode and FIN bit
    if payload_length <= 125:
        frame.append(payload_length)
    elif payload_length <= 65535:
        frame.append(126)
        frame.extend(payload_length.to_bytes(2, byteorder='big'))
    else:
        frame.append(127)
        frame.extend(payload_length.to_bytes(8, byteorder='big'))
    frame.extend(payload)

    client_socket.sendall(frame)

    # Receive and print the echoed message
    response = client_socket.recv(1024)
    print(f"Echoed message: {response[2:].decode()}")  # Skip the WebSocket frame header

    client_socket.close()

client()
