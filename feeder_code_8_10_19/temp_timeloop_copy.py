import time
from datetime import timedelta
import threading
from ipyparallel import Client


rc = Client()


# def foo():
#     import time
#     time.sleep(5)
#     return 'foo'

# def bar():
#     import time
#     time.sleep(10) 
#     return 'bar'  


# def func_1():
#     import time
#     t_end = time.time()+ 3
#     while time.time() < t_end:
#     # while True:
#         if time.time() >= t_end:
#             break
#         t = time.ctime()
#         return f'func_1 {t}'
        

# def func_2():
#     import time
#     t_end = time.time()+ 63
#     while time.time() < t_end:
#     # while True:
#         if time.time() >= t_end:
#             break
#         t = time.ctime()
#         return f'func_2 {t}'
    # return None


def func_1():
    import time
    # time.sleep(3)
    t = time.ctime()
    return f'func_1 {t}'
        

def func_2():
    import time
    time.sleep(5)
    t = time.ctime()
    return f'func_2 {t}'


def call_func_1():
    t_end = time.time()+ 5
    if time.time() >= t_end:
        return None
    while time.time() < t_end:
        t = time.ctime()
        res1 = rc[0].apply(func_1)
        print (res1.get())

def call_func_2():
    t_end = time.time()+ 10
    if time.time() >= t_end:
        return None
    while time.time() < t_end:
        t = time.ctime()
        res2 = rc[1].apply(func_2)
        print (res2.get())
       

if __name__ == "__main__":
    while True:
        call_func_1()
        call_func_2()

        # res1 = rc[0].apply(func_1)
        # res2 = rc[1].apply(func_2)
        # results = [res1, res2]

        # while not all(map(lambda ar: ar.ready(), results)):
        #     pass

        # print(res1.get(), res2.get())
    
    # while True:
    #     a = func_1()
    #     b = func_2()
    # WAIT_TIME_SECONDS = 2

    # ticker = threading.Event()
    # while not ticker.wait(WAIT_TIME_SECONDS):
    #     func_1()

