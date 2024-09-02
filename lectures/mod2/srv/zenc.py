import socket

# Predefined questions
questions = [
    b'Beautiful is better than?',
    b'Explicit is better than?',
    b'Simple is better than?'
]

def start_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        for question in questions:
            # Send question to the server
            client_socket.sendall(question)
            print(f"Sent: {question}")
            
            # Receive the response from the server
            response = client_socket.recv(1024)
            print(f"Received: {response}")

        # Close the connection by exiting the loop (implicitly closes socket)

if __name__ == "__main__":
    start_client()
