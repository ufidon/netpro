import socket

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9999))

    while True:
        message = input("😄 :> ")
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode()
        print(f"Server says: {response}")

if __name__ == "__main__":
    client_program()