#!/usr/bin/env python3

"""
Set default values
"""

from random import randrange


class TestDefaults:
    HOST = "127.0.0.1"
    DOWN_TIMEOUT = 0.1
    PORT_RANGE = (20_000, 65_535)
    PORT = None

    def __init__(self, host: str or None = None, down_timeout: float or None = None) -> None:
        """
        Init random port
        :param host: host to set
        :param down_timeout: down timeout to set
        """
        if host:
            self.HOST = host
        if down_timeout:
            self.DOWN_TIMEOUT = down_timeout
        self.PORT = self.generate_port()

    @classmethod
    def generate_port(cls, port_range: tuple = PORT_RANGE):
        """
        Generates random port
        :param port_range: range in format (first, second)
        :return: random number from range
        """
        return randrange(*port_range)
