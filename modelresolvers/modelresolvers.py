from typing import Callable


class ModelResolvers:
    def __init__(self):
        self._queries = {}
        self._mutations = {}

    def query(self, name: str | None = None):
        def decorator(func: Callable):
            type_name = name or func.__name__
            self._queries[type_name] = func
            return func

        return decorator

    def mutation(self, name: str | None = None):
        def decorator(func: Callable):
            type_name = name or func.__name__
            self._mutations[type_name] = func
            return func

        return decorator
