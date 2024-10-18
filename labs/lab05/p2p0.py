import socket
import threading
import os, sys, time


class Node:
    def __init__(self, host, port, shared_dir):
        self.host = host
        self.port = port  # used as node_id
        self.server_socket = None
        self.shared_dir = shared_dir

        # The access to these shared data structures must be protected with a lock in multithreading
        # self.peers = []  # List of connected peers (peer_id=node_id)
        # the keys of self.request_sockets are the list of connected peers
        self.response_sockets = {} # {peer_id: response_socket}
        self.request_sockets = {}  # {peer_id: request_socket}

        self.evExit = threading.Event()
        self.lock = threading.Lock()

    # Function to start the server to listen for incoming connections
    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Node listening on {self.host}:{self.port}")

        while not self.evExit.is_set():
            try:
                response_socket, addr = self.server_socket.accept()
                with self.lock:
                  self.response_sockets[addr[1]] = response_socket
                print(f"Connection established with peer {addr[1]}")
                response_handler = threading.Thread(
                    target=self.handle_peer, args=(response_socket,)
                )
                response_handler.start()
            except TimeoutError as e:
                continue
            except OSError as e:
                if self.evExit.is_set():
                    print("Server socket closed, exiting server...")
                else:
                    print(f"Unexpected OSError: {e}")
                    raise e

        print("Server thread exiting.")
        if self.server_socket:
            self.server_socket.close()  # Ensure the server socket is closed

    # Function to handle requests from connected peers
    def handle_peer(self, response_socket):
        while not self.evExit.is_set():
            pass

    # Function to run the console for interaction
    def console(self):
        while True:
            commands = input(">:").strip().split()

            # === Task 1: describe the usage of each command ===
            if (not commands) or (commands[0] == "help") or (commands[0] == "?"):
                print("show usages of all commands")
            
            # === Task 2: discover active peers and list connected peers ===
            elif commands[0] == "scan": # discover active peers
                pass
            elif commands[0] == "lp":  # list peers
                pass

            # === handle peer connection and disconnection ===
            elif commands[0] == "connect":  # connect peer_id
                pass
            elif commands[0] == "disconnect":  # disconnect peer_id
                pass            

            # === Task 3: search for files on all connected peers ===
            elif commands[0] == "sf":  # search for files
                pass

            # === Task 4: download files ===
            elif commands[0] == "request":  # request filename on peer_id
                pass

            elif commands[0] == "quit":
                self.evExit.set()  # Signal the server to stop
                break
            else:
                print("Unknown command.")

        # After the loop, close the server socket explicitly
        try:
            if self.server_socket:
                self.server_socket.close()  # Close the server socket to interrupt accept()
                time.sleep(0.1)
        except Exception as e:
            print(f"Error closing server socket: {e}")

        # Close all response and request sockets
        for svk, svv in self.response_sockets.items():
            svv.close()
        for sck, scv in self.request_sockets.items():
            scv.close()

        print("All sockets closed. Exiting program.")


# Main execution
if __name__ == "__main__":
    host = "127.0.0.1"  # We use the loopback address for testing
    port = int(input("Enter your port (e.g., 5000, 5001, etc.): "))

    shared_dir = f"./sf{port}"  # Directory containing shared files
    os.makedirs(shared_dir, exist_ok=True)

    peer = Node(host, port, shared_dir)

    # Start the server in a separate thread
    server_thread = threading.Thread(target=peer.start_server, daemon=True)
    server_thread.start()

    # Start the request interaction
    peer.console()

    # Wait for the server thread to finish
    server_thread.join(0.1)
    sys.exit(0)
