import asyncio
import websockets

async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        message = "Hello, Server!"
        print(f"Sending message: {message}")
        await websocket.send(message)
        
        response = await websocket.recv()
        print(f"Received response: {response}")

asyncio.run(client())
