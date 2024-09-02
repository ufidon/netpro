import socket
import threading

# Aphorisms from the Zen of Python
aphorisms = {
    b'Beautiful is better than?': b'Ugly.',
    b'Explicit is better than?': b'Implicit.',
    b'Simple is better than?': b'Complex.'
}

def handle_client(connection, client_address):
    print(f"Connected by {client_address}")
    with connection:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            
            print(f"Received: {data} from {client_address}")
            
            # Respond to the question if it's recognized
            if data in aphorisms:
                response = aphorisms[data]
                connection.sendall(response)
                print(f"Sent: {response} to {client_address}")
            else:
                print(f"Unrecognized question from {client_address}.")
                break

    print(f"Connection with {client_address} closed")

def start_tcp_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"TCP Server started at {host}:{port}")

        while True:
            connection, client_address = server_socket.accept()
            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
            client_thread.start()

if __name__ == "__main__":
    start_tcp_server()
