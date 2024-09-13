### NTP Protocol Analysis and Implementation

---

### **Objective:**
This lab aims to provide hands-on experience with the Network Time Protocol (NTP). You will learn how to capture and analyze NTP packets using Wireshark, and then implement both an NTP client and server using Python socket.

---

### **Prerequisites:**
- Basic knowledge of networking protocols
- Familiarity with Wireshark
- Basic Python programming skills

### NTP Packet Format

#### 1. **NTP Packet Header Fields (First 32 Bits)**
- bit 0 is the **most significant bit**
- bit 31 is the **least significant bit**

| **Field**             | **Bit Range** | **Size (Bits)** | **Description**                                                                                              |
|-----------------------|---------------|-----------------|--------------------------------------------------------------------------------------------------------------|
| **LI (Leap Indicator)** | 0-1          | 2               | Indicates whether a leap second will be added or subtracted at the last minute of the last day of the month.  |
| **VN (Version Number)** | 2-4          | 3               | Indicates the version of NTP being used.                                                                     |
| **Mode**              | 5-7           | 3               | Specifies the mode of the packet: Client (3), Server (4), etc.                                               |
| **Stratum**           | 8-15          | 8               | Indicates the stratum level of the local clock, ranging from 0 (unspecified) to 15 (maximum).                 |
| **Poll Interval**     | 16-23         | 8               | The maximum interval between successive messages, expressed as a logarithm base 2.                           |
| **Precision**         | 24-31         | 8               | The precision of the system clock, expressed as a logarithm base 2.                                          |



#### 2. **NTP Packet Root Delay and Dispersion**
| **Field**               | **Size (Bits)** | **Description**                                                                                              |
|-------------------------|-----------------|--------------------------------------------------------------------------------------------------------------|
| **Root Delay**          | 32              | The total round-trip delay to the primary reference source, in seconds.                                       |
| **Root Dispersion**     | 32              | The maximum error relative to the primary reference source, in seconds.                                       |

#### 3. **NTP Packet Reference Identifier and Timestamps**
| **Field**                  | **Size (Bits)** | **Description**                                                                                              |
|----------------------------|-----------------|--------------------------------------------------------------------------------------------------------------|
| **Reference Identifier**    | 32              | Identifies the particular reference source.                                                                  |
| **Reference Timestamp**     | 64              | The time when the system clock was last set or corrected, in seconds and fraction.                            |
| **Originate Timestamp (t0)**     | 64              | The time at which the request departed the client for the server.                                             |
| **Receive Timestamp (t1)**       | 64              | The time at which the request arrived at the server.                                                          |
| **Transmit Timestamp (t2)**      | 64              | The time at which the response left the server for the client.                                                |

#### 4. **NTP Packet Extension Fields and Authentication**
| **Field**                 | **Size (Bits)** | **Description**                                                                                              |
|---------------------------|-----------------|--------------------------------------------------------------------------------------------------------------|
| **Key Identifier**        | 32              | Used in authenticated NTP to identify the key for message authentication.                                    |
| **Message Digest**        | 128             | A hash of the NTP message used for authentication (e.g., MD5 or SHA1).                                        |

# NTP Packet Field Calculations

NTP packets are typically 48 bytes long and contain several fields. Here's a breakdown of each field and how it's calculated from the raw data:

1. Leap Indicator (LI) - 2 bits
   - Formula: `(raw_data[0] >> 6) & 0x3`
   - Explanation: First 2 bits of the first byte

2. Version Number (VN) - 3 bits
   - Formula: `(raw_data[0] >> 3) & 0x7`
   - Explanation: Bits 3-5 of the first byte

3. Mode - 3 bits
   - Formula: `raw_data[0] & 0x7`
   - Explanation: Last 3 bits of the first byte

4. Stratum - 8 bits
   - Formula: `raw_data[1]`
   - Explanation: Entire second byte

5. Poll Interval - 8 bits
   - Formula: `raw_data[2]`
   - Explanation: Entire third byte

6. Precision - 8 bits (signed integer)
   - Formula: `struct.unpack('b', raw_data[3:4])[0]`
   - Explanation: Entire fourth byte, interpreted as a signed integer

7. Root Delay - 32 bits
   - Formula: `i,f = struct.unpack('!HH', raw_data[4:8])`
   - Explanation: Bytes 5-8, in NTP short format = 16-bit integer + 16-bit fraction, `i+f/2**16` seconds

