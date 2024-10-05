import ssl
import socket
import logging

# Generate the client key and certificate:
# openssl req -new -x509 -days 365 -nodes -out client.crt -keyout client.key

# Enable logging to print the SSL handshake
logging.basicConfig(level=logging.DEBUG)

# Create a client socket and wrap it with SSL
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

# Verify the server's certificate
context.load_verify_locations("server.crt")  
# Set up client-side certificate and key for mutual authentication
# Client cert & key
context.load_cert_chain(certfile="client.crt", keyfile="client.key")  

# Enable SSL handshake debugging
context.set_ciphers('ALL')  # Use all ciphers for debugging purposes

# Connect securely
with context.wrap_socket(client_socket, server_hostname='localhost') as ssock:
    ssock.connect(('localhost', 8080))
    
    # Send and receive data
    ssock.send(b'Hello from SSL client')
    data = ssock.recv(1024).decode('utf-8')
    print(f"Received: {data}")
