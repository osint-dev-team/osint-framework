#!/usr/bin/env python3
from phonenumbers import NumberParseException, parse, format_number, PhoneNumberFormat

from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Runner(OsintRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @staticmethod
    def __gen_all(formatted_num: str) -> [str]:
        """
        Generates all possible variants of number formats
        :param formatted_num: formatted number
        :return: the list of all formats
        """
        number_groups = formatted_num.split(" ")
        num_list = [formatted_num]
        separators = ["", "-", "."]
        # Automate some separation formats of numbers
        for sep in separators:
            joined = sep.join(number_groups)
            num_list.append(joined)
        phone_w_brackets = "{prefix}({code}){rest}".format(
            prefix=number_groups[0],
            code=number_groups[1],
            rest="".join(number_groups[2:])
        )
        num_list.append(phone_w_brackets)
        return num_list

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        Main runner function for the script
        :param args: args from core runner
        :param kwargs: kwargs from core runner
        :return: ScriptResponse message
        """
        try:
            phone = kwargs.get("phone")
            parsed_num = parse(phone, None)
        except NumberParseException:
            return ScriptResponse.error(result=None, message="Not viable number or not international format")
        except Exception:
            return ScriptResponse.error(result=None, message="Something went wrong!")
        try:
            result = self.__gen_all(format_number(parsed_num, PhoneNumberFormat.NATIONAL)) + \
                     self.__gen_all(format_number(parsed_num, PhoneNumberFormat.INTERNATIONAL)) + \
                     [format_number(parsed_num, PhoneNumberFormat.E164)]
            result = list(dict.fromkeys(result))
        except Exception:
            return ScriptResponse.error(result=None, message="Something went wrong!")

        return ScriptResponse.success(
            result=result,
            message=f"All possible number formats for phone number {phone}",
        )


if __name__ == "__main__":
    script_module = Runner()
    script_result = script_module.run()
    print(script_result)
