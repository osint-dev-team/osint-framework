#!/usr/bin/env python3
import requests
from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Runner(OsintRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @staticmethod
    def tel_region(number: str = "Unknown") -> str:
        """
        Region recognition using the phone number
        :param number: phone number to check
        :return: information about the region and the operator
        """
        response = requests.get('https://eduscan.net/help/phone_ajax.php?', params={'num': number})
        return response.text

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        Main runner function for the script
        :param args: args from core runner
        :param kwargs: kwargs from core runner
        :return: ScriptResponse message
        """
        result = self.tel_region(number=kwargs.get("number"))
        if len(result) == 15:
            return ScriptResponse.error(message="Sorry, no such number!")
        return ScriptResponse.success(
            result=result.split('~')[-1],
            message=f"Successfully finished! (args: {args}, kwargs: {kwargs})",
        )


if __name__ == "__main__":
    script_module = Runner()
    script_result = script_module.run()
    print(script_result)