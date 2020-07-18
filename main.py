#!/usr/bin/env python3

"""
Main runner.

Please, for all the searches, use the following classes:
'BaseCase', 'OsintCase', 'ReconCase'
"""


from pprint import pprint

from src.core.case.osint import OsintCase
from src.core.case.recon import ReconCase
from src.core.case.base import BaseCase
from src.core.utils.log import Logger


logger = Logger.get_logger(name="osint-framework")


def run_case(case_class: type, *args, **kwargs):
    """
    Define and smoke run the BaseCase
    :param case_class: original class of the case
    :param args: some args
    :param kwargs: some kwargs
    :return: result of the execution
    """
    logger.info(f"start {case_class.__name__} case processing")
    case = case_class()
    case.process(*args, **kwargs)
    return case.get_results()


if __name__ == "__main__":
    # fmt: off
    base_case = run_case(case_class=BaseCase, username="johndoe", email="johndoe@gmail.com", fullname="John Doe")
    osint_case = run_case(case_class=OsintCase, username="johndoe", email="johndoe@gmail.com", fullname="John Doe")
    recon_case = run_case(case_class=ReconCase, url="https://facebook.com")

    pprint(base_case)
    pprint(osint_case)
    pprint(recon_case)
    # fmt: on
