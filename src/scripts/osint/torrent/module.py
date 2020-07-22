#!/usr/bin/env python3

# Import any required runner
# 1. OsintRunner - for OSINT scripts
# 2. ReconRunner - for RECON scripts
# 3. BaseRunner - for out-of-scope scripts ("other")
from src.core.base.osint import OsintRunner, BaseRunner, PossibleKeys

# Import 'ScriptResponse' to return good responses from the module, like
# 1. ScriptResponse.success - if everything is good
# 2. ScriptResponse.error - if everything is bad
from src.core.utils.response import ScriptResponse

# Validate your named arguments. For example, this validator
# will raise 'KeyError' if you will try to put 'hostname' argument
# into the 'OsintRunner' runner, and so on
from src.core.utils.validators import validate_kwargs
from json import loads
from requests import get


class Defaults:
    API_KEY = "cc351c5a2a2c4e5ca8f215ed98200902"


# You can use OsintRunner, ReconRunner or BaseRunner as the base class
class Runner(OsintRunner):
    """
    Basic script example
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

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        The main '.run()' function to run your script.
        Note: this function is always synchronous, without any
        async/await init. You can use 'asyncio.run(...)' here,
        but don't put any 'async' before function definition
        :param args: args that you provide (not used for now)
        :param kwargs: kwargs that you provide (required to run something!)
        :return: ScriptResponse message (error or success)
        """
        ip = kwargs.get("ip")
        api_key = kwargs.get("torrent_api_key", Defaults.API_KEY)
        if not ip:
            return ScriptResponse.error(message="No IP was provided")
        response = get(f"https://api.antitor.com/history/peer/?ip={ip}&key={api_key}")
        torrents_dict = loads(response.text)
        return ScriptResponse.success(
            message=f"Script finished for {ip}", result=torrents_dict
        )
