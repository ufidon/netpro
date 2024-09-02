from multiprocessing import Process, Lock, Event, Semaphore, Queue, Pipe, Value, Array, Pool
import time

def worker_with_lock(lock, value):
    """Worker function that uses a lock for synchronization."""
    with lock:
        print("Lock acquired by worker.")
        value.value += 1
        time.sleep(2)
        print(f"Value after increment by worker with lock: {value.value}")

def worker_with_event(event):
    """Worker function that waits for an event."""
    print("Worker waiting for event.")
    event.wait()  # Wait until event is set
    print("Event received! Worker proceeding...")

def worker_with_semaphore(semaphore, num):
    """Worker function that uses a semaphore."""
    with semaphore:
        print(f"Worker {num} acquired semaphore.")
        time.sleep(1)
        print(f"Worker {num} releasing semaphore.")

def worker_with_pipe(conn):
    """Worker function that sends data via Pipe."""
    conn.send("Data from worker via Pipe")
    conn.close()

def worker_with_queue(queue):
    """Worker function that sends data via Queue."""
    queue.put("Data from worker via Queue")

def worker_with_shared_memory(num, arr):
    """Worker function that uses shared memory."""
    num.value += 10
    for i in range(len(arr)):
        arr[i] *= -1
    print(f"Shared memory updated: num={num.value}, arr={arr[:]}")

def worker_with_pool(x):
    """Worker function for process pooling."""
    return x * x

def main():
    # 1. Process Management: Creation and Termination
    print("=== Process Management: Creation and Termination ===")
    lock = Lock()
    value = Value('i', 0)
    p1 = Process(target=worker_with_lock, args=(lock, value))
    p1.start()
    p1.join()  # Wait for process to complete

    # Terminate a process (not really needed here as the process completes)
    # p1.terminate()

    # 2. Synchronization with Lock, Event, and Semaphore
    print("\n=== Synchronization with Lock, Event, and Semaphore ===")
    event = Event()
    semaphore = Semaphore(2)  # Allow 2 workers to run concurrently

    p2 = Process(target=worker_with_event, args=(event,))
    p3 = Process(target=worker_with_semaphore, args=(semaphore, 1))
    p4 = Process(target=worker_with_semaphore, args=(semaphore, 2))

    p2.start()
    p3.start()
    p4.start()

    time.sleep(2)  # Delay to show event waiting
    event.set()  # Trigger event, letting p2 continue

    p2.join()
    p3.join()
    p4.join()

    # 3. IPC Communication with Pipe and Queue
    print("\n=== IPC Communication with Pipe and Queue ===")
    parent_conn, child_conn = Pipe()
    queue = Queue()

    p5 = Process(target=worker_with_pipe, args=(child_conn,))
    p6 = Process(target=worker_with_queue, args=(queue,))

    p5.start()
    p6.start()

    print(parent_conn.recv())  # Receive data from pipe
    print(queue.get())         # Receive data from queue

    p5.join()
    p6.join()

    # 4. Shared Memory with Value and Array
    print("\n=== Shared Memory with Value and Array ===")
    num = Value('i', 5)
    arr = Array('i', [1, 2, 3, 4, 5])

    p7 = Process(target=worker_with_shared_memory, args=(num, arr))
    p7.start()
    p7.join()

    print(f"Final shared memory: num={num.value}, arr={arr[:]}")

    # 5. Process Pooling
    print("\n=== Process Pooling ===")
    with Pool(4) as pool:
        results = pool.map(worker_with_pool, range(10))
        print(f"Pooling results: {results}")

if __name__ == "__main__":
    main()