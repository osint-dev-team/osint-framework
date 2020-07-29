#!/usr/bin/env python3

"""
Defines base runner for the RECON scripts
"""
from typing import Any

from src.core.utils.validators import validate_kwargs
from src.core.base.base import BaseRunner


class PossibleKeys:
    """
    Defines default values for the function arguments (kwargs, named args)
    """

    KEYS = ["host", "hostname", "ip", "url", "torrent_api_key"]


class ReconRunner(BaseRunner):
    def __init__(self, logger: str = __name__):
        super(ReconRunner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> Any:
        """
        ReconRunner 'run' base implementation
        :param args: some positional args
        :param kwargs: some named args
        :return: None in this case(base class)
        """
        pass
