import time
from threading import Thread

from game import game_cycle


def cycled_factory(interval: int, cycle: game_cycle):
    def cycled(func: callable) -> callable:
        def wrapper(*args, **kwargs) -> None:
            def do_cycle(*_args, **_kwargs) -> None:
                while cycle.running:
                    func(*_args, **_kwargs)
                    time.sleep(interval)

            Thread(target=do_cycle, args=args, kwargs=kwargs).start()

        return wrapper

    return cycled


def threaded(func: callable) -> callable:
    def wrapper(*args, **kwargs) -> None:
        Thread(target=func, args=args, kwargs=kwargs, daemon=True).start()

    return wrapper
