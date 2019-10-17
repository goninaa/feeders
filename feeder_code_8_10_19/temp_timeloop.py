import time
from timeloop import Timeloop
from datetime import timedelta
import threading

tl = Timeloop()

@tl.job(interval=timedelta(seconds=2))
def func_1():
    t_end = time.time()+ 3
    while time.time() < t_end:
    # while True:
        if time.time() >= t_end:
            break
        t = time.ctime()
        print (f'func_1 {t}')
        

@tl.job(interval=timedelta(seconds=4))
def func_2():
    t_end = time.time()+ 3
    while time.time() < t_end:
    # while True:
        if time.time() >= t_end:
            break
        t = time.ctime()
        print (f'func_2 {t}')
    # return None
       

if __name__ == "__main__":
    tl.start(block=True)
    # while True:
    #     a = func_1()
    #     b = func_2()
    WAIT_TIME_SECONDS = 2

    ticker = threading.Event()
    while not ticker.wait(WAIT_TIME_SECONDS):
        func_1()
        func_2()

