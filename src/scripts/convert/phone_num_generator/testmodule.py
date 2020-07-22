from random import randint


def rand_num_gen() -> str:
    """
    This should probably be here
    Generates a random number for the test
    :return: string representation of the number
    """
    return "+7" + "".join([str(randint(1, 9)) for _ in range(10)])
