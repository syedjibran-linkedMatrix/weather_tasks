import time

def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time-start_time
        print(f"Function named as {func.__name__} is executed in {execution_time:.4f} seconds")
    return wrapper

@timing
def add(a,b):
    return a+b

@timing
def sleep_function():
    time.sleep(3)
    return "Function is finished"


add(3,2)
sleep_function()