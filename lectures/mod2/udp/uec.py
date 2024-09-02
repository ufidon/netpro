import socket

def start_udp_echo_client(host='127.0.0.1', port=65432, message='Hello, Server!'):
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # Send a message to the server
        client_socket.sendto(message.encode(), (host, port))
        print(f'Sent: {message}')
        
        # Receive the echoed message from the server
        data, _ = client_socket.recvfrom(1024)
        print(f'Received: {data.decode()}')

if __name__ == "__main__":
    start_udp_echo_client()
