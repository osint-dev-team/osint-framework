#!/usr/bin/env python3

"""
Main runner.
"""

from logging import basicConfig, INFO

from src.cli.handlers.files import FileManager
from src.cli.interface.arguments import parse_args
from src.cli.interface.validators import check_arg_length, check_py_version
from src.cli.interface.opener import show_opener
from src.core.runner.manager import CaseManager
from pathlib import Path


basicConfig(level=INFO)


if __name__ == "__main__":
    # fmt: off

    show_opener()
    check_py_version()
    check_arg_length()
    scenario = str(parse_args().scenario)

    if scenario.endswith("json"):
        cases = FileManager.load_json_scenario(scenario)
    else:
        cases = FileManager.load_yaml_scenario(scenario)

    manager = CaseManager(cases)
    results = list(manager.multi_case_runner())

    FileManager.save_results(results, name=Path(scenario).stem)

    # fmt: on
