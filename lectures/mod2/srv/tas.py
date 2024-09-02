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

# List of sockets to monitor for incoming connections
sockets_list = [server_socket]

# Dictionary to store connected clients' data
clients = {}

print(f"TCP server running on {HOST}:{PORT}")

while True:
    # Use select to get a list of sockets that are ready for reading
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            # A new client connection
            client_socket, client_address = server_socket.accept()
            client_socket.setblocking(False)
            sockets_list.append(client_socket)
            clients[client_socket] = client_address
            print(f"Accepted new connection from {client_address}")
        else:
            # An existing client has sent a message
            message = notified_socket.recv(1024)
            if not message:
                # Client disconnected
                print(f"Closed connection from {clients[notified_socket]}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
            else:
                # Echo the message back to the client
                print(f"Received message from {clients[notified_socket]}: {message.decode()}")
                notified_socket.send(message)

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
