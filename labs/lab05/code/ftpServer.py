import socket
import threading
import os

# FTP server settings
FTP_USER = 'user'
FTP_PASS = 'password'
FTP_ROOT = './ftp_root'  # Directory for storing files
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 2121  # FTP control port

def handle_client(client_socket):
    client_socket.send(b'220 Welcome to Simple FTP Server\r\n')

    authenticated = False
    cmd_with_data = ''
    file_path = ''
    filename = ''
    file_exist = False
    data_socket = None  # Will hold the passive data connection socket

    while True:
        # Receive FTP command
        command = client_socket.recv(1024).decode('utf-8').strip()
        if not command:
            break
        print(f"Received command: {command}")
        
        if command.startswith('USER'):
            client_socket.send(b'331 Username okay, need password.\r\n')
        
        elif command.startswith('PASS'):
            if command.split()[1] == FTP_PASS:
                authenticated = True
                client_socket.send(b'230 User logged in, proceed.\r\n')
            else:
                client_socket.send(b'530 Login incorrect.\r\n')
        
        elif authenticated:
            if command.startswith('RETR'):
                filename = command.split()[1]
                file_path = os.path.join(FTP_ROOT, filename)
                
                if os.path.exists(file_path):
                    client_socket.send(b'150 File status okay; about to open data connection.\r\n')
                    file_exist = True
                    cmd_with_data = 'RETR'
                else:
                    client_socket.send(b'550 File not found.\r\n')

            elif command.startswith('STOR'):
                filename = command.split()[1]
                file_path = os.path.join(FTP_ROOT, filename)
                
                client_socket.send(b'150 Ready to receive data.\r\n')
                cmd_with_data = 'STOR'

            elif command.startswith('LIST'):
                client_socket.send(b'150 Here comes the directory listing.\r\n')
                cmd_with_data = 'LIST'
                   

            elif command == 'PASV':
                data_socket, passive_port = enter_passive_mode(client_socket)
                ip, port1, port2 = convert_ip_port(HOST, passive_port)
                response = f'227 Entering Passive Mode ({ip},{port1},{port2})\r\n'
                client_socket.send(response.encode('utf-8'))
                data_conn, addr = data_socket.accept()

                if cmd_with_data == 'LIST':
                    for file in os.listdir(FTP_ROOT):
                        data_conn.send(f"{file}\r\n".encode('utf-8'))
                    data_conn.close()
                    client_socket.send(b'226 Directory send OK.\r\n')

                elif cmd_with_data == 'RETR' and file_exist:
                    with open(file_path, 'rb') as f:
                        data_conn.sendfile(f)
                        data_conn.close()
                    file_exist = False
                    client_socket.send(b'226 Transfer complete.\r\n')

                elif cmd_with_data == 'STOR':
                    with open(file_path, 'wb') as f:
                        while True:
                            data = data_conn.recv(1024)
                            if not data:
                                break
                            f.write(data)
                    data_conn.close()
                    client_socket.send(b'226 Transfer complete.\r\n')

                cmd_with_data = ''

            elif command == 'QUIT':
                client_socket.send(b'221 Goodbye.\r\n')
                client_socket.close()
                break
        
        else:
            client_socket.send(b'530 Not logged in.\r\n')


def enter_passive_mode(control_socket):
    """
    Opens a data connection in passive mode.
    The server binds to an ephemeral port and waits for the client to connect.
    """
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind((HOST, 0))  # Bind to an available port
    data_socket.listen(1)
    
    passive_port = data_socket.getsockname()[1]
    return data_socket, passive_port


def convert_ip_port(ip, port):
    """
    Converts IP and port into the format required by the FTP protocol for PASV response.
    """
    ip_parts = ip.split('.')
    port1 = port // 256
    port2 = port % 256
    return ','.join(ip_parts), port1, port2


def start_ftp_server():
    # Set up root directory
    if not os.path.exists(FTP_ROOT):
        os.makedirs(FTP_ROOT)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"FTP server listening on {HOST}:{PORT}")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        
        # Handle client connection in a new thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_ftp_server()
