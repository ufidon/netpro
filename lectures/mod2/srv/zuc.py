import socket

# Predefined questions
questions = [
    b'Beautiful is better than?',
    b'Explicit is better than?',
    b'Simple is better than?'
]

def start_udp_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        
        for question in questions:
            # Send question to the server
            client_socket.sendto(question, (host, port))
            print(f"Sent: {question}")
            
            # Receive the response from the server
            data, _ = client_socket.recvfrom(1024)
            print(f"Received: {data}")

if __name__ == "__main__":
    start_udp_client()
