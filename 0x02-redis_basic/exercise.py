#!/usr/bin/env python3
""" Cache module """
import uuid
from typing import Union, Optional, Callable
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    """ Count calls decorator """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ Call history decorator """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function """
        key = method.__qualname__
        input = str(args)
        self._redis.rpush(f"{key}:inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(f"{key}:outputs", output)
        return output

    return wrapper


def replay(method: Callable):
    """ Replay decorator """
    r = redis.Redis()
    key = method.__qualname__
    count = r.get(key)
    inputs = r.lrange(f"{key}:inputs", 0, -1)
    outputs = r.lrange(f"{key}:outputs", 0, -1)
    print(f"{key} was called {count} times:")
    for i, o in zip(inputs, outputs):
        print(f"{key}(*{i.decode('utf-8')}) -> {o.decode('utf-8')}")


class Cache:
    """ Cache class """
    def __init__(self):
        """ Constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[bytes, str, int, float]) -> str:
        """ Store data in redis """
        r = str(uuid.uuid4())
        self._redis.set(r, data)
        return r

    def get(self, key: str, fn: Optional[Callable] = None) -> \
            Union[bytes, str, int, float]:
        """ Get data from redis """
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ Get string from redis """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """ Get int from redis """
        return self.get(key, fn=int)
