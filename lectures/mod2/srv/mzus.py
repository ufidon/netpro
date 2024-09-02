import socket
import threading

# Aphorisms from the Zen of Python
aphorisms = {
    b'Beautiful is better than?': b'Ugly.',
    b'Explicit is better than?': b'Implicit.',
    b'Simple is better than?': b'Complex.'
}

def handle_client(data, client_address, server_socket):
    print(f"Received {data} from {client_address}")
    
    # Respond to the question if it's recognized
    if data in aphorisms:
        response = aphorisms[data]
        server_socket.sendto(response, client_address)
        print(f"Sent {response} to {client_address}")
    else:
        print(f"Unrecognized question from {client_address}.")

def start_udp_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"UDP Server started at {host}:{port}")

        while True:
            data, client_address = server_socket.recvfrom(1024)
            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(data, client_address, server_socket))
            client_thread.start()

if __name__ == "__main__":
    start_udp_server()
