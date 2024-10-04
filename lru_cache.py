from functools import lru_cache
import time


@lru_cache
def add(a,b):
    time.sleep(3)
    return a+b

print(add(3,5)) #result will print after 3 second because it is not cached yet
print(add(3,5)) #result will print immediately