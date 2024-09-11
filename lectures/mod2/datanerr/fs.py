import socket

MESSAGE_SIZE = 1024

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def receive_message(sock):
    message = recvall(sock, MESSAGE_SIZE)
    return message.decode().rstrip('\0') if message else None

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
        print(f"Received: {message}")
    
    conn.close()
    server_socket.close()

server()
