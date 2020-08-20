#!/usr/bin/env python3

from src.core.base.osint import BaseRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Runner(BaseRunner):
    """
    Basic example
    """

    required = []

    def __init__(self, logger: str = __name__):
        """
        Re-init base class instance
        :param logger: logger to use
        """
        super(Runner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        Return basic success response
        :param args: args
        :param kwargs: kwargs
        :return: ScriptResponse message
        """
        return ScriptResponse.success(message="Script finished")
