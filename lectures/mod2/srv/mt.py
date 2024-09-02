import threading
import time
from queue import Queue

def thread_worker(lock, event, queue, condition):
    """Worker function demonstrating synchronization and communication."""
    with lock:
        print(f"{threading.current_thread().name}: Lock acquired.")
        time.sleep(1)
        print(f"{threading.current_thread().name}: Performing work...")

    # Wait for an event to proceed
    print(f"{threading.current_thread().name}: Waiting for event.")
    event.wait()
    print(f"{threading.current_thread().name}: Event triggered, resuming work.")

    with condition:
        print(f"{threading.current_thread().name}: Condition acquired, waiting for notification.")
        condition.wait()
        print(f"{threading.current_thread().name}: Notified, continuing work.")

    # Simulate work and put a result in the queue
    result = f"Result from {threading.current_thread().name}"
    queue.put(result)
    print(f"{threading.current_thread().name}: Result put in queue.")

def timer_worker():
    """Worker function executed by a Timer."""
    print("Timer worker executed after delay.")

def daemon_worker():
    """Worker function for daemon thread."""
    i = 15
    while i>0:
        print("Daemon thread running in the background.")
        time.sleep(2)
        i = i-1
    
    print("Daemon stopped.")

def main():
    # 1. Thread Management
    print("=== Thread Management ===")
    lock = threading.Lock()
    event = threading.Event()
    queue = Queue()
    condition = threading.Condition()

    threads = []
    for i in range(3):
        t = threading.Thread(target=thread_worker, args=(lock, event, queue, condition))
        threads.append(t)
        t.start()

    # 2. Timer
    print("\n=== Timer ===")
    timer = threading.Timer(5, timer_worker)
    timer.start()  # Will execute after 5 seconds

    # 3. Daemon Threads
    print("\n=== Daemon Threads ===")
    daemon = threading.Thread(target=daemon_worker, daemon=True)
    daemon.start()

    # Allow daemon thread to run for a bit
    time.sleep(6)
    
    # 4. Trigger event and notify condition
    print("\n=== Triggering Event and Notifying Condition ===")
    event.set()  # Trigger the event to unblock threads waiting on it

    time.sleep(1)
    with condition:
        condition.notify_all()  # Notify all threads waiting on the condition
    time.sleep(1)

    # 5. Wait for all threads to complete
    for t in threads:
        t.join()

    # 6. Retrieve and display results from the queue
    print("\n=== Queue Results ===")
    while not queue.empty():
        print(queue.get())

if __name__ == "__main__":
    main()
