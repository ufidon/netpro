import socket

# Aphorisms from the Zen of Python
aphorisms = {
    b'Beautiful is better than?': b'Ugly.',
    b'Explicit is better than?': b'Implicit.',
    b'Simple is better than?': b'Complex.'
}

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server started at {host}:{port}")

        while True:
            connection, client_address = server_socket.accept()
            with connection:
                print(f"Connected by {client_address}")

                while True:
                    # Receive data from the client
                    data = connection.recv(1024)
                    if not data:
                        break
                    
                    print(f"Received: {data}")
                    
                    # Respond to the question if it's recognized
                    if data in aphorisms:
                        response = aphorisms[data]
                        connection.sendall(response)
                        print(f"Sent: {response}")
                    else:
                        print("Unrecognized question.")
                        break

            print(f"Connection with {client_address} closed")

if __name__ == "__main__":
    start_server()
