The Network Time Protocol (NTP) packet consists of several fields, each serving a specific purpose in synchronizing time between the client and server. Below is a detailed explanation of each field and its value in an NTP packet:

### NTP Packet Structure

The NTP packet structure typically consists of 48 bytes and includes the following fields:

1. **LI (Leap Indicator) (2 bits)**
   - **Purpose**: Indicates whether there is a leap second adjustment.
   - **Values**:
     - `00`: No warning.
     - `01`: Last minute has 61 seconds.
     - `10`: Last minute has 59 seconds.
     - `11`: Clock is unsynchronized.

2. **VN (Version Number) (3 bits)**
   - **Purpose**: Indicates the NTP protocol version.
   - **Values**: Ranges from `000` (version 1) to `100` (version 4).

3. **Mode (3 bits)**
   - **Purpose**: Indicates the mode of operation.
   - **Values**:
     - `0`: Reserved.
     - `1`: Symmetric active.
     - `2`: Symmetric passive.
     - `3`: Client.
     - `4`: Server.
     - `5`: Broadcast.
     - `6`: NTP control message.
     - `7`: Reserved for private use.

4. **Stratum (8 bits)**
   - **Purpose**: Indicates the stratum level of the clock source.
   - **Values**:
     - `0`: Unspecified or invalid.
     - `1`: Primary reference (e.g., a radio clock equipped with a GPS receiver).
     - `2-15`: Secondary reference (synchronized via NTP).
     - `16`: Unsynchronized.
     - `17-255`: reserved.

5. **Poll Interval (8 bits)**
   - **Purpose**: Indicates the maximum interval between successive messages, expressed as a power of two in seconds.
   - **Values**: Ranges from `MINPOLL` `4` ($16=2^4$ seconds) to `MAXPOLL` `17` ($131,072=2^{17}$ seconds).

6. **Precision (8 bits)**
   - **Purpose**: Indicates the precision of the system clock, expressed as a power of two.
   - **Values**: Typically a negative value; e.g., `-20` corresponds to a precision of about 1 microsecond.
   - The precision is normally determined when the service first starts up as the minimum of several iterations of the time to read the system clock.

7. **Root Delay (32 bits)**
   - **Purpose**: Indicates the total round-trip delay to the primary reference source, in seconds.
   - **Values**: a floating number in NTP short format with 16 bits integer and 16 bits fractional. Positive values indicate a delay; negative values indicate an advance.

8. **Root Dispersion (32 bits)**
   - **Purpose**: Indicates the maximum error relative to the primary reference source, in seconds.
   - **Values**: a floating number in NTP short format with 16 bits integer and 16 bits fractional. Represents the nominal error.

9. **Reference Identifier (32 bits)**
   - **Purpose**: Identifies the particular reference source.
   - **Values**: 
     - Stratum 0-1: ASCII string (e.g., "GPS ", "ATOM").
     - Stratum 2-15: The IP address of the reference NTP server.
       - the four-octet IPv4 address, or
       - the first four octets of the MD5 hash of the IPv6 address

**ASCII identifiers**

- Stratum=0: a four-character ASCII string, called the "kiss code"
- Stratum=1: a four-octet, left-justified, zero-padded ASCII    string assigned to the reference clock
- Any string beginning with the ASCII character "X" is reserved for unregistered
   experimentation and development

| ID   | Clock Source                                             |
|------|----------------------------------------------------------|
| GOES | Geosynchronous Orbit Environment Satellite               |
| GPS  | Global Position System                                   |
| GAL  | Galileo Positioning System                               |
| PPS  | Generic pulse-per-second                                 |
| IRIG | Inter-Range Instrumentation Group                        |
| WWVB | LF Radio WWVB Ft. Collins, CO 60 kHz                     |
| DCF  | LF Radio DCF77 Mainflingen, DE 77.5 kHz                  |
| HBG  | LF Radio HBG Prangins, HB 75 kHz                         |
| MSF  | LF Radio MSF Anthorn, UK 60 kHz                          |
| JJY  | LF Radio JJY Fukushima, JP 40 kHz, Saga, JP 60 kHz       |
| LORC | MF Radio LORAN C station, 100 kHz                        |
| TDF  | MF Radio Allouis, FR 162 kHz                             |
| CHU  | HF Radio CHU Ottawa, Ontario                             |
| WWV  | HF Radio WWV Ft. Collins, CO                             |
| WWVH | HF Radio WWVH Kauai, HI                                  |
| NIST | NIST telephone modem                                     |
| ACTS | NIST telephone modem                                     |
| USNO | USNO telephone modem                                     |
| PTB  | European telephone modem                                 |


