import socket

def client():
  # Connect to the server
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('127.0.0.1', 12345))

  # Aphorisms to send to the server
  aphorisms = {b'Beautiful is better than?': b'Ugly.',
               b'Explicit is better than?': b'Implicit.',
               b'Simple is better than?': b'Complex.'}

  # Send the aphorisms one by one
  for question, _ in aphorisms.items():
    s.sendall(question)
    response = b''
    while True:
      data = s.recv(1024)
      response += data
      if data.endswith(b'.'):
        break
    print(f"Received response: {response.decode('utf-8')}")

  # Close the connection
  s.close()

if __name__ == "__main__":
  client()