import socket

# Aphorisms from the Zen of Python
aphorisms = {
    b'Beautiful is better than?': b'Ugly.',
    b'Explicit is better than?': b'Implicit.',
    b'Simple is better than?': b'Complex.'
}

def start_udp_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"UDP Server started at {host}:{port}")

        while True:
            # Receive data from the client
            data, client_address = server_socket.recvfrom(1024)
            print(f"Received {data} from {client_address}")
            
            # Respond to the question if it's recognized
            if data in aphorisms:
                response = aphorisms[data]
                server_socket.sendto(response, client_address)
                print(f"Sent {response} to {client_address}")
            else:
                print("Unrecognized question.")

if __name__ == "__main__":
    start_udp_server()
