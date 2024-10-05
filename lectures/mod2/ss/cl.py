import ssl
import socket
import logging

# Enable logging to print the SSL handshake
logging.basicConfig(level=logging.DEBUG)

# Create a client socket and wrap it with SSL
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_verify_locations("server.crt")  # The server's certificate to verify

# Enable SSL handshake debugging
context.set_ciphers('ALL')  # Include all available ciphers for debugging purposes

# Connect securely
with context.wrap_socket(client_socket, server_hostname='localhost') as ssock:
    ssock.connect(('localhost', 8080))
    
    # Send and receive data
    ssock.send(b'Hello from SSL client')
    data = ssock.recv(1024).decode('utf-8')
    print(f"Received: {data}")
