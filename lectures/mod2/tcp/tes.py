import socket

def start_tcp_echo_server(host='127.0.0.1', port=65432):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the address
        server_socket.bind((host, port))
        print(f'Server started on {host}:{port}')
        
        # Listen for incoming connections
        server_socket.listen()
        print('Waiting for a connection...')
        
        # Accept a connection
        conn, addr = server_socket.accept()
        with conn:
            print(f'Connected by {addr}')
            while True:
                # Receive data from the client
                data = conn.recv(1024)
                if not data:
                    break
                print(f'Received: {data.decode()}')
                
                # Echo the data back to the client
                conn.sendall(data)
                print(f'Sent: {data.decode()}')

if __name__ == "__main__":
    start_tcp_echo_server()
