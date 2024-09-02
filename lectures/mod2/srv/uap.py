import socket
import select

HOST = '127.0.0.1'
PORT = 9999

# Create a UDP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

# Create a poll object
poller = select.poll()

# Register the server socket with the poller
poller.register(server_socket, select.POLLIN)

print(f"UDP server running on {HOST}:{PORT}")

while True:
    events = poller.poll()

    for fd, flag in events:
        if flag & select.POLLIN:
            data, addr = server_socket.recvfrom(1024)
            print(f"Received {data.decode()} from {addr}")
            server_socket.sendto(data, addr)
