import socket
import struct

def send_large_message(sock, address, message, chunk_size=1024):
    sequence_number = 0
    header_struct = struct.Struct('!I')  # 4-byte sequence number

    for i in range(0, len(message), chunk_size):
        chunk = message[i:i + chunk_size]
        header = header_struct.pack(sequence_number)
        sock.sendto(header + chunk, address)
        sequence_number += 1

    # Send an empty chunk with a special sequence number to indicate the end
    sock.sendto(header_struct.pack(sequence_number), address)

# Example usage
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = b'This is a large message that will be sent in chunks.' * 100
send_large_message(sock, ('127.0.0.1', 1060), message)
