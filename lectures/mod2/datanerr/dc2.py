import socket

def send_message(sock, message):
    message += '\n'
    sock.sendall(message.encode())

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    
    message = "Hello, delimiter-based world!"
    send_message(client_socket, message)
    
    client_socket.close()

client()
