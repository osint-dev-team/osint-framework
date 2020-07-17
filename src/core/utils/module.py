#!/usr/bin/env python3

from sys import argv
from src.core.base import base


def run_module(module: base, args: list, arg_name: str, arg_value: str or None = None) -> dict:
    """
    Use module as a 'python3 -m ...' module
    :param module: module object
    :param args: list of args from CLI
    :param arg_name: name of arg to use
    :param arg_value: default arg value
    :return: results
    """
    runner = module.Runner()
    try:
        arg_value = args[1]
    except:
        pass
    return runner.run(**{arg_name: arg_value})
