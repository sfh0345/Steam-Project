import threading
import time

def analyticsmulticore(steamid64):
    # global steamid64
    # Define the task functions
    task_functions = [task_function_1, task_function_2, task_function_3, task_function_4, task_function_5, task_function_6, task_function_7]  # Add task_function_3, ..., task_function_7 as needed

    # Create threads
    threads = []
    for task_function in task_functions:
        thread = threading.Thread(target=task_function, args=(steamid64,))
        threads.append(thread)

    # Start the threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All threads have finished.")






def task_function_1(steamid64):
    for i in range(5):
        time.sleep(0.3)  # Simulating some work
        print("Thread 1:", i)
        print(steamid64)

def task_function_2(steamid64):
    for i in range(5):
        time.sleep(0.3)  # Simulating some work
        print("Thread 2:", i)

def task_function_3(steamid64):
    for i in range(10):
        time.sleep(0.3)  # Simulating some work
        print("Thread 3:", i)

def task_function_4(steamid64):
    for i in range(10):
        time.sleep(0.3)  # Simulating some work
        print("Thread 4:", i)

def task_function_5(steamid64):
    for i in range(10):
        time.sleep(0.3)  # Simulating some work
        print("Thread 5:", i)

def task_function_6(steamid64):
    for i in range(6):
        time.sleep(0.3)  # Simulating some work
        print("Thread 6:", i)

def task_function_7(steamid64):
    for i in range(10):
        time.sleep(0.3)  # Simulating some work
        print("Thread 7:", i)
        print(steamid64)

