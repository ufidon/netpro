import ssl
import socket
import logging

# Generate the server key and certificate:
# openssl req -new -x509 -days 365 -nodes -out server.crt -keyout server.key

# Enable logging to print the SSL handshake
logging.basicConfig(level=logging.DEBUG)

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(5)

# Wrap the socket with SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# Set SSL logging level to debug
context.set_ciphers('ALL')  # Include all available ciphers for debugging purposes
context.set_servername_callback(lambda s, c, h : print(f'SSL Handshake with client: {h}'))

print("Waiting for client...")
with context.wrap_socket(server_socket, server_side=True) as ssock:
    conn, addr = ssock.accept()
    print(f"Connection from {addr}")
    
    # Receive and send data
    data = conn.recv(1024).decode('utf-8')
    print(f"Received: {data}")
    conn.send(b'Hello from SSL server')

    conn.close()
