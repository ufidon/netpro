import socket
import threading
import time

def listen_to_server(client_socket):
    while True:
        response = client_socket.recv(1024).decode()
        if not response:
            break
        
        print(f"Server says: {response}")
        
def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9999))

    # Start the thread to listen to server messages
    tRec = threading.Thread(target=listen_to_server, args=(client_socket,))
    tRec.start()

    try:
        while True:
            message = input("😄 :> ")

            # Send the message with a newline delimiter
            if message.strip() == '`exit':
                print("quitting...")
                client_socket.sendall((message + '\n').encode())
                time.sleep(1)
                break
            elif message.strip() == '`help':
                print("Show the usages of all commands")
            else:
                client_socket.sendall((message + '\n').encode())

    except:
        pass
    finally:
        client_socket.close()

    tRec.join()
    
if __name__ == "__main__":
    client_program()