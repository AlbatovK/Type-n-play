from threading import Thread

from game import game_cycle


def cycled_factory(cycle: game_cycle):
    def cycled(func: callable) -> callable:
        def wrapper(*args, **kwargs) -> None:
            @threaded
            def do_cycle(*_args, **_kwargs) -> None:
                while cycle.running:
                    func(*_args, **_kwargs)

            do_cycle(*args, **kwargs)

        return wrapper

    return cycled


def threaded(func: callable) -> callable:
    def wrapper(*args, **kwargs) -> None:
        def timed(*_args, **_kwargs):
            func(*_args, **_kwargs)

        Thread(target=timed, args=args, kwargs=kwargs, daemon=True).start()

    return wrapper
