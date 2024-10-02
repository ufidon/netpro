import socket
import threading

def listen_to_server(client_socket):
    while True:
        response = client_socket.recv(1024).decode()
        print(f"Server says: {response}")
        
def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9999))

    # Start the thread to listen to server messages
    threading.Thread(target=listen_to_server, args=(client_socket,)).start()

    try:
        while True:
            message = input("😄 :> ")
            # Send the message with a newline delimiter
            client_socket.sendall(message.encode())
    except:
        pass
    finally:
        client_socket.close()

if __name__ == "__main__":
    client_program()