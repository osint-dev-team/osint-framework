#!/usr/bin/env python3

"""
Main runner.
"""

from pprint import pprint

from src.core.runner.manager import CaseManager


class DefaultValues:
    CASES = [
        {
            "case": "base",
            "name": "testname-profile",
            "description": "Base example for 'testname' user profile",
            "kwargs": {
                "username": "testname",
                "email": "testmail@gmail.com",
                "fullname": "Test Name"
            }
        },
        {
            "case": "osint",
            "name": "johndoe-profile",
            "description": "Osint example for 'johndoe' user profile",
            "kwargs": {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "fullname": "John Doe"
            }
        },
        {
            "case": "recon",
            "name": "facebook-website",
            "description": "Recon example for 'facebook.com' website",
            "kwargs": {
                "url": "https://facebook.com",
            }
        },
        {
            "case": "recon",
            "name": "habr-website",
            "description": "Recon example for 'habr.com' website",
            "kwargs": {
                "url": "https://habr.com",
            }
        },
        {
            "case": "recon",
            "name": "8-8-8-8-host",
            "description": "Recon example for '8.8.8.8' host",
            "kwargs": {
                "ip": "8.8.8.8"
            }
        },
        {
            "case": "recon",
            "name": "13-91-95-74-host",
            "description": "Recon example for '13.91.95.74' host",
            "kwargs": {
                "ip": "13.91.95.74"
            }
        },
    ]


if __name__ == "__main__":
    # fmt: off

    # Define CaseManager class
    manager = CaseManager(cases=DefaultValues.CASES, max_workers=10)

    # Run all the cases in parallel way
    multiple_results = manager.multi_case_runner()
    for single_result in multiple_results:
        pprint(single_result)

    # Run single case
    single_results = manager.single_case_runner(
        case_class="recon",
        case_name="test single runner",
        case_description="Nothing special",
        url="https://habr.com/"
    )

    # Show results
    pprint(single_results)
    # fmt: on
