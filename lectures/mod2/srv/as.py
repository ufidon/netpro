import asyncio

# Function simulating an asynchronous task
async def async_worker(lock, event, semaphore, name):
    async with lock:  # Acquire lock asynchronously
        print(f"{name}: Lock acquired.")
        await asyncio.sleep(1)
        print(f"{name}: Performing work.")

    # Wait for an event to proceed
    print(f"{name}: Waiting for event.")
    await event.wait()
    print(f"{name}: Event triggered, resuming work.")

    # Use semaphore to control access
    async with semaphore:
        print(f"{name}: Semaphore acquired, doing limited work.")
        await asyncio.sleep(1)

    return f"Result from {name}"

# Function simulating asynchronous I/O using streams
async def async_io_handler(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    print(f"Received: {message}")

    response = f"Echo: {message}"
    writer.write(response.encode())
    await writer.drain()  # Ensure data is sent
    print("Response sent.")

    writer.close()
    await writer.wait_closed()

async def main():
    # 1. Event Loop Management
    loop = asyncio.get_event_loop()

    # 2. Task Management
    lock = asyncio.Lock()
    event = asyncio.Event()
    semaphore = asyncio.Semaphore(2)  # Allow max 2 concurrent tasks

    tasks = [
        loop.create_task(async_worker(lock, event, semaphore, "Task 1")),
        loop.create_task(async_worker(lock, event, semaphore, "Task 2")),
        loop.create_task(async_worker(lock, event, semaphore, "Task 3")),
    ]

    # Start the async I/O server
    server = await asyncio.start_server(async_io_handler, '127.0.0.1', 8888)

    # Allow the tasks to run a bit before setting the event
    await asyncio.sleep(2)
    print("\n=== Triggering Event ===")
    event.set()

    # 3. Future Handling
    results = await asyncio.gather(*tasks)  # Gather results from tasks
    print("\n=== Results ===")
    for result in results:
        print(result)

    # Close the server
    server.close()
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())  # 4. Run the event loop
