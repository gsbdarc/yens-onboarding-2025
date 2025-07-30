import multiprocessing
import time
import math

def crunch_numbers():
    end_time = time.time() + 30  # Run for 30 seconds
    while time.time() < end_time:
        # Do some math-heavy operations
        for i in range(10000):
            math.sqrt(i)

if __name__ == "__main__":
    # On a shared cluster, DO NOT use multiprocessing.cpu_count()
    num_cores = 10  
    processes = []

    for _ in range(num_cores):
        p = multiprocessing.Process(target=crunch_numbers)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
