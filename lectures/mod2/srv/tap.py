import socket
import select

HOST = '127.0.0.1'
PORT = 8888

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

# Set the server socket to non-blocking mode
server_socket.setblocking(False)

# Create a poll object
poller = select.poll()

# Register the server socket with the poller for incoming connections
poller.register(server_socket, select.POLLIN)

# Dictionary to store connected clients' data
clients = {}

print(f"TCP server running on {HOST}:{PORT}")

while True:
    # Poll sockets for I/O events
    events = poller.poll()

    for fd, flag in events:
        if fd == server_socket.fileno():
            # A new client connection
            client_socket, client_address = server_socket.accept()
            client_socket.setblocking(False)
            poller.register(client_socket, select.POLLIN)
            clients[client_socket.fileno()] = client_socket
            print(f"Accepted new connection from {client_address}")
        else:
            client_socket = clients[fd]
            if flag & select.POLLIN:
                # An existing client has sent a message
                message = client_socket.recv(1024)
                if not message:
                    # Client disconnected
                    print(f"Closed connection from {client_socket.getpeername()}")
                    poller.unregister(fd)
                    client_socket.close()
                    del clients[fd]
                else:
                    # Echo the message back to the client
                    print(f"Received message from {client_socket.getpeername()}: {message.decode()}")
                    client_socket.send(message)
