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


if __name__ == "__main__":
    # Will return 2 results from "other" category scripts
    other_case = BaseCase()
    other_case.process(
        username="johndoe", email="johndoe@gmail.com", fullname="John Doe",
    )
    other_case_results = other_case.get_results()

    # Will return 1 result from "recon" category scripts
    recon_case = ReconCase()
    recon_case.process(url="https://facebook.com")
    recon_case_results = recon_case.get_results()

    # Will return nothing (no scripts for now, sorry!)
    osint_case = OsintCase()
    osint_case.process(username="any_value_here")
    osint_case_results = osint_case.get_results()

    # Print out all the results
    for result in other_case_results, recon_case_results, osint_case_results:
        pprint(result)
