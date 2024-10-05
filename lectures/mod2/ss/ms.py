import ssl
import socket
import logging

# Generate the server key and certificate:
# openssl req -new -x509 -days 365 -nodes -out server.crt -keyout server.key

# Enable logging to print the SSL handshake
logging.basicConfig(level=logging.DEBUG)

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
server_socket.bind(('localhost', 8080))
server_socket.listen(5)

# Wrap the socket with SSL and set up mutual TLS (mTLS)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

# Server cert & key
context.load_cert_chain(certfile="server.crt", keyfile="server.key")  
# Configure server to verify client certificates
context.verify_mode = ssl.CERT_REQUIRED  # Require client certificate
context.load_verify_locations("client.crt")  # Trusted client certificate authority (CA)

# Set SSL logging level to debug
context.set_ciphers('ALL')  # Use all ciphers for debugging purposes
context.set_servername_callback(lambda s, c, h: print(f'SSL Handshake with client: {h}'))

print("Waiting for client...")
with context.wrap_socket(server_socket, server_side=True) as ssock:
    conn, addr = ssock.accept()
    print(f"Connection from {addr}")

    # Get client certificate and verify
    client_cert = conn.getpeercert()
    if client_cert:
        print("Client Certificate:", client_cert)
    else:
        print("No client certificate provided.")

    # Receive and send data
    data = conn.recv(1024).decode('utf-8')
    print(f"Received: {data}")
    conn.send(b'Hello from SSL server')

    conn.close()