8. Root Dispersion - 32 bits
   - Formula: `i,f = struct.unpack('!HH', raw_data[8:12])`
   - Explanation: Bytes 9-12, in NTP short format = 16-bit integer + 16-bit fraction, `i+f/2**16` seconds

9. Reference Identifier - 32 bits
   - Formula: `raw_data[12:16]`
   - Explanation: Bytes 13-16, usually interpreted as a 4-character ASCII string for IPv4

10. Reference Timestamp - 64 bits
    - Formula: `_parse_timestamp(raw_data[16:24])`
    - Explanation: Bytes 17-24, interpreted as NTP timestamp format

11. Origin Timestamp - 64 bits
    - Formula: `_parse_timestamp(raw_data[24:32])`
    - Explanation: Bytes 25-32, interpreted as NTP timestamp format

12. Receive Timestamp - 64 bits
    - Formula: `_parse_timestamp(raw_data[32:40])`
    - Explanation: Bytes 33-40, interpreted as NTP timestamp format

13. Transmit Timestamp - 64 bits
    - Formula: `_parse_timestamp(raw_data[40:48])`
    - Explanation: Bytes 41-48, interpreted as NTP timestamp format

**👉 NTP Timestamp parsing function**:
```python
def _parse_timestamp(raw_timestamp):
    """Convert a 64-bit NTP timestamp to a floating point number of seconds since the epoch."""
    int_part, frac_part = struct.unpack('!II', raw_timestamp)
    # NTP timestamp in floating seconds = int_part + frac_part / 2**32
    # Unix timestamp in floating seconds = NTP timestamp in floating seconds - 2208988800
    return int_part + frac_part / 2**32 - 2208988800  # Subtract seconds between 1900 and 1970
```

Note: The NTP timestamp is a 64-bit fixed-point number, where the first 32 bits represent the number of seconds since January 1, 1900, and the last 32 bits represent the fractional part of the second.

1.  The $\displaystyle \text{Corrected time} = t3 + \frac{(t1 - t0) + (t2 - t3)}{2}$
    - $t3$ is the time when the client received the ntp packet


**👉 Unix timestamp vs. datetime**
```python
import time
from datetime import datetime

# 1. get current time in unix timestamp
unix_timestamp = time.time()
print("current time in Unix timestamp: ", unix_timestamp) # sample output: current time in Unix timestamp:  1726238781.0123541

# convert unix timestamp to datetime
uts2dt = datetime.fromtimestamp(unix_timestamp)
print(f"{unix_timestamp} -> {uts2dt}") # sample output: 1726238781.0123541 -> 2024-09-13 10:46:21.012354

# 2. get current time in datetime
dttm = datetime.now()
print("Current time  in datetime: ", dttm) # sample output: Current time  in datetime:  2024-09-13 10:59:48.754367

# convert datetime to unix timestamp
dt2uts = dttm.timestamp()
print(f"{dttm}->{dt2uts}") # sample output: 2024-09-13 10:59:48.754367->1726239588.754367
```


# NTP Field Values to Raw Data Conversion

Here's how to convert each NTP field value back to its raw data representation:

1. Leap Indicator (LI), Version Number (VN), and Mode - Combined into first byte
   ```python
   first_byte = (LI << 6) | (VN << 3) | Mode
   raw_data = bytes([first_byte])
   ```

2. Stratum - 8 bits
   ```python
   raw_data += bytes([Stratum])
   ```

3. Poll Interval - 8 bits
   ```python
   raw_data += bytes([Poll])
   ```

4. Precision - 8 bits (signed integer)
   ```python
   raw_data += struct.pack('b', Precision)
   ```

5. Root Delay - 32 bits
   ```python
   root_delay_int = int(Root_Delay // 1)
   root_delay_frac = int((Root_Delay % 1) * 2**16)
   raw_data += struct.pack('!HH', root_delay_int, root_delay_frac)
   ```

6. Root Dispersion - 32 bits
   ```python
   root_dispersion_int = int(Root_Dispersion // 1)
   root_dispersion_frac = int((Root_Dispersion % 1) * 2**16)
   raw_data += struct.pack('!HH', root_dispersion_int, root_dispersion_frac)
   ```

