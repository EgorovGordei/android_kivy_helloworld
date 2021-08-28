import time


class Timer:
    def __init__(self, waiting_time, func):
        self.func = func
        self.waiting_time = waiting_time
        self.canceled = False

    def cancel(self):
        self.canceled = True
        print("Canceling")

    def start(self):
        time.sleep(self.waiting_time)
        print("Timer starting", self.canceled)
        if not self.canceled:
            self.func()


def in_new_thread(function):
    from functools import wraps
    wraps(function)
    def wrapper(*args, **kwargs):
        from threading import Thread
        t = Thread(target=function, args=args, kwargs=kwargs)
        name = "Thread - {} (args={}, kwargs={})".format(function.__name__,
                                                         args, kwargs)
        t.setName(name)
        t.start()
    wrapper.__name__ = "in_new_thread({}).wrapper".format(function.__name__)
    return wrapper
