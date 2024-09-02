import asyncio

class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        print(f"Connection from {peername}")

    def data_received(self, data):
        message = data.decode()
        print(f"Data received: {message}")

        # Echo the received data back to the client
        self.transport.write(data)
        print(f"Sent: {message}")

        # Close the connection after echoing back the data
        self.transport.close()

async def main():
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '127.0.0.1', 8888
    )

    print("TCP server running on 127.0.0.1:8888")
    async with server:
        await server.serve_forever()

asyncio.run(main())
