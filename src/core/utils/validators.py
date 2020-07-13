#!/usr/bin/env python3


def validate_kwargs(possible_keys: list) -> callable:
    """
    Validate search keys for the functions and classes
    :param possible_keys: possible keys to search with
    :return: function or raise exception
    """

    def wrap(function):
        def wrapped_function(*args, **kwargs):
            if any(arg not in possible_keys for arg in kwargs.keys()):
                raise KeyError(f"Wrong search key. Possible keys: {possible_keys}")
            return function(*args, **kwargs)

        return wrapped_function

    return wrap
