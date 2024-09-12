import asyncio

async def handle_client(reader, writer):
    print("Client connected")

    while True:
        # Read the length prefix
        length_data = await reader.readexactly(4)  # Assuming length prefix is 4 bytes
        message_length = int.from_bytes(length_data, 'big')
        
        # Read the message
        message = await reader.readexactly(message_length)
        print(f"Received message: {message.decode()}")
        
        # Echo the message back
        writer.write(length_data + message)
        await writer.drain()

async def server():
    server = await asyncio.start_server(handle_client, 'localhost', 8888)
    async with server:
        await server.serve_forever()

asyncio.run(server())
