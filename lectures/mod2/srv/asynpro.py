import asyncio

class EchoProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        """
        Called when a connection is established. Initialize protocol with transport.
        """
        self.transport = transport
        print("Connection established")

    def data_received(self, data):
        """
        Called when data is received. Process the data and send it back.
        """
        message = data.decode()
        print(f"Received: {message}")

        # Echo the received data back to the client
        self.transport.write(data)
        print(f"Sent: {message}")
        print('Close the client socket')
        self.transport.close()
        
    def error_received(self, exception):
        """
        Called when an error occurs. Handle the exception.
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

    # Create a TCP server using the EchoProtocol
    server = await loop.create_server(
        lambda: EchoProtocol(), '127.0.0.1', 8888
    )

    print("Server running on 127.0.0.1:8888")

    async with server:
        await server.serve_forever()

asyncio.run(main())
