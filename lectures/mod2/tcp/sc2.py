import socket
import struct
import time
import datetime

NTP_SERVER = "time.google.com"  # NTP server
NTP_PORT = 123
NTP_PACKET_FORMAT = "!12I"  # 12 unsigned 32-bit integers in big-endian format
NTP_DELTA = 2208988800  # Time difference between 1900 and 1970 in seconds

def parse_sntp_response(data):
    unpacked_data = struct.unpack(NTP_PACKET_FORMAT, data[:48])
    
    # Extracting the relevant fields
    leap_indicator = (unpacked_data[0] >> 30) & 0x3
    version_number = (unpacked_data[0] >> 27) & 0x7
    mode = (unpacked_data[0] >> 24) & 0x7
    stratum = data[1] & 0xff
    poll_interval = data[2] & 0xff
    precision = data[3] & 0xff

    root_delay = unpacked_data[1] / (2**16)
    root_dispersion = unpacked_data[2] / (2**16)
    ref_id = unpacked_data[3]
    
    # Timestamps
    ref_timestamp = unpacked_data[4] + float(unpacked_data[5]) / 2**32
    orig_timestamp = unpacked_data[6] + float(unpacked_data[7]) / 2**32
    recv_timestamp = unpacked_data[8] + float(unpacked_data[9]) / 2**32
    transmit_timestamp = unpacked_data[10] + float(unpacked_data[11]) / 2**32
    
    return {
        "leap_indicator": leap_indicator,
        "version_number": version_number,
        "mode": mode,
        "stratum": stratum,
        "poll_interval": poll_interval,
        "precision": precision,
        "root_delay": root_delay,
        "root_dispersion": root_dispersion,
        "ref_id": ref_id,
        "ref_timestamp": ref_timestamp - NTP_DELTA,
        "orig_timestamp": orig_timestamp - NTP_DELTA,
        "recv_timestamp": recv_timestamp - NTP_DELTA,
        "transmit_timestamp": transmit_timestamp - NTP_DELTA,
    }

def sntp_request():
    # Create a socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(5)

    # Get the current time as the Originate Timestamp
    current_time = time.time()  # Current time in seconds since Unix epoch
    epoch_diff = 2208988800  # Difference between 1900 and 1970 in seconds
    timestamp = current_time + epoch_diff

    # Convert to SNTP format (64-bit value with 32 bits for seconds and 32 bits for fractions)
    seconds = int(timestamp)
    fractional = int((timestamp - seconds) * (2**32))

    # Pack the timestamp into the SNTP request
    originate_timestamp = struct.pack('!I', seconds) + struct.pack('!I', fractional)

    # Prepare the SNTP request packet (48 bytes)
    # Only the first byte is non-zero, setting LI=0, VN=4, Mode=3 (client mode)
    packet = b'\x1b' + 47 * b'\0'

    # Insert the Originate Timestamp into the packet (starting at byte 24)
    packet = packet[:24] + originate_timestamp + packet[32:]

    # Send the SNTP request to the server
    client.sendto(packet, (NTP_SERVER, NTP_PORT))

    # Receive the response from the server
    try:
        data, _ = client.recvfrom(1024)
    except socket.timeout:
        print("Request timed out")
        return

    # Close the socket
    client.close()

    # Parse the response
    parsed_response = parse_sntp_response(data)
    
    # Calculate the offset from the SNTP server
    # T1 = parsed_response['orig_timestamp']
    T1 = current_time
    T2 = parsed_response['recv_timestamp']
    T3 = parsed_response['transmit_timestamp']
    T4 = time.time()  # Local system time when the response was received
    
    offset = ((T2 - T1) + (T3 - T4)) / 2
    
    print("SNTP Response:")
    print(f"Leap Indicator: {parsed_response['leap_indicator']}")
    print(f"Version Number: {parsed_response['version_number']}")
    print(f"Mode: {parsed_response['mode']}")
    print(f"Stratum: {parsed_response['stratum']}")
    print(f"Root Delay: {parsed_response['root_delay']} seconds")
    print(f"Root Dispersion: {parsed_response['root_dispersion']} seconds")
    print(f"Reference Timestamp: {datetime.datetime.utcfromtimestamp(parsed_response['ref_timestamp'])}")
    print(f"Originate Timestamp (T1): {datetime.datetime.utcfromtimestamp(T1)}")
    print(f"Receive Timestamp (T2): {datetime.datetime.utcfromtimestamp(T2)}")
    print(f"Transmit Timestamp (T3): {datetime.datetime.utcfromtimestamp(T3)}")
    print(f"Destination Timestamp (T4): {datetime.datetime.utcfromtimestamp(T4)}")
    print(f"Offset: {offset} seconds")
    print(f"Corrected Time: {datetime.datetime.utcfromtimestamp(T4 + offset)} UTC")

if __name__ == "__main__":
    sntp_request()
