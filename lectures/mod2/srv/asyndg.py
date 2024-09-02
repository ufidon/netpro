import asyncio

class EchoDatagramProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        """
        Called when the connection is established.
        """
        self.transport = transport
        print("Connection established")

    def datagram_received(self, data, addr):
        """
        Called when a datagram is received.
        """
        message = data.decode()
        print(f"Received: {message} from {addr}")

        # Echo the received data back to the client
        self.transport.sendto(data, addr)
        print(f"Sent: {message}")

    def error_received(self, exception):
        """
        Called when an error occurs.
        """
        print(f"Error received: {exception}")

    def connection_lost(self, exc):
        """
        Called when the connection is closed or lost.
        """
        if exc:
            print(f"Connection lost with error: {exc}")
        else:
            print("Connection closed")

async def main():
    loop = asyncio.get_running_loop()

    # Create a UDP server using the EchoDatagramProtocol
    listen = loop.create_datagram_endpoint(
        lambda: EchoDatagramProtocol(), local_addr=('127.0.0.1', 9999)
    )

    transport, protocol = await listen
    print("Server running on 127.0.0.1:9999")

    try:
        await asyncio.sleep(3600)  # Keep the server running for 1 hour
    finally:
        transport.close()

asyncio.run(main())
