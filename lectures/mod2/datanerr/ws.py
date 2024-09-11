import socket
import base64
import hashlib

def generate_websocket_accept_key(websocket_key):
    """Generate WebSocket accept key for handshake."""
    websocket_guid = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    accept_key = base64.b64encode(hashlib.sha1((websocket_key + websocket_guid).encode()).digest()).decode()
    return accept_key

def handle_client(conn):
    # Perform WebSocket handshake
    request = conn.recv(1024).decode()
    headers = dict(line.split(': ', 1) for line in request.splitlines()[1:] if ': ' in line)
    websocket_key = headers.get('Sec-WebSocket-Key')
    accept_key = generate_websocket_accept_key(websocket_key)

    handshake_response = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Accept: " + accept_key + "\r\n"
        "\r\n"
    )
    conn.sendall(handshake_response.encode())

    while True:
        # Read WebSocket frame
        frame = conn.recv(1024)
        if not frame:
            break

        # Parse WebSocket frame (simplified)
        payload_length = frame[1] & 127
        if payload_length == 126:
            payload_length = int.from_bytes(frame[2:4], byteorder='big')
        elif payload_length == 127:
            payload_length = int.from_bytes(frame[2:10], byteorder='big')
        
        payload = frame[2 + (4 if payload_length == 126 else 10 if payload_length == 127 else 0):]

        print(f"Received message: {payload.decode()}")

        # Echo the received message
        conn.sendall(frame)  # Echo back the frame (simplified)

    conn.close()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)
    print("WebSocket server is listening on port 8080...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        handle_client(conn)

server()
