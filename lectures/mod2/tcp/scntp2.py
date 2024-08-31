from scapy.all import *
import time
import socket
NTP_DELTA = 2208988800  # Time difference between 1900 and 1970 in seconds

def ntp_request(server):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)

    # Create an NTP packet
    ntp = NTP(version=4, mode=3)  # Version 4, Client mode
    
    try:
        # Send the packet
        sock.sendto(bytes(ntp), (server, 123))
        
        # Receive the response
        data, addr = sock.recvfrom(1024)
        
        # Parse the response
        response = NTP(data)
        
        return response
    except socket.timeout:
        print("Request timed out")
        return None
    finally:
        sock.close()

def analyze_ntp_response(response, server):
    if response is None:
        print("No response received.")
        return
    
    print(f"NTP Server: {server}")
    print(f"Stratum: {response.stratum}")
    print(f"Reference ID: {response.ref_id}")
    print(f"Root delay: {response.delay}")
    print(f"Root dispersion: {response.dispersion}")
    
    # Calculate and print the offset
    client_tx = response.orig - NTP_DELTA
    server_rx = response.recv - NTP_DELTA
    server_tx = response.sent - NTP_DELTA
    client_rx = time.time()

    print(f"{client_tx=}\n{server_rx=}\n{server_tx=}\n{client_rx=}")
    
    offset = ((server_rx - client_tx) + (server_tx - client_rx)) / 2
    print(f"Offset: {offset:.6f} seconds")

    print("current time:", datetime.fromtimestamp(float(client_rx+offset)));

if __name__ == "__main__":
    server = "pool.ntp.org"  # You can change this to any NTP server
    
    print(f"Sending NTP request to {server}...")
    response = ntp_request(server)
    
    if response:
        analyze_ntp_response(response, server)
    else:
        print("No response received from the server.")