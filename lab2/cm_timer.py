import time
from contextlib import contextmanager

class cm_timer_1:
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        print(f"time: {elapsed_time:.2f}")


with cm_timer_1(): # comment for right work №7
    time.sleep(5.2)


@contextmanager
def cm_timer_2():
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"time: {elapsed_time:.2f}")


with cm_timer_2():
    time.sleep(5.2)