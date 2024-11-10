from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from werkzeug.security import generate_password_hash, check_password_hash
import base64

# Basic Authentication credentials (for demonstration purposes)
USERNAME = 'admin'
PASSWORD = 'secret'
HASHED_PASSWORD = generate_password_hash(PASSWORD)

def authenticate(request):
    """Check if the request has valid basic authentication credentials."""
    auth = request.headers.get('Authorization')
    
    if auth is None or not auth.startswith('Basic '):
        return False

    # Decode the Base64 encoded credentials
    encoded_credentials = auth.split(' ')[1]
    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    username, password = decoded_credentials.split(':', 1)

    return username == USERNAME and check_password_hash(HASHED_PASSWORD, password)

def application(environ, start_response):
    request = Request(environ)

    # Check for authentication
    if not authenticate(request):
        # Send a 401 Unauthorized response
        response = Response('Unauthorized', status=401)
        response.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
        return response(environ, start_response)

    # Your application logic here
    response = Response('Hello, authenticated user!')
    return response(environ, start_response)

if __name__ == '__main__':
    run_simple('localhost', 8000, application)
