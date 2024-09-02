import socket

def start_udp_echo_server(host='127.0.0.1', port=65432):
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # Bind the socket to the address
        server_socket.bind((host, port))
        print(f'Server started on {host}:{port}')
        
        while True:
            # Receive data from the client
            data, addr = server_socket.recvfrom(1024)
            print(f'Received {data.decode()} from {addr}')
            
            # Echo the data back to the client
            server_socket.sendto(data, addr)
            print(f'Sent {data.decode()} back to {addr}')

if __name__ == "__main__":
    start_udp_echo_server()
