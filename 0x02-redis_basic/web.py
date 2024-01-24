#!/usr/bin/env python3
""" get_page """
from typing import Callable
from functools import wraps
import requests
import redis

redis = redis.Redis()


def count(method: Callable) -> Callable:
    """ count """
    @wraps(method)
    def wrapper(url):
        """ wrapper """
        redis.incr(f"count:{url}")
        cached = redis.get(f"cached:{url}")
        if cached:
            return cached.decode('utf-8')
        res = method(url)
        redis.set(f"count:{url}", 0)
        redis.setex(f"cached:{url}", 10, res)
        return res
    return wrapper


@count
def get_page(url: str) -> str:
    """ get_page """
    return requests.get(url).text