This table lists clock source IDs and their descriptions in a clear and organized way using Markdown syntax.


1.  **Reference Timestamp (64 bits)**
    - **Purpose**: Indicates the time when the system clock was last set or corrected.
    - **Values**: 64-bit timestamp (32 bits for seconds and 32 bits for the fractional second part).

2.  **Originate Timestamp (64 bits)**
    - **Purpose**: The time at which the client sent the request to the server.
    - **Values**: 64-bit timestamp in NTP timestamp format(32 bits for seconds and 32 bits for the fractional second part).

3.  **Receive Timestamp (64 bits)**
    - **Purpose**: The time at which the server received the client's request.
    - **Values**: 64-bit timestamp in NTP timestamp format(32 bits for seconds and 32 bits for the fractional second part).

4.  **Transmit Timestamp (64 bits)**
    - **Purpose**: The time at which the server sent the response to the client.
    - **Values**: 64-bit timestamp in NTP timestamp format(32 bits for seconds and 32 bits for the fractional second part).

5.  **Optional Fields (Extension Fields)**
    - **Purpose**: Used for authentication and other purposes.
    - **Values**: Various, depending on the extension used.

### Example NTP Packet

Let's consider an example of each field value in a typical NTP response packet:

- **LI_VN_MODE**: `00100100` (Leap Indicator: 0, Version Number: 4, Mode: 4)
- **Stratum**: `2` (Secondary reference)
- **Poll Interval**: `6` (64 seconds)
- **Precision**: `-20` (Precision of about 1 microsecond)
- **Root Delay**: `0.00390625` seconds
- **Root Dispersion**: `0.00781250` seconds
- **Reference Identifier**: `192.168.1.1` (IP address of the reference server)
- **Reference Timestamp**: `3849015734.12345678` (Time when the clock was last set)
- **Originate Timestamp**: `3849015756.23456789` (Time when the client sent the request)
- **Receive Timestamp**: `3849015756.34567890` (Time when the server received the request)
- **Transmit Timestamp**: `3849015756.45678901` (Time when the server sent the response)

### Interpreting the Timestamps

- **NTP Timestamp Format**: The timestamps are given in seconds since January 1, 1900, with the fractional part representing fractions of a second.
- **Convert to Unix Time**: To convert NTP time to Unix time, subtract `2208988800` seconds (the difference between the NTP and Unix epochs).

For example, if the **Transmit Timestamp** is `3849015756.45678901`:
- Convert to Unix time: `3849015756.45678901 - 2208988800 = 1640026956.45678901`
- Human-readable format: `2021-12-20 12:02:36.456789` UTC


## How Does A NTP Calculate the Precision?

The precision in an NTP packet represents the precision of the system clock, and it is expressed as a power of two in seconds. The formula to calculate the precision is:

$\text{Precision} = 2^{n} \text{ seconds}$

Where `n` is a signed integer representing the precision.

### Steps to Calculate NTP Precision:

1. **Determine the clock resolution**: Identify the smallest time increment the system clock can measure (e.g., 1 millisecond, 1 microsecond, etc.).

2. **Express the resolution in seconds**: Convert the clock resolution to seconds. For example, if the resolution is 1 millisecond, then:

   $\text{Clock Resolution} = 0.001 \text{ seconds}$

3. **Calculate the power of two**: Express the clock resolution as a power of two by finding the nearest power of two less than or equal to the clock resolution in seconds.

   For example, if the clock resolution is 1 millisecond (`0.001` seconds):

   $\text{Precision} = 2^{-10} \text{ seconds}$

   Here, $2^{-10}$ is approximately $0.0009765625$ seconds, which is close to 1 millisecond.

4. **Determine the precision value (n)**: The exponent $n$ in the power of two (which is `-10` in this example) is the precision value that will be included in the NTP packet.

### Example Calculation:

