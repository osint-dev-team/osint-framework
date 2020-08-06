#!/usr/bin/env python3

from src.core.base.recon import ReconRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs
from requests import get
from http import cookiejar


class Runner(ReconRunner):
    """
    Class that performs cookie flags checking.
    """
    required = ["url"]

    def __init__(self, logger: str = __name__):
        """
        Re-init base class instance with this function.
        Simply put, you need to provide proper logger name
        to the parent class, so please, save this structure for
        the init function.
        :param logger: logger to use (name of _this_ runner by default)
        """
        super(Runner, self).__init__(logger)

    @staticmethod
    def __has_http_only(cookie: cookiejar.Cookie) -> bool:
        """
        Checks the specified cookie
        for the HttpOnly flag.
        :param cookie: Cookie for Checking
        :return: True if there is
        HttpOnly flag.
        """
        extra_args = cookie.__dict__.get("_rest")

        if not extra_args:
            return False

        return any(key.lower() == "httponly" for key in extra_args.keys())

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        Checks Secure, HttpOnly, Prefixed,
        Same-site flags for the
        cookies of a specified URL.
        :param args: args from core runner
        :param kwargs: kwargs from core runner
        :return: ScriptResponse with dictionary
        containing flags mentioned above.
        """

        url = kwargs.get("url")

        if not url:
            return ScriptResponse.error(message="Url was not provided!")

        result = {}

        response = get(url)
        for cookie in response.cookies:
            result[cookie.name] = {
                "Path": cookie.path,
                "Secure": cookie.secure,
                "HttpOnly": self.__has_http_only(cookie),
                "Prefix": cookie.name.startswith(("__Secure-", "__Host-"))
                if cookie.name
                else False,
                "Same-Site": cookie.__dict__.get("_rest").get("SameSite", "None"),
            }

        return ScriptResponse.success(
            result=result,
            message=f"Successfully finished cookie policy check for {url}",
        )
