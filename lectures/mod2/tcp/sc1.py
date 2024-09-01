import socket
import struct
import time

def sntp_request(host='pool.ntp.org', port=123):
    # Create a socket and set the timeout
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(5)

    # SNTP packet (48 bytes) - 0x1B is the NTP version and mode (client mode, version 3)
    # packet = b'\x1b' + 47 * b'\0'
    packet = b'\x23' + 47 * b'\0'

    # Send the packet to the SNTP server
    client.sendto(packet, (host, port))

    # Receive the response and get the time
    data, _ = client.recvfrom(1024)
    
    if data:
        return parse_sntp_response(data)
    else:
        raise Exception("No data received from SNTP server")

def parse_sntp_response(data):
    # Unpack the first 48 bytes of the SNTP packet
    unpacked = struct.unpack('!12I', data[0:48])

    # Extract the transmit timestamp (seconds since epoch)
    transmit_timestamp = unpacked[10] - 2208988800  # Convert NTP time to UNIX time (subtract 70 years in seconds)
    
    # Convert to human-readable format
    time_received = time.ctime(transmit_timestamp)
    
    return time_received

# Main function to request time from SNTP server
if __name__ == '__main__':
    try:
        print("Requesting time from SNTP server...")
        time_received = sntp_request()
        print("Time received from SNTP server:", time_received)
    except Exception as e:
        print("Failed to retrieve time:", e)