- If the system clock has a precision of 1 microsecond:

   $\text{Clock Resolution} = 0.000001 \text{ seconds}$

   Find the nearest power of two:

   $\text{Precision} = 2^{-20} \text{ seconds}$

   Here, $n = -20$, so the precision field in the NTP packet would be `-20`.


## How Does A NTP Server Calculate The Root Delay?

### Root Delay Calculation

**Root Delay** represents the total round-trip delay to the primary reference source (i.e., the delay between the NTP server and its reference clock). It's calculated as the sum of the network delays between each pair of NTP servers in the synchronization path.

#### Calculation
Root Delay is typically calculated in a multi-hop NTP hierarchy where multiple NTP servers synchronize to one another. The delay for each hop is measured, and the Root Delay is the sum of these delays.

1. **Single Hop (Direct connection to a reference clock):**
   - $\text{Root Delay} = \text{Round-Trip Delay to Reference Clock}$

2. **Multiple Hops (NTP server synchronizes to another NTP server):**
   - $\text{Root Delay} = \sum_{i=1}^{n} \text{Network Delay of Hop } i$
   where `n` is the number of hops to the primary reference clock.

- The delay for each hop is measured using the NTP timestamps (T1, T2, T3, T4) where:
  - T1: Time at which the request was sent by the client.
  - T2: Time at which the request was received by the server.
  - T3: Time at which the server sent the response.
  - T4: Time at which the response was received by the client.

  The round-trip delay $D$ for each hop is: 
  $D = (T4 - T1) - (T3 - T2)$

### Root Dispersion Calculation

**Root Dispersion** is the maximum error relative to the primary reference source. It accounts for the cumulative clock offset of all the NTP servers in the synchronization path.

#### Calculation
1. **Single Hop (Direct connection to a reference clock):**
   - $\text{Root Dispersion} = \text{Maximum Error of Reference Clock}$

2. **Multiple Hops (NTP server synchronizes to another NTP server):**
   - $\text{Root Dispersion} = \sum_{i=1}^{n} \text{Dispersion of Hop } i$
     - where `n` is the number of hops to the primary reference clock.

- The dispersion for each hop is calculated as:
   - $\text{Dispersion} = \text{Precision} + (\text{Error Bound} \times \text{Age})$
      - **Precision**: Indicates the precision of the clock.
      - **Error Bound**: Represents the maximum clock offset from the true time.
      - **Age**: The time since the last synchronization.

### Practical Example

Consider a simple NTP hierarchy where your server synchronizes to an upstream NTP server, which in turn is synchronized to a stratum 1 server.

1. **Root Delay Calculation**:
   - The delay between your server and the upstream server: 50 ms.
   - The delay between the upstream server and the stratum 1 server: 20 ms.
   - **Total Root Delay**: 50 ms + 20 ms = 70 ms.

2. **Root Dispersion Calculation**:
   - Your server's clock precision: 1 ms.
   - Upstream server's clock precision: 2 ms.
   - Error Bound for your server: 0.5 ms/s.
   - Error Bound for the upstream server: 0.3 ms/s.
   - Time since the last synchronization for both servers: 10 s.
   - **Root Dispersion**:
     - Your server: $1 \text{ ms} + (0.5 \times 10) = 6 \text{ ms}$
     - Upstream server: $2 \text{ ms} + (0.3 \times 10) = 5 \text{ ms}$
     - **Total Root Dispersion**: 6 ms + 5 ms = 11 ms.

This gives you an estimate of the total delay and error that could be expected between your server and the reference clock at the root of the NTP hierarchy.

# References
- [Network Time Protocol Version 4  Core Protocol Specification](https://www.eecis.udel.edu/~mills/database/brief/flow/ntp4.pdf)
- [Network Time Protocol Version 4 Reference and Implementation Guide](https://www.eecis.udel.edu/~mills/database/reports/ntp4/ntp4.pdf)
- [The Network Time Protocol (NTP) Project](https://www.ntp.org/)
  - [Computer Network Time Synchronization: the Network Time Protocol](https://www.ntp.org/reflib/brief/seminar/ntp.pdf)
- [What's the best timing resolution can i get on Linux](https://stackoverflow.com/questions/12643535/whats-the-best-timing-resolution-can-i-get-on-linux)