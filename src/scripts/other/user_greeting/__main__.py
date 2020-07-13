#!/usr/bin/env python3

from src.core.base.osint import BaseRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Runner(BaseRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @staticmethod
    def user_greeting(user: str = "Unknown") -> str:
        """
        Simple example function for user greeting
        :param user: name of the user to check
        :return: greeting message
        """
        return f"Hello, {user}!"

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        Main runner function for the script
        :param args: args from core runner
        :param kwargs: kwargs from core runner
        :return: ScriptResponse message
        """
        result = self.user_greeting(user=kwargs.get("username"))
        if not result:
            return ScriptResponse.success(message="Sorry, no greetings for this user!")
        return ScriptResponse.success(
            result=result,
            message=f"Successfully finished! (args: {args}, kwargs: {kwargs})",
        )


if __name__ == "__main__":
    script_module = Runner()
    script_result = script_module.run()
    print(script_result)
