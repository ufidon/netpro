import socket
import struct

def send_message(sock, message):
    message_length = len(message)
    length_prefix = struct.pack('!I', message_length)
    sock.sendall(length_prefix + message)

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    
    message = b'Hello, length-prefixed world!'
    send_message(client_socket, message)
    
    client_socket.close()

client()
