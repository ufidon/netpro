import socket, ssl

def client(host, port, cafile=None):
    # 1. Create a TLS context object regarding certificate validation and choice of cipher.
    purpose = ssl.Purpose.SERVER_AUTH  # Verify the server
    context = ssl.create_default_context(purpose, cafile=cafile)
    # If cafile is None, system default CA certificates are used.

    # Create a raw TCP socket and connect to the server
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((host, port))
    print(f'Connected to host {host!r} and port {port}')

    # 2. Wrap the raw socket with SSL
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)

    # 3. Perform communication with SSL-wrapped socket
    try:
        while True:
            data = ssl_sock.recv(1024)
            if not data:
                break
            print(repr(data))
    finally:
        ssl_sock.close()

if __name__ == '__main__':
    host = 'localhost'  # Specify the host or use a command line argument
    port = 8443         # Specify the port or use a command line argument
    cafile = 'server.crt'       # Provide a path to a CA certificate if needed
    
    client(host, port, cafile)