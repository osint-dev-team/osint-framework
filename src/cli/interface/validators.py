#!/usr/bin/env python3

from sys import version_info, exit, argv
from rich.console import Console


REQUIRED = (3, 7)
REQUIRED_STR = "{}.{}".format(*REQUIRED)


def check_py_version() -> None:
    """
    This function checks a python version to be
    sure that all of the features will be supported.
    :return: None
    """
    if version_info < REQUIRED:
        console = Console()
        console.print(
            f"Required python version: {REQUIRED_STR} or newer. "
            f"Your version is: {version_info.major}.{version_info.minor}",
            style="red",
        )
        exit(1)


def check_arg_length() -> None:
    """
    This function checks length of the arguments
    :return: None
    """
    if len(argv) == 1:
        console = Console()
        console.print(f"usage: main.py [-h] [-s SCENARIO]", style="red")
        exit(1)
