#!/usr/bin/env python3

from base64 import encodebytes

from mmh3 import hash
from requests import get
from requests.exceptions import RequestException

from src.core.base.recon import ReconRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Runner(ReconRunner):
    """
    Class that generates Shodan favicon mmh3 hash
    """
    required = ["url"]

    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs):
        """
        Returns hash of favicon.ico of given url.
        :param args: args from core runner
        :param kwargs: kwargs from core runner
        :return: ScriptResponse message
        """
        url = kwargs.get("url")

        try:
            response = get(f"{url}/favicon.ico")
        except RequestException as req_err:
            return ScriptResponse.error(
                result=None,
                message=f"Can't connect to {url}!" f"Error message: {req_err}",
            )

        favicon = encodebytes(response.content)
        favicon_hash = hash(favicon)

        return ScriptResponse.success(
            result=favicon_hash,
            message=f"Successfully made favicon hash of {url}! "
            f"Use https://www.shodan.io/search?query=http.favicon.hash:{favicon_hash}",
        )
