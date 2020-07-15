#!/usr/bin/env python3

from requests import request
from requests.exceptions import ConnectionError

from src.core.base.recon import ReconRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Defaults:
    # List of the Request Methods Recognized by Apache
    METHODS: list = [
        "GET",
        "PUT",
        "POST",
        "DELETE",
        "CONNECT",
        "OPTIONS",
        "TRACE",
        "PATCH",
        "PROPFIND",
        "PROPPATCH",
        "MKCOL",
        "COPY",
        "MOVE",
        "LOCK",
        "UNLOCK",
        "VERSION_CONTROL",
        "CHECKOUT",
        "UNCHECKOUT",
        "CHECKIN",
        "UPDATE",
        "LABEL",
        "REPORT",
        "MKWORKSPACE",
        "MKACTIVITY",
        "BASELINE_CONTROL",
        "MERGE",
        "INVALID",
    ]


class Runner(ReconRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs):
        """
        Returns list of allowed methods. E.g. ['GET', 'POST'].
        Also checks if method is forbidden or somehow filtered.
        Needs url to run.
        :param args: args from core runner
        :param kwargs: kwargs from core runner
        :return: ScriptResponse message
        """
        allowed_methods = []
        filtered_methods = []
        forbidden_methods = []
        url = kwargs.get("url")

        for method in Defaults.METHODS:
            try:
                status = request(method, url).status_code

                # 2xx - success
                # 405 - method not allowed
                if 200 <= status < 300:
                    allowed_methods.append(method)
                elif status == 405:
                    forbidden_methods.append(method)
                else:
                    filtered_methods.append((method, status))
            except ConnectionError:
                pass

        return ScriptResponse.success(
            result=allowed_methods,
            message=f"Url: {url}\nAllowed: {allowed_methods}\nForbidden: {forbidden_methods}\nFiltered: {filtered_methods}",
        )
