import asyncio

async def handle_client(reader, writer):
    print("Client connected")

    while True:
        # Read a fixed length of 1024 bytes
        data = await reader.readexactly(1024)
        message = data.decode().strip()
        if not message:
            break
        print(f"Received message: {message}")

        # Echo the message back
        writer.write(data)
        await writer.drain()

    writer.close()
    await writer.wait_closed()

async def server():
    server = await asyncio.start_server(handle_client, 'localhost', 8890)
    async with server:
        await server.serve_forever()

asyncio.run(server())
