import asyncio

async def handle_client(reader, writer):
    print("Client connected")

    while True:
        # Read until delimiter
        data = b''
        while not data.endswith(b'\n'):
            chunk = await reader.read(100)
            if not chunk:
                return
            data += chunk

        message = data.strip(b'\n').decode()
        print(f"Received message: {message}")

        # Echo the message back
        writer.write(data)
        await writer.drain()

async def server():
    server = await asyncio.start_server(handle_client, 'localhost', 8889)
    async with server:
        await server.serve_forever()

asyncio.run(server())
