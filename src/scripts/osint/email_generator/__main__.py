#!/usr/bin/env python3
from time import time
from src.scripts.osint.email_generator import EmailGenerator
from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Runner(OsintRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        Main runner function for the script
        :param args: args from core runner
        :param kwargs: kwargs from core runner
        :return: ScriptResponse message
        """
        try:
            # to work normally you need to give a limit, because max size may be over a billion
            # to reduce the value, you can help me better dividing username into lexems
            tm = time()
            emailgen = EmailGenerator(limit=100_000)
            username = kwargs.get("username")
            if username is None:
                raise KeyError("EmailGenerator can't work without username!")
            result = list(emailgen.Generate(username))
        except Exception as err:
            ScriptResponse.error(message=str(err))
        else:
            return ScriptResponse.success(
                result=result, message="Successfully finished! script lasted {:.2f} seconds".format(time() - tm)
            )
