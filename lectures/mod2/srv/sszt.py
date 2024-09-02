import socketserver

# Aphorisms from the Zen of Python
aphorisms = {
    b'Beautiful is better than?': b'Ugly.',
    b'Explicit is better than?': b'Implicit.',
    b'Simple is better than?': b'Complex.'
}

class TCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Connected by {self.client_address}")
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            
            print(f"Received: {data} from {self.client_address}")
            
            # Respond to the question if it's recognized
            if data in aphorisms:
                response = aphorisms[data]
                self.request.sendall(response)
                print(f"Sent: {response} to {self.client_address}")
            else:
                print(f"Unrecognized question from {self.client_address}.")
                break

        print(f"Connection with {self.client_address} closed")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 65432
    with ThreadedTCPServer((HOST, PORT), TCPRequestHandler) as server:
        print(f"TCP Server started at {HOST}:{PORT}")
        server.serve_forever()