7. Reference Identifier - 32 bits
   ```python
   if isinstance(Reference_ID, str):
       raw_data += Reference_ID.encode('ascii').ljust(4, b'\x00')
   else:
       raw_data += struct.pack('!I', Reference_ID)
   ```

8. Reference Timestamp - 64 bits
   ```python
   raw_data += _timestamp_to_ntp_format(Reference_Timestamp)
   ```

9. Origin Timestamp - 64 bits
   ```python
   raw_data += _timestamp_to_ntp_format(Origin_Timestamp)
   ```

10. Receive Timestamp - 64 bits
    ```python
    raw_data += _timestamp_to_ntp_format(Receive_Timestamp)
    ```

11. Transmit Timestamp - 64 bits
    ```python
    raw_data += _timestamp_to_ntp_format(Transmit_Timestamp)
    ```

NTP Timestamp conversion function:
```python
def _timestamp_to_ntp_format(timestamp):
    """Convert a floating point number of seconds since the Unix epoch to NTP timestamp format."""
    ntp_timestamp = timestamp + 2208988800  # Add seconds between 1900 and 1970
    int_part = int(ntp_timestamp)
    frac_part = int((ntp_timestamp - int_part) * 2**32)
    return struct.pack('!II', int_part, frac_part)
```

Complete packet assembly:
```python
def create_ntp_packet(LI, VN, Mode, Stratum, Poll, Precision, Root_Delay, Root_Dispersion, 
                      Reference_ID, Reference_Timestamp, Origin_Timestamp, 
                      Receive_Timestamp, Transmit_Timestamp):
    raw_data = bytes()
    
    # Assemble the packet using the formulas above
    
    # First byte (LI, VN, Mode)
    raw_data += bytes([(LI << 6) | (VN << 3) | Mode])
    
    # Remaining fields...
    raw_data += bytes([Stratum])
    raw_data += bytes([Poll])
    raw_data += struct.pack('b', Precision)
    raw_data += struct.pack('!HH', int(Root_Delay), int((Root_Delay - int(Root_Delay)) * 2**16))
    raw_data += struct.pack('!HH', int(Root_Dispersion), int((Root_Dispersion - int(Root_Dispersion)) * 2**16))
    
    if isinstance(Reference_ID, str):
        raw_data += Reference_ID.encode('ascii').ljust(4, b'\x00')
    else:
        raw_data += struct.pack('!I', Reference_ID)
    
    raw_data += _timestamp_to_ntp_format(Reference_Timestamp)
    raw_data += _timestamp_to_ntp_format(Origin_Timestamp)
    raw_data += _timestamp_to_ntp_format(Receive_Timestamp)
    raw_data += _timestamp_to_ntp_format(Transmit_Timestamp)
    
    return raw_data
```

---

### **Task 1: Capture and Analyze NTP Packets Using Wireshark**

#### **Objective:**
Capture NTP request and response packets using Wireshark and analyze the packet structure.

#### **Steps:**

1. **Setup Wireshark:**
   - Ensure Wireshark is installed on your system. 
   - Open Wireshark and select the network interface that connects to the internet.

2. **Capture NTP Traffic:**
   - In the Wireshark filter bar, enter `ntp` to filter NTP packets.
   - Start the capture.
   - On your machine, initiate an NTP request. You can do this by running `ntpdate <ntp-server-address>` in a terminal (Linux) or by using an existing NTP client tool.
      ```bash
      sudo apt install ntpdate
      ntpdate -q -u -p 1 pool.ntp.org
      ```

3. **Analyze NTP Packets:**
   - Once the NTP packets are captured, stop the capture in Wireshark.
   - Identify an NTP request packet and an NTP response packet in the capture.
   - Expand the packet details in Wireshark to analyze the fields, such as `LI`, `VN`, `Mode`, `Stratum`, `Timestamps`, etc.
     - Convert all timestamps into human-readable format
     - Calculate the corrected time
     - Hint: changing the format in the “Time Display Format” menu item in the “View” menu to find the time when a packet is captured
   - Take screenshots of the analyzed packets and document the significant fields.

#### **Deliverables:**
- Screenshots of NTP request and response packets.
- A short report summarizing the key fields in the packets and their significance.

---

### **Task 2: Implement an NTP Client Using Python**

