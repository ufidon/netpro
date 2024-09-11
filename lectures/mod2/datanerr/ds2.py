import socket

def receive_message(sock):
    buffer = b''
    while True:
        data = sock.recv(1)
        if not data or data == b'\n':
            break
        buffer += data
    return buffer.decode()

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
