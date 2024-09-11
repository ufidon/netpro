import socket
import struct

def receive_large_message(sock, bufsize=1028):  # 1024 + 4 bytes for header
    header_struct = struct.Struct('!I')
    chunks = {}
    expected_seq = 0

    while True:
        data, addr = sock.recvfrom(bufsize)
        sequence_number = header_struct.unpack(data[:header_struct.size])[0]
        chunk = data[header_struct.size:]

        if not chunk:  # End of message
            break

        chunks[sequence_number] = chunk

        # Optionally, handle missing or out-of-order chunks here
        expected_seq += 1

    # Reassemble the message in the correct order
    message = b''.join(chunks[i] for i in range(expected_seq))
    return message, addr

# Example usage
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 1060))
message, sender_addr = receive_large_message(sock)
print('Received message:', message.decode())
