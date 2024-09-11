import socket
import struct

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def receive_message(sock):
    # Read the 4-byte length prefix
    length_prefix = recvall(sock, 4)
    if not length_prefix:
        return None
    message_length = struct.unpack('!I', length_prefix)[0]
    
    # Read the message data based on the length prefix
    return recvall(sock, message_length)

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Server is listening...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")
    
    while True:
        message = receive_message(conn)
        if not message:
            break
        print(f"Received: {message.decode()}")
    
    conn.close()
    server_socket.close()

server()
