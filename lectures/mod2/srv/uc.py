import socket

# Constants
UDP_IP = "127.0.0.1"  # Server IP address
UDP_PORT = 12345      # Server port

def udp_client(message):
    """Send a message to the UDP server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(message.encode(), (UDP_IP, UDP_PORT))
    data, _ = client_socket.recvfrom(1024)
    print(f"Received response from server: {data.decode()}")

if __name__ == '__main__':
    udp_client("Hello, UDP Server!")
