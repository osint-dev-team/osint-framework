#!/usr/bin/env python3

from src.core.base.recon import ReconRunner
from src.core.utils.response import ScriptResponse
from requests import get
from requests.utils import CaseInsensitiveDict


class Runner(ReconRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @staticmethod
    def __get_host(hostname: str) -> CaseInsensitiveDict:
        """
        Get host headers
        :param hostname: hostname to check
        :return: dictionary with headers
        """
        return get(hostname).headers

    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        Main runner function for the script
        :param args: args from core runner
        :param kwargs: kwargs from core runner
        :return: ScriptResponse message
        """
        hostname = kwargs.get("hostname")
        return ScriptResponse.success(
            result=self.__get_host(hostname), message="Success"
        )
