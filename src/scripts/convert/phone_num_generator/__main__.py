#!/usr/bin/env python3

from random import randint
import phonenumbers

def rand_num_gen() -> str:
    """
    Generates a random number for the test
    :return: string representation of the number
    """
    return "8" + "".join([str(randint(1, 9)) for _ in range(10)])


def normalise(phone_num: str) -> str:
    """
    Converts the given number to a normalised Russian area format
    :param phone_num: phone number to be converted
    :return: normalised phone number as a string
    """
    numbers = [digit for digit in phone_num if digit.isdigit()]
    norm_num = "".join(numbers)
    if len(norm_num) == 11:
        norm_num = '7' + norm_num
    return norm_num


def gen_all(norm_num: str) -> [str]:
    """
    Generates all possible variants of number formats
    :param norm_num: normalised number
    :return: the list of all formats
    """
    number_groups = [norm_num[first: second] for first, second in [(0, 1), (1, 4), (4, 7), (7, 9), (9, 11)]]
    num_list = []
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


def test():
    """
    Test function to check the code
    """
    rand_number_test = rand_num_gen()
    normal_num = normalise(rand_number_test)
    final_list = gen_all(normal_num)
    print(final_list)
    # this loop just proves that the normaliser works correctly
    for number in final_list:
        print(normalise(number))


#test()

x = phonenumbers.parse("+442083661177", None)
print(x)

