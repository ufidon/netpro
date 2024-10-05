import ssl
import socket
import pprint

# Generate the server key and certificate:
# openssl req -new -x509 -days 365 -nodes -out server.crt -keyout server.key

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
server_socket.bind(('localhost', 8080))
server_socket.listen(5)

# Wrap the socket with SSL
context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH, cafile=None)
# cat server.crt server.key > server.pem
context.load_cert_chain(certfile="server.pem")

pprint.pprint(context.get_ca_certs())

# Accept client connections securely
print("Waiting for client...")
with context.wrap_socket(server_socket, server_side=True) as ssock:
    print(f'{ssock.version()}')
    conn, addr = ssock.accept()
    print(f"Connection from {addr}")
    
    # Receive and send data
    data = conn.recv(1024).decode('utf-8')
    print(f"Received: {data}")
    conn.send(b'Hello from SSL server')

    conn.close()
