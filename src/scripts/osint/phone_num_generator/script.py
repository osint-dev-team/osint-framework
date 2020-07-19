#!/usr/bin/env python3

import random


def rand_num_gen():
    # генерирует случайный номер для теста
    # args: none
    # return: 11-digit number
    ans = '8'
    for i in range(1, 11):
        ans += str(random.randint(1, 9))
    return ans


def normalise(phone_num):
    # приводит любой номер в определенный формат - 7xxxxxxxxxxx
    # args: номер для нормализации в виде строки
    # return: 7xxxxxxxxxxx
    numbers = [digit for digit in phone_num if digit.isdigit()]
    norm_num = "".join(numbers)
    if len(norm_num) == 11:
        norm_num = '7' + norm_num
    return norm_num


def gen_all(norm_num):
    # генерирует все возможные варианты написания
    # args: нормализированный номер
    # return: список строк номеров
    number_groups = [norm_num[0], norm_num[1:4], norm_num[4:7], norm_num[7:9], norm_num[9:11]]
    num_list = []
    separators = ["", "-", "."]
    for sep in separators:  # автоматизированный процесс для некоторых
        num_list.append(sep.join(number_groups))
        num_list.append("+" + sep.join(number_groups))
    # отдельный пример вне цикла
    num_list.append(
        number_groups[0] + "(" + number_groups[1] + ")" + number_groups[2] + number_groups[3] + number_groups[4])
    num_list.append(
        "+" + number_groups[0] + "(" + number_groups[1] + ")" + number_groups[2] + number_groups[3] + number_groups[4])

    return num_list


# тест для проверки кода
def test():
    rand_number_test = rand_num_gen()
    normal_num = normalise(rand_number_test)
    final_list = gen_all(normal_num)
    print(final_list)
    # этот цикл чтобы убедиться, что нормализатор работает на любых форматах
    for number in final_list:
        print(normalise(number))
