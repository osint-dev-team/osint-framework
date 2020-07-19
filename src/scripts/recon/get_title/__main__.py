#!/usr/bin/env python3
import requests

from src.core.base.recon import ReconRunner
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Runner(ReconRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    def run(self, *args, **kwargs):
        """
        Try to find http title
        :param args: args from core runner
        :param kwargs: kwargs from core runner
        :return: http title if it's exist
        """
        url = kwargs.get("url")
        response = requests.get(url)
        response = response.text
        result = "None title"
        try:
            result = response[response.find('<title>') + 7: response.find('</title>')]
        except:
            pass
        return ScriptResponse.success(
            result=result, message="Title on {url} is: ".format(url=url)
        )
