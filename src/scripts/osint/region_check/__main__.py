#!/usr/bin/env python3

import requests

from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Runner(OsintRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @staticmethod
    def __phone_to_region(phone: str = "Unknown") -> str:
        """
        Region recognition using the phone number
        :param phone: phone number to check
        :return: information about the region and the operator
        """
        response = requests.get(
            "https://eduscan.net/help/phone_ajax.php", params={"num": phone}
        )
        return response.text

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        Main runner function for the script
        :param args: args from core runner
        :param kwargs: kwargs from core runner
        :return: ScriptResponse message
        """
        try:
            result = self.__phone_to_region(phone=kwargs.get("phone"))
        except Exception:
            return ScriptResponse.error(result=None, message="Something went wrong!")
        result = result.split("~")
        if result[1] != "0":
            return ScriptResponse.success(result=None, message="Sorry, no such number!")
        return ScriptResponse.success(
            result=(result[-1], result[-2]),
            message=f"Found region: {result[-1]} | found operator: {result[-2]} | for phone number {result[0]}",
        )


if __name__ == "__main__":
    script_module = Runner()
    script_result = script_module.run()
    print(script_result)
