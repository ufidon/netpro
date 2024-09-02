import socket
import threading

# Constants
UDP_IP = "0.0.0.0"  # Listen on all network interfaces
UDP_PORT = 12345    # Port to listen on

def handle_client(data, address, server_socket):
    """Handle incoming data from a client."""
    print(f"Received message from {address}: {data.decode()}")
    response = f"Message received from {address}".encode()
    server_socket.sendto(response, address)

def udp_server():
    """Create and run the UDP server."""
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((UDP_IP, UDP_PORT))
    
    print(f"UDP server listening on {UDP_IP}:{UDP_PORT}")

    while True:
        # Receive data from clients
        data, address = server_socket.recvfrom(1024)
        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(data, address, server_socket))
        client_thread.start()

if __name__ == '__main__':
    udp_server()
