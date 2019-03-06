import sys
import os
import time
import functools


def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer


def os_detect(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        value = func(*args, **kwargs)
        return '{} {}!'.format(value, sys.platform)
    return wrapper_timer


@os_detect
@timer
def crazy_func():
    a = [x**1000 for x in range(10000)]
    return 'hello'


print(crazy_func())
