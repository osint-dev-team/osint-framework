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
        try:
            response = requests.get(url, verify=False).text
        except Exception as get_err:
            return ScriptResponse.error(result=None, message=str(get_err))

        search_title = search(r"<title>(.*)</title>", response)
        result = search_title.group(1) if search_title else None
        return ScriptResponse.success(
            result=result,
            message=f"Successfully found the title for {url}"
            if result
            else "Can not get the title or bad url",
        )
