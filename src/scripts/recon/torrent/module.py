#!/usr/bin/env python3

from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs
from json import loads
from requests import get


class Defaults:
    API_KEY = "cc351c5a2a2c4e5ca8f215ed98200902"


class Runner(OsintRunner):
    """
    Runner class is used for parsing torrents by ip.
    """

    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        Parses torrents by ip.
        :param args: args from core runner.
        :param kwargs: kwargs from core runner.
        :return: ScriptResponse with dictionary of torrents.
        """
        ip = kwargs.get("ip")
        api_key = kwargs.get("torrent_api_key", Defaults.API_KEY)
        if not ip:
            return ScriptResponse.error(message="No IP was provided")
        response = get(f"https://api.antitor.com/history/peer/?ip={ip}&key={api_key}").json()
        return ScriptResponse.success(
            message=f"Script finished for {ip}", result=response
        )
