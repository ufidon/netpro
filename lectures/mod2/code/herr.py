import sys
import socket

def main():
  # Get user input for host, port, and filename (assuming all are required)
  host = input("Enter host: ")
  port = int(input("Enter port: "))
  filename = input("Enter filename: ")

  # Create socket
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  except socket.error as e:
    print("Error creating socket:", e)
    sys.exit(1)

  # Connect to host and port
  try:
    s.connect((host, port))
  except socket.gaierror as e:
    print("Address-related error connecting to server:", e)
    sys.exit(1)
  except socket.error as e:
    print("Connection error:", e)
    sys.exit(1)

  # Send data (HTTP GET request)
  try:
    msg = f"GET {filename} HTTP/1.0\r\n\r\n"
    s.sendall(msg.encode('utf-8'))
  except socket.error as e:
    print("Error sending data:", e)
    sys.exit(1)

  # Receive data from server
  while True:
    try:
      buf = s.recv(2048)
    except socket.error as e:
      print("Error receiving data:", e)
      sys.exit(1)
    if not len(buf):
      break
    sys.stdout.write(buf.decode('utf-8'))

  # Close socket
  s.close()

if __name__ == "__main__":
  main()