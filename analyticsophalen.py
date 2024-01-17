import threading
from getnewgame import getrecommendedgames
from getmostplayedgame import getmostplayed


def analyticsmulticore(steamid64):
    # global steamid64
    # Define the task functions
    task_functions = [task_function_1, task_function_2]

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

    # print("All threads have finished.")


def task_function_1(steamid64):
    getrecommendedgames(steamid64)


def task_function_2(steamid64):
    getmostplayed(steamid64)



# analyticsmulticore("76561199022018738")