import socketserver
import threading

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class SimpleTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Connection from {self.client_address}")
        while True:
            data = self.request.recv(1024).decode()
            if not data:
                break
            print(f"Received: {data}")
            self.request.sendall(b"Message received")

if __name__ == "__main__":
    with ThreadedTCPServer(("localhost", 9999), SimpleTCPHandler) as server:
        server.serve_forever()