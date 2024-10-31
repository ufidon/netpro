from http.server import HTTPServer, SimpleHTTPRequestHandler
import base64
import functools

# User credentials database (realm: {username: password})
CREDENTIALS = {
    'admin_realm': {'admin': 'adminpass'},
    'user_realm': {'user': 'userpass'}
}

class BasicAuthHandler(SimpleHTTPRequestHandler):
    def do_AUTHHEAD(self, realm):
        self.send_response(401)
        self.send_header('WWW-Authenticate', f'Basic realm="{realm}"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def authenticate(self, realm):
        # Check for Authorization header
        auth_header = self.headers.get('Authorization')
        if not auth_header:
            self.do_AUTHHEAD(realm)
            self.wfile.write(b'No authentication provided')
            return False

        # Decode credentials
        try:
            auth_type, credentials = auth_header.split()
            if auth_type.lower() != 'basic':
                self.do_AUTHHEAD(realm)
                return False

            username, password = base64.b64decode(credentials).decode().split(':', 1)
        except:
            self.do_AUTHHEAD(realm)
            return False

        # Validate credentials for specific realm
        return (CREDENTIALS.get(realm, {}).get(username) == password)

    def do_GET(self):
        # Different routes with different realms
        if self.path.startswith('/admin'):
            if not self.authenticate('admin_realm'):
                return
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Admin Area: Access Granted')

        elif self.path.startswith('/user'):
            if not self.authenticate('user_realm'):
                return
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'User Area: Access Granted')

        else:
            # Public area
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Public Area: No Authentication Required')

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, BasicAuthHandler)
    print(f'Server running on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()