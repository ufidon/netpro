import socket

MESSAGE_SIZE = 1024

def send_message(sock, message):
    padded_message = message.ljust(MESSAGE_SIZE, '\0')
    sock.sendall(padded_message.encode())

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    
    message = "Hello, fixed-length world!"
    send_message(client_socket, message)
    
    client_socket.close()

client()
