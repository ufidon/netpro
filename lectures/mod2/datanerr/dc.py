import socket

DELIMITER = b'\n'

def send_message(sock, message):
    sock.sendall(message + DELIMITER)

def client(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.shutdown(socket.SHUT_RD)
    send_message(sock, b'Beautiful is better than ugly.')
    send_message(sock, b'Explicit is better than implicit.')
    send_message(sock, b'Simple is better than complex.')
    send_message(sock, b'')
    sock.close()

if __name__ == '__main__':
    # Replace the IP address and port as needed
    client(('127.0.0.1', 1060))
