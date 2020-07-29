#!/usr/bin/env python3

"""
Main runner.
"""

from logging import basicConfig, INFO
from pprint import pprint
from yaml import safe_load
from sys import argv

from src.core.runner.manager import CaseManager
from src.core.utils.log import Logger

basicConfig(level=INFO)
logger = Logger.get_logger(name="osint-framework")


class DefaultValues:
    CASES = []


def run_single_case(manager: CaseManager) -> dict or list:
    """
    Run single case
    :param manager: manager to use
    :return: data
    """
    return manager.single_case_runner(
        case_class="recon",
        case_name="test single runner",
        case_description="Nothing special",
        url="https://habr.com/"
    )


def load_scenario(scenario: str or None = None) -> list:
    """
    Load scenario to run
    :param scenario: scenario .yaml filename
    :return: list with data
    """
    if not scenario:
        return DefaultValues.CASES
    try:
        with open(scenario, mode="r") as scenario_file:
            return safe_load(scenario_file)
    except:
        logger.error(msg=f"Scenario file is not available or can not be opened")


if __name__ == "__main__":
    # fmt: off

    # Load scenario file
    scenario_cases = load_scenario(scenario=argv[1] if len(argv) >= 2 else None)
    if not scenario_cases:
        logger.error(msg=f"Scenario file is empty. Cases is not defined")
        exit(1)

    # Start processing
    logger.info(f"Start framework for {len(scenario_cases)} cases")

    # Define CaseManager class
    manager = CaseManager(cases=scenario_cases, max_workers=5)

    # Run all the cases in parallel way
    multiple_results = manager.multi_case_runner()
    for single_result in multiple_results:
        pprint(single_result)

    # fmt: on
