import socket

DELIMITER = b'\n'

def recvall(sock):
    data = b''
    while True:
        # change buffersize from 20 to 1024, rerun the program 
        block = sock.recv(20)
        if not block:
            break
        data += block
        if data.endswith(DELIMITER):
            break
    return data.rstrip(DELIMITER)

def server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)
    print('Listening at', sock.getsockname())
    sc, sockname = sock.accept()
    print('Accepted connection from', sockname)
    sc.shutdown(socket.SHUT_WR)
    while True:
        message = recvall(sc)
        if not message:
            break
        for m in message.split(DELIMITER):
          print('Received message:', repr(m))
    sc.close()
    sock.close()

if __name__ == '__main__':
    # Replace the IP address and port as needed
    server(('127.0.0.1', 1060))
