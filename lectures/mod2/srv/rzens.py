import socket

def server():
  # Create a socket and bind it to a port
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('127.0.0.1', 12345))
  s.listen()

  # Aphorisms to respond to
  aphorisms = {b'Beautiful is better than?': b'Ugly.',
               b'Explicit is better than?': b'Implicit.',
               b'Simple is better than?': b'Complex.'}

  # Handle incoming connections
  while True:
    conn, addr = s.accept()
    print(f"Connected by {addr}")

    while True:
      data = conn.recv(1024)
      if not data:
        break

      if data in aphorisms:
        answer = aphorisms[data]
        conn.sendall(answer)

    conn.close()
    print("Connection closed")

if __name__ == "__main__":
  server()