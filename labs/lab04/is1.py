import socketserver

class SimpleTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Connection from {self.client_address}")
        while True:
            data = self.request.recv(1024).decode()
            if not data:
                break
            print(f"Received: {data}")
            self.request.sendall(b"Message received\n")

if __name__ == "__main__":
    with socketserver.TCPServer(("localhost", 9999), SimpleTCPHandler) as server:
        server.serve_forever()