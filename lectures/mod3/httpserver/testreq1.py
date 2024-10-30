from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._print_request_details()
        self._send_response()

    def do_POST(self):
        self._print_request_details()
        self._send_response()

    def do_PUT(self):
        self._print_request_details()
        self._send_response()

    def do_DELETE(self):
        self._print_request_details()
        self._send_response()

    def do_HEAD(self):
        self._print_request_details()
        self._send_response()

    def do_OPTIONS(self):
        self._print_request_details()
        self._send_response()

    def _print_request_details(self):
        # Print request method and path
        print(f"Received {self.command} request for {self.path}")
        
        # Print headers
        print("Headers:")
        for key, value in self.headers.items():
            print(f"  {key}: {value}")
        
        # Print body if available
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            print("Body:")
            print(body.decode("utf-8"))
        print("-" * 40)

    def _send_response(self):
        # Send a simple 200 OK response
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Request received and logged.")

# Define server details
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
