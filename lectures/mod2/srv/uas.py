import socket
import select

HOST = '127.0.0.1'
PORT = 9999

# Create a UDP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"UDP server running on {HOST}:{PORT}")

while True:
    # Use select to get a list of sockets that are ready for reading
    read_sockets, _, _ = select.select([server_socket], [], [])

    for notified_socket in read_sockets:
        data, addr = notified_socket.recvfrom(1024)
        print(f"Received {data.decode()} from {addr}")
        notified_socket.sendto(data, addr)
