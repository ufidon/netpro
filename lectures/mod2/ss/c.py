import ssl
import socket
import pprint


# Create a client socket and wrap with SSL
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

pprint.pprint(context.get_ca_certs())
pprint.pprint(context.get_ciphers())

# The server's certificate to verify
context.load_verify_locations("server.crt") 

# Connect securely
with context.wrap_socket(client_socket, server_hostname='localhost') as ssock:
    ssock.connect(('localhost', 8080))
    scert = ssock.getpeercert()
    pprint.pprint(scert)
    
    # Send and receive data
    ssock.send(b'Hello from SSL client')
    data = ssock.recv(1024).decode('utf-8')
    print(f"Received: {data}")