#### **Objective:**
Develop a basic NTP client in Python that sends an NTP request to a server and processes the response to obtain the current time.

#### **Framework/Template:**

```python
import socket
import struct
import time

# Constants
NTP_SERVER = 'pool.ntp.org'
NTP_PORT = 123
NTP_TIMESTAMP_DELTA = 2208988800  # NTP epoch (1900-01-01) to UNIX epoch (1970-01-01)

def ntp_client():
    # Create a UDP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # NTP packet format (LI, VN, Mode = 3 for client)
    ntp_data = b'\x1b' + 47 * b'\0'
    
    # Send the packet to the NTP server
    client.sendto(ntp_data, (NTP_SERVER, NTP_PORT))
    
    # Receive the response from the server
    ntp_response, _ = client.recvfrom(1024)
    
    # Unpack the received data
    unpacked_data = struct.unpack('!12I', ntp_response)
    
    # Extract the transmit timestamp
    transmit_timestamp = unpacked_data[10] + float(unpacked_data[11]) / 2**32
    
    # Convert to UNIX time
    unix_time = transmit_timestamp - NTP_TIMESTAMP_DELTA
    
    # Calculate then print the corrected time
    # The corrected time = t3 + ((t1-t0) + (t2-t3))/2
    #   - t3 is the time when the client received the ntp packet

if __name__ == '__main__':
    ntp_client()
```

#### **Steps:**

1. **Understand the Template:**
   - Review the provided Python code template. Understand the structure and how the NTP request is formed.
   - The `ntp_client()` function sends a packet to an NTP server, receives a response, and then extracts the time.

2. **Test the NTP Client:**
   - Run the script on your local machine.
   - Verify that the script prints the correct current time by comparing it with your system’s time.

3. **Modify the Client:**
   - Modify the script to send additional information such as local time in the request packet.
   - Experiment with different NTP servers.

#### **Deliverables:**
- Modified NTP client code.
- Screenshot of the output showing all packet fields in human-readable format.

---

### **Task 3: Implement an NTP Server Using Python**

#### **Objective:**
Develop a basic NTP server in Python that listens for requests and sends accurate time responses.

#### **Framework/Template:**

```python
import socket
import struct
import time

# Constants
NTP_PORT = 123
NTP_TIMESTAMP_DELTA = 2208988800  # NTP epoch (1900-01-01) to UNIX epoch (1970-01-01)

def ntp_server():
    # Create a UDP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('0.0.0.0', NTP_PORT))
    
    print("NTP server running...")
    
    while True:
        # Receive an NTP request
        data, address = server.recvfrom(1024)
        
        # Get the current time
        current_time = time.time() + NTP_TIMESTAMP_DELTA
        
        # Create the NTP response packet
        ntp_data = struct.pack('!12I', 0b00100100, 0, 0, 0, 0, 0, 0, 0, 0, 0, int(current_time), int((current_time % 1) * 2**32))
        
        # Send the response back to the client
        server.sendto(ntp_data, address)

if __name__ == '__main__':
    ntp_server()
```

#### **Steps:**

1. **Understand the Template:**
   - Review the provided Python code template. Understand how the NTP response is constructed and how the server handles incoming requests.

2. **Test the NTP Server:**
   - Run the script on your local machine.
   - Use the NTP client implemented in Task 2 to send a request to this server and verify the response.

3. **Modify the Server:**
   - Enhance the server to handle multiple clients simultaneously.
   - Add functionality to log each request with a timestamp and client information.

#### **Deliverables:**
- Modified NTP server code.
- Screenshot of the server handling requests from clients.
  - show information of clients' endpoints and 
  - all packet fields in human-readable format.

---

### **Submission:**
- Submit the following files and reports:
  1. **Task 1:** Screenshots of NTP packets and a short analysis report.
  2. **Task 2:** Python code for the NTP client and screenshot of the output.
  3. **Task 3:** Python code for the NTP server and screenshot of it handling requests.

### **Conclusion:**
By completing this lab, you will gain practical knowledge of NTP, including how to analyze NTP packets, and implement your own NTP client and server using Python socket.

# References
- [Network Time Protocol Version 4: Protocol and Algorithms Specification](https://datatracker.ietf.org/doc/html/rfc5905)
- [NTP packet fields explanation](./ntpfields.md)