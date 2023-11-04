import time
import tracemalloc

# decorator for time consumption measurements
def measure_time(func):
    def wrapper(*args, **kwargs):
        # trace memory
        tracemalloc.start()
        
        # Wrapped function call
        result = func(*args, **kwargs)

        print(f"Peak memory usage: {tracemalloc.get_traced_memory()[1]} bytes")
        tracemalloc.stop()
        return result
    return wrapper

# decorator for time consumption measurements
def measure_memory(func):
    def wrapper(*args, **kwargs):
        # trace time before function call
        start_time = time.time()
        
        # Wrapped function call
        result = func(*args, **kwargs)
        
        end_time = time.time()

        print(f"Execution time: {end_time - start_time} seconds")
        return result
    return wrapper