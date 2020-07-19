#!/usr/bin/env python3
from phonenumbers import NumberParseException, parse

from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs
from random import randint
import phonenumbers






#
# def test():
#     """
#     Test function to check the code
#     """
#     rand_number_test = rand_num_gen()
#     normal_num = normalise(rand_number_test)
#     final_list = gen_all(normal_num)
#     print(final_list)
#     # this loop just proves that the normaliser works correctly
#     for number in final_list:
#         print(normalise(number))
#
#
#test()
#
# x = phonenumbers.parse("+442083661177", None)


class Runner(OsintRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @staticmethod
    def rand_num_gen() -> str:
        """
        I don't think we need this anymore
        Generates a random number for the test
        :return: string representation of the number
        """
        return "+7" + "".join([str(randint(1, 9)) for _ in range(10)])

    @staticmethod
    def __gen_all(parsed_num: str) -> [str]:
        """
        Generates all possible variants of number formats
        :param parsed_num: parsed number
        :return: the list of all formats
        """
        number_groups = parsed_num.split(" ")
        num_list = [parsed_num]
        separators = ["", "-", "."]
        # Automate some separation formats of numbers
        for sep in separators:
            joined = sep.join(number_groups)
            num_list.extend((joined, f"+{joined}"))
        phone_w_brackets = "{prefix}({code}){rest}".format(
            prefix=number_groups[0],
            code=number_groups[1],
            rest="".join(number_groups[2:])
        )
        num_list.extend((phone_w_brackets, f"+{phone_w_brackets}"))
        return num_list

    @staticmethod
    def __phone_number_list(self, parsed_num: str) -> [str]:
        return self.__gen_all(phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.NATIONAL)) + \
               self.__gen_all(phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.INTERNATIONAL)) +\
               self.__gen_all(phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.E164))


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
            parsed_number = parse(phone)
        except NumberParseException:
            return ScriptResponse.error(result=None, message="Not viable number or not international format")
        try:
            result = self.__phone_number_list(parsed_number)
        except Exception:
            return ScriptResponse.error(result=None, message="Something went wrong!")

        return ScriptResponse.success(
            result=result,
            message=f"All possible number formats: {result} | for phone number {phone}",
        )


if __name__ == "__main__":
    script_module = Runner()
    script_result = script_module.run()
    print(script_result)
