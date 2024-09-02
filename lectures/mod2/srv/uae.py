import socket
import select

HOST = '127.0.0.1'
PORT = 9999

# Create a UDP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

# Create an epoll object
epoll = select.epoll()

# Register the server socket with epoll
epoll.register(server_socket.fileno(), select.EPOLLIN)

print(f"UDP server running on {HOST}:{PORT}")

try:
    while True:
        events = epoll.poll()

        for fd, event in events:
            if event & select.EPOLLIN:
                data, addr = server_socket.recvfrom(1024)
                print(f"Received {data.decode()} from {addr}")
                server_socket.sendto(data, addr)
finally:
    epoll.unregister(server_socket.fileno())
    epoll.close()
    server_socket.close()
