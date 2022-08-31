from threading import Thread


def threaded(func):
    def wrapper(*args, **kwargs):
        Thread(target=func, args=args, kwargs=kwargs, daemon=True).start()

    return wrapper
