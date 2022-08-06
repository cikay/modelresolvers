from typing import Callable


class ModelResolvers:
    def __init__(self):
        self._queries = {}
        self._mutations = {}

    def query(self, name: str | None = None):
        def decorator(func: Callable):
            type_ = name or func.__name__
            self._queries[type_] = func

        return decorator

    def mutation(self, name: str | None = None):
        def decorator(func: Callable):
            type_ = name or func.__name__
            self._mutations[type_] = func

        return decorator
