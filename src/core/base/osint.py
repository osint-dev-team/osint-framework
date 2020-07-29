#!/usr/bin/env python3

"""
Defines base runner for the OSINT scripts
"""
from typing import Any

from src.core.base.base import BaseRunner
from src.core.utils.validators import validate_kwargs


class PossibleKeys:
    """
    Defines default values for the function arguments (kwargs, named args)
    """

    KEYS = ["email", "username", "fullname", "vk_api_key", "phone", "region"]


class OsintRunner(BaseRunner):
    def __init__(self, logger: str = __name__):
        super(OsintRunner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> Any:
        """
        OsintRunner 'run' base implementation
        :param args: some positional args
        :param kwargs: some named args
        :return: None in this case(base class)
        """
        pass
