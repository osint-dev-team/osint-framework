#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
from json import dump, load
from yaml import safe_load

from src.core.utils.log import Logger


logger = Logger.get_logger(name="osint-framework")


class DefaultValues:
    RESULTS_DIR = Path(__file__).parents[3].joinpath("results")
    CASES = []


class FileManager:
    @staticmethod
    def save_results(results: dict or list, name: str or None = "scenario") -> Path:
        """
        Save scenario results
        :param results: results to save
        :param name: name to overwrite (if required)
        :return: path to file
        """
        DefaultValues.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        file_path = DefaultValues.RESULTS_DIR.joinpath(f"{name}_{current_time}.json")
        with open(file=str(file_path), mode="w",) as results_file:
            dump(results, results_file, indent=2, default=str, ensure_ascii=False)
        return file_path

    @staticmethod
    def load_scenario(scenario: str or None, method: callable) -> list:
        """
        Load scenario to run
        :param scenario: scenario file
        :param method: function to use, JSON or YAML load
        :return: list with data
        """
        if not scenario:
            return DefaultValues.CASES
        try:
            with open(scenario, mode="r") as scenario_file:
                return method(scenario_file)
        except:
            logger.error(msg=f"Scenario file is not available or can not be opened")

    @staticmethod
    def load_yaml_scenario(scenario: str or None = None) -> list:
        """
        Load yaml scenario to run
        :param scenario: scenario .yaml filename
        :return: list with data
        """
        return FileManager.load_scenario(scenario, method=safe_load)

    @staticmethod
    def load_json_scenario(scenario: str or None = None) -> list:
        """
        Load json scenario to run
        :param scenario: scenario .json filename
        :return: list with data
        """
        return FileManager.load_scenario(scenario, method=load)
