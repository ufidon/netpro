import socket
import threading
import os

HOST = '127.0.0.1'  # Server IP
PORT = 2121           # FTP control port
control_socket = None  # Global control socket for use by the console thread

def ftp_command(command):
    """
    Send an FTP command to the server and return its response.
    """
    control_socket.send(f"{command}\r\n".encode('utf-8'))
    response = control_socket.recv(1024).decode('utf-8').strip()
    print(f"Server response: {response}")
    return response

def parse_pasv_response(response):
    """
    Parse the PASV response to extract the IP and port to connect to for the data connection.
    """
    start = response.find('(') + 1
    end = response.find(')')
    numbers = response[start:end].split(',')
    ip_address = '.'.join(numbers[:4])
    port = int(numbers[4]) * 256 + int(numbers[5])
    return ip_address, port

def data_connection_pasv():
    """
    Request a passive mode connection (PASV) and open a data connection.
    """
    response = ftp_command("PASV")
    ip, port = parse_pasv_response(response)
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((ip, port))
    return data_socket

def ftp_retrieve(filename):
    response = ftp_command(f"RETR {filename}")
    if response[:3] == '150':
      data_conn = data_connection_pasv()
      with open(filename, 'wb') as f:
          while True:
              data = data_conn.recv(1024)
              if not data:
                  break
              f.write(data)
      data_conn.close()
      print(f"Downloaded {filename}")

      response = control_socket.recv(1024).decode('utf-8').strip()
      print(f"Server response: {response}")

def ftp_store(filename):
    ftp_command(f"STOR {filename}")
    data_conn = data_connection_pasv()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            data_conn.sendall(data)
    data_conn.close()
    print(f"Uploaded {filename}")

    response = control_socket.recv(1024).decode('utf-8').strip()
    print(f"Server response: {response}")

def ftp_list():
    ftp_command("LIST")
    data_conn = data_connection_pasv()
    print("Directory listing:")
    while True:
        data = data_conn.recv(1024)
        if not data:
            break
        print(data.decode('utf-8'))
    data_conn.close()

    response = control_socket.recv(1024).decode('utf-8').strip()
    print(f"Server response: {response}")

def ftp_quit():
    ftp_command("QUIT")
    control_socket.close()

def console_thread():
    """
    This thread allows user interaction via the console.
    The user can type FTP commands such as LIST, RETR, STOR, QUIT.
    """
    while True:
        command = input("ftp> ").strip()

        if command.startswith('LIST'):
            ftp_list()

        elif command.startswith('RETR'):
            filename = command.split()[1]
            ftp_retrieve(filename)

        elif command.startswith('STOR'):
            filename = command.split()[1]
            ftp_store(filename)

        elif command == 'QUIT':
            ftp_quit()
            print("Connection closed. Exiting.")
            break

        else:
            print("Invalid command. Available commands: LIST, RETR <filename>, STOR <filename>, QUIT")

def main():
    global control_socket  # Declare the control_socket as global so both threads can use it

    # Create control socket and connect to the FTP server
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_socket.connect((HOST, PORT))
    response = control_socket.recv(1024).decode('utf-8').strip()
    print(f"Server: {response}")

    # Login to the FTP server
    ftp_command("USER user")
    ftp_command("PASS password")

    # Start console thread for user interaction
    console = threading.Thread(target=console_thread)
    console.start()

    # Wait for the console thread to finish
    console.join()

if __name__ == "__main__":
    main()
