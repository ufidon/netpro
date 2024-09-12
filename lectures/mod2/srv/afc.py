import asyncio

async def client():
    reader, writer = await asyncio.open_connection('localhost', 8890)

    # Send a message with fixed length
    message = "Hello, Server!".ljust(1024)
    writer.write(message.encode())
    await writer.drain()

    # Receive the response
    response = await reader.readexactly(1024)
    print(f"Received response: {response.decode().strip()}")

    writer.close()
    await writer.wait_closed()

asyncio.run(client())
