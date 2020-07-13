#!/usr/bin/env python3

"""
Main runner
"""


from pprint import pprint

from src.core.runner.runner import ScriptRunner

if __name__ == "__main__":
    runner = ScriptRunner()
    runner.run_category(
        category="osint",
        username="admin",
        email="johndoe@gmail.com",
        fullname="John Doe",
    )
    results = runner.get_results()

    pprint(results)
