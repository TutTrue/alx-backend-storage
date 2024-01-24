#!/usr/bin/env python3
""" Cache module """
import uuid
from typing import Union, Optional, Callable
import redis


class Cache:
    """ Cache class """
    def __init__(self):
        """ Constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()


    def store(self, data: Union[bytes, str, int, float]) -> str:
        """ Store data in redis """
        r = str(uuid.uuid4())
        self._redis.set(r, data)
        return r


    def get(self, key: str, fn: Optional[Callable] = None) -> Union[bytes, str, int, float]:
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
