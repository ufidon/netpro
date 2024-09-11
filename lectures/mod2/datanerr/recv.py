import socket

host = 'github.com'
# Create a socket and connect to a server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, 80))

# Send an HTTP GET request
request = b"GET / HTTP/1.1\r\nHost: " + host + b"\r\n\r\n"
sock.sendall(request)

# Receive the response
response = b''
while True:
    data = sock.recv(4096)  # Receive up to 4096 bytes at a time
    if not data:  # If no more data, break the loop
        break
    response += data

print(response.decode('utf-8'))
sock.close()