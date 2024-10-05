import socket, ssl

def server(host, port, certfile, cafile=None):
    # 1. Create a TLS context object
    purpose = ssl.Purpose.CLIENT_AUTH  # Accept client connections
    context = ssl.create_default_context(purpose, cafile=cafile)
    context.load_cert_chain(certfile)  # Load server's certificate and private key

    # Create a TCP listener socket
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((host, port))
    listener.listen(1)
    print(f'Listening at interface {host!r} and port {port}')
    
    raw_sock, address = listener.accept()
    print(f'Connection from host {address[0]!r} and port {address[1]}')
    
    # 2. Wrap the accepted raw socket with SSL
    ssl_sock = context.wrap_socket(raw_sock, server_side=True)

    # 3. Perform communication with the client
    try:
        ssl_sock.sendall('Simple is better than complex.'.encode('ascii'))
    finally:
        ssl_sock.close()

if __name__ == '__main__':
    host = 'localhost'  # Specify the host or use a command line argument
    port = 8443         # Specify the port or use a command line argument
    certfile = 'server.pem'  # Path to your server certificate
    cafile = None       # Provide a path to a CA certificate if needed
    
    server(host, port, certfile, cafile)