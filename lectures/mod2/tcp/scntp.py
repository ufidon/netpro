from scapy.all import *
import time
NTP_DELTA = 2208988800  # Time difference between 1900 and 1970 in seconds

def ntp_request(server):
    # Create an IP packet
    ip = IP(dst=server)
    
    # Create a UDP packet with destination port 123 (NTP)
    udp = UDP(dport=123)
    
    # Create an NTP packet
    ntp = NTP(version=4, mode=3)  # Version 4, Client mode
    
    # Combine the packets
    packet = ip/udp/ntp
    
    # Send the packet and wait for a response
    response = sr1(packet, timeout=2, verbose=False)
    
    return response

def analyze_ntp_response(response):
    if response is None:
        print("No response received.")
        return
    
    if NTP not in response:
        print("Response doesn't contain an NTP packet.")
        return
    
    ntp = response[NTP]
    
    print(f"NTP Server: {response[IP].src}")
    print(f"Stratum: {ntp.stratum}")
    print(f"Reference ID: {ntp.ref_id}")
    print(f"Root delay: {ntp.delay}")
    print(f"Root dispersion: {ntp.dispersion}")
    
    # Calculate and print the offset
    client_tx = ntp.orig - NTP_DELTA
    server_rx = ntp.recv - NTP_DELTA
    server_tx = ntp.sent - NTP_DELTA
    client_rx = time.time()
    
    offset = ((server_rx - client_tx) + (server_tx - client_rx)) / 2
    print(f"Offset: {offset:.6f} seconds")

    print("current time:", datetime.fromtimestamp(float(client_rx+offset)));

if __name__ == "__main__":
    server = "pool.ntp.org"  # You can change this to any NTP server
    
    print(f"Sending NTP request to {server}...")
    response = ntp_request(server)
    
    if response:
        analyze_ntp_response(response)
    else:
        print("No response received from the server.")