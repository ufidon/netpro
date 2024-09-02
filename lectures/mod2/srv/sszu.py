import socketserver

# Aphorisms from the Zen of Python
aphorisms = {
    b'Beautiful is better than?': b'Ugly.',
    b'Explicit is better than?': b'Implicit.',
    b'Simple is better than?': b'Complex.'
}

class UDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        print(f"Received {data} from {self.client_address}")
        
        # Respond to the question if it's recognized
        if data in aphorisms:
            response = aphorisms[data]
            socket.sendto(response, self.client_address)
            print(f"Sent {response} to {self.client_address}")
        else:
            print(f"Unrecognized question from {self.client_address}.")

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 65432
    with ThreadedUDPServer((HOST, PORT), UDPRequestHandler) as server:
        print(f"UDP Server started at {HOST}:{PORT}")
        server.serve_forever()
