import asyncio

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport
        print("UDP server started")

    def datagram_received(self, data, addr):
        message = data.decode()
        print(f"Received {message} from {addr}")

        # Echo the received data back to the client
        print(f"Sending {message} to {addr}")
        self.transport.sendto(data, addr)

async def main():
    loop = asyncio.get_running_loop()

    # Create a datagram endpoint (UDP)
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr=('127.0.0.1', 9999)
    )

    try:
        print("UDP server running on 127.0.0.1:9999")
        await asyncio.sleep(3600)  # Run for 1 hour
    finally:
        transport.close()

asyncio.run(main())
