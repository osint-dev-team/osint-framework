#!/usr/bin/env python3


def run_module(
    runner: type, args: list, arg_name: str, arg_default: str or None = None
) -> dict:
    """
    Use module as a 'python3 -m ...' module
    :param runner: runner object
    :param args: list of args from CLI
    :param arg_name: name of arg to use
    :param arg_default: default arg value
    :return: results
    """
    runner = runner()
    return runner.run(**{arg_name: args[1] if len(args) >= 2 else arg_default})
