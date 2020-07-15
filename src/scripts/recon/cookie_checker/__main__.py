from src.core.base.recon import ReconRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs
from requests import get


class Runner(ReconRunner):
    """
    Class that performs cookie flags checking.
    """

    def __init__(self, logger: str = __name__):
        """
        Re-init base class instance with this function.
        Simply put, you need to provide proper logger name
        to the parent class, so please, save this structure for
        the init function.
        :param logger: logger to use (name of _this_ runner by default)
        """
        super(Runner, self).__init__(logger)

    def __has_http_only(self, cookie):
        """
        Checks the specified cookie
        for the HttpOnly flag.
        :param cookie: Cookie for Checking
        :return: True if there is
        HttpOnly flag.
        """
        extra_args = cookie.__dict__.get("_rest")
        if extra_args:
            for key in extra_args.keys():
                if key.lower() == "httponly":
                    return True

        return False

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

        url = kwargs.get("url", "")

        result = {}

        if url == "":
            return ScriptResponse.error(message="Url was not provided!")

        response = get(kwargs["url"])
        cookies = response.cookies

        for i in cookies:
            result[i.name] = {}
            result[i.name]["Path"] = i.path
            result[i.name]["Secure"] = i.secure
            result[i.name]["HttpOnly"] = self.__has_http_only(i)
            result[i.name]["Prefix"] = i.name.startswith(("__Secure-", "__Host-"))
            result[i.name]["Same-Site"] = i.__dict__.get("_rest").get("SameSite", None)

        return ScriptResponse.success(
            result=result,
            message=f"Successfully finished cookie policy check for {url}",
        )
