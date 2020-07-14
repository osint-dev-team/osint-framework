#!/usr/bin/env python3

"""
Defines base runner
"""
from logging import getLogger
from typing import Any


class BaseRunner:
    """
    Defines base runner class to create childs from
    """

    def __init__(self, logger: str = __name__):
        """
        Initialize the base class
        :param logger: logger name
        """
        self.log = getLogger(name=logger)
        self.log.info("script started")

    def run(self, *args, **kwargs) -> Any:
        """
        Base run method
        :param args: some positional args
        :param kwargs: some named args
        :return: None in this case (base class)
        """
        pass
