#!/usr/bin/env python3

from requests import request
from requests.exceptions import RequestException

from src.core.base.recon import ReconRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs

from string import ascii_uppercase
from random import seed, choice, randint


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


def get_random_method():
    seed()
    letters = ascii_uppercase
    length = randint(6, 10)
    method = "".join(choice(letters) for i in range(length))
    return method


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

        # Copy original methods list to avoid class variable modifications
        methods = list(Defaults.METHODS)

        # Append random method to check if server is not faking.
        methods.append(get_random_method())

        for method in methods:
            try:
                status = request(method, url).status_code
                method_result = {"method": method, "status": status}

                # 2xx - success
                # 405 - method not allowed
                if 200 <= status < 300:
                    allowed_methods.append(method_result)
                elif status == 405:
                    forbidden_methods.append(method_result)
                else:
                    filtered_methods.append(method_result)
            except RequestException:
                pass

        return ScriptResponse.success(
            result={
                "allowed": allowed_methods,
                "forbidden": forbidden_methods,
                "filtered": filtered_methods,
            },
            message=f"URL: {url} - "
                    f"allowed: {len(allowed_methods)}, "
                    f"forbidden: {len(forbidden_methods)}, "
                    f"filtered: {len(filtered_methods)}",
        )
