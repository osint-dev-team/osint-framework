#!/usr/bin/env python3
import requests

from re import search
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
            response = requests.get(url).text
        except Exception as get_err:
            return ScriptResponse.error(result=None, message=str(get_err))

        search_title = search(r"<title>(.*)</title>", response)
        return ScriptResponse.success(
            result=search_title.group(1) if search_title else None,
            message="Title on {url} is: ".format(url=url),
        )
