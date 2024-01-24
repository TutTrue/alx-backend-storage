#!/usr/bin/env python3
""" Cache module """
import uuid
import redis


class Cache:
    """ Cache class """
    def __init__(self):
        """ Constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()


    def store(self, data: bytes) -> str:
        """ Store data in redis """
        r = str(uuid.uuid4())
        self._redis.set(r, data)
        return r
        