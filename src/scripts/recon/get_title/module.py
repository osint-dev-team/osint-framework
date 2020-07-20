#!/usr/bin/env python3
import requests

from src.core.base.recon import ReconRunner
from src.core.utils.response import ScriptResponse


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
        response = None
        result = "None title or Bad url"
        try:
            response = requests.get(url)
        except:
            pass
        if response is None:
            return ScriptResponse.success(
                result=result, message="Title on {url} is: ".format(url=url)
            )
        response = response.text
        if response.find("<title>") != -1 and response.find("</title>") != -1:
            try:
                result = response[
                    response.find("<title>") + 7 : response.find("</title>")
                ]
            except:
                pass
        return ScriptResponse.success(
            result=result, message="Title on {url} is: ".format(url=url)
        )