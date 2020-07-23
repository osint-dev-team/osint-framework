#!/usr/bin/env python3

"""
Main runner.

Please, for all the searches, use the following classes:
'BaseCase', 'OsintCase', 'ReconCase'
"""

from src.core.runner.manager import CaseManager
from pprint import pprint


if __name__ == "__main__":
    # fmt: off
    cases = [
        {
            "case": "base",
            "kwargs": {
                "username": "testname",
                "email": "testmail@gmail.com",
                "fullname": "Test Name"
            }
        },
        {
            "case": "osint",
            "kwargs": {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "fullname": "John Doe"
            }
        },
        {
            "case": "recon",
            "kwargs": {
                "url": "https://facebook.com",
            }
        },
        {
            "case": "recon",
            "kwargs": {
                "url": "https://habr.com",
            }
        },
        {
            "case": "recon",
            "kwargs": {
                "ip": "8.8.8.8"
            }
        },
        {
            "case": "recon",
            "kwargs": {
                "url": "https://habr.com",
            }
        },
        {
            "case": "recon",
            "kwargs": {
                "ip": "13.91.95.74"
            }
        },
    ]

    manager = CaseManager(cases=cases, max_workers=10)
    results = manager.multi_case_runner()
    for result in results:
        pprint(result)

    # fmt: on
