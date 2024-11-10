import hashlib
import os
from flask import Flask, request, jsonify, Response
import logging
import time

app = Flask(__name__)

# In-memory user database
users = {
    "user1": "password123",
    "admin": "adminpass"
}

# Set up logging
logging.basicConfig(level=logging.INFO)

def generate_nonce():
    """Generates a unique nonce."""
    return hashlib.md5(os.urandom(16)).hexdigest()

def generate_ha1(username, password, realm="example.com"):
    """Generate HA1 hash using MD5 of 'username:realm:password'."""
    return hashlib.md5(f"{username}:{realm}:{password}".encode()).hexdigest()

def generate_ha2(method, uri):
    """Generate HA2 hash using MD5 of 'method:uri'."""
    return hashlib.md5(f"{method}:{uri}".encode()).hexdigest()

def generate_response_hash(ha1, ha2, nonce, nc, cnonce, qop="auth"):
    """Generate the final response hash."""
    return hashlib.md5(f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}".encode()).hexdigest()

@app.before_request
def log_request_info():
    logging.info(f"Request Method: {request.method}")
    logging.info(f"Request URL: {request.url}")
    logging.info(f"Request Headers: {request.headers}")

@app.after_request
def log_response_info(response):
    logging.info(f"Response Status: {response.status}")
    logging.info(f"Response Headers: {response.headers}")
    return response

def check_digest_auth(auth_header):
    """Process the Digest Auth header and validate the request."""
    if not auth_header:
        return False, None
    
    # Parse the Digest Auth header
    auth_parts = {k.strip(): v.strip('"') for k, v in 
                  (item.split('=') for item in auth_header.replace('Digest ', '').split(', '))}
    
    username = auth_parts.get("username")
    if username not in users:
        return False, None
    
    # Retrieve stored password and create HA1
    password = users[username]
    ha1 = generate_ha1(username, password)
    ha2 = generate_ha2(request.method, auth_parts.get("uri"))
    response_hash = generate_response_hash(
        ha1=ha1,
        ha2=ha2,
        nonce=auth_parts.get("nonce"),
        nc=auth_parts.get("nc"),
        cnonce=auth_parts.get("cnonce"),
        qop=auth_parts.get("qop")
    )

    return response_hash == auth_parts.get("response"), username

def digest_authenticate():
    """Send a 401 response with a Digest authentication challenge."""
    nonce = generate_nonce()
    response = Response(status=401)
    response.headers["WWW-Authenticate"] = (
        f'Digest realm="example.com",'
        f'nonce="{nonce}",'
        f'qop="auth",'
        f'algorithm="MD5"'
    )
    return response

@app.route('/secure-data')
def secure_data():
    auth_header = request.headers.get("Authorization")
    is_authenticated, username = check_digest_auth(auth_header)
    
    if not is_authenticated:
        return digest_authenticate()
    
    return jsonify(message=f"Hello, {username}! This is secured data.")

if __name__ == '__main__':
    app.run(debug=True)
