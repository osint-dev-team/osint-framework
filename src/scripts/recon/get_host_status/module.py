#!/usr/bin/env python3

from src.core.base.recon import ReconRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs
from requests import get


class Runner(ReconRunner):
    """
    Class that performs host status check
    """
    required = ["url"]

    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs):
        """
        Returns HTTP response status code
        :param args: args from core runner
        :param kwargs: kwargs from core runner
        :return: ScriptResponse message
        """
        url = kwargs.get("url")
        status = get(url=url).status_code
        return ScriptResponse.success(
            result=status, message=f"Got HTTP response status from {url}"
        )
