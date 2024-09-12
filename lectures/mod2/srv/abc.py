import asyncio

async def client():
    reader, writer = await asyncio.open_connection('localhost', 8888)

    # Send a message with length prefix
    message = "Hello, Server!"
    message_bytes = message.encode()
    length_prefix = len(message_bytes).to_bytes(4, 'big')
    writer.write(length_prefix + message_bytes)
    await writer.drain()

    # Receive the response
    response_length_data = await reader.readexactly(4)
    response_length = int.from_bytes(response_length_data, 'big')
    response = await reader.readexactly(response_length)
    print(f"Received response: {response.decode()}")

    writer.close()
    await writer.wait_closed()

asyncio.run(client())
