#!/usr/bin/env python3

from redis import Redis
from os import environ


class DefaultValues:
    # 24 hrs
    REDIS_TIMEOUT = 86400
    REDIS_HOST = environ.get("REDIS_HOST", default="localhost")


class RedisCache:
    def __init__(
        self,
        host: str = DefaultValues.REDIS_HOST,
        timeout: int = DefaultValues.REDIS_TIMEOUT,
    ):
        self.options = dict(timeout=timeout)
        self.redis = Redis(host=host)

    def get(self, key) -> dict or list:
        """
        Return redis cache value
        :param key: key to get
        :return: cache
        """
        if self.exists(key):
            return self.redis.get(key)
        return None

    def set(self, key, value, timeout=None) -> None:
        """
        Set redis cache value
        :param key: key to set
        :param value: value to set
        :param timeout: timeout to live
        :return: None
        """
        self.redis.set(key, value)
        if timeout:
            self.redis.expire(key, timeout)
        else:
            self.redis.expire(key, self.options["timeout"])

    def delitem(self, key) -> None:
        """
        Delete cache value
        :param key: key to delete
        :return: None
        """
        self.redis.delete(key)

    def exists(self, key) -> bool:
        """
        Check if value exists
        :param key: key to check
        :return: bool
        """
        return bool(self.redis.exists(key))
