import time
from threading import Thread

from game import game_cycle


def cycled_factory(cycle: game_cycle):
    def cycled(func: callable) -> callable:
        def wrapper(*args, **kwargs) -> None:
            @threaded
            def do_cycle(*_args, **_kwargs) -> None:
                while cycle.running:
                    start = time.time()
                    func(*_args, **_kwargs)
                    print(time.time() - start, func.__name__)

            do_cycle(*args, **kwargs)

        return wrapper

    return cycled


def threaded(func: callable) -> callable:
    def wrapper(*args, **kwargs) -> None:
        def timed(*_args, **_kwargs):
            start = time.time()
            func(*_args, **_kwargs)
            print(time.time() - start, func.__name__)

        Thread(target=timed, args=args, kwargs=kwargs, daemon=True).start()

    return wrapper
