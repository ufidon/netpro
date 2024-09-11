import asyncio
import websockets

async def handle_client(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(message)  # Echo back the received message

async def server():
    async with websockets.serve(handle_client, 'localhost', 8765):
        print("WebSocket server is listening on ws://localhost:8765")
        await asyncio.Future()  # Run the server forever

asyncio.run(server())
