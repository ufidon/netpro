import asyncio

async def client():
    reader, writer = await asyncio.open_connection('localhost', 8889)

    # Send a message with delimiter
    message = "Hello, Server!"
    writer.write((message + '\n').encode())
    await writer.drain()

    # Receive the response
    response = await reader.readuntil(b'\n')
    print(f"Received response: {response.decode().strip()}")

    writer.close()
    await writer.wait_closed()

asyncio.run(client())
