#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
from json import dump


class DefaultValues:
    RESULTS_DIR = Path(__file__).parents[3].joinpath("results")
    CASES = []


class Saver:
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
        with open(
            file=str(file_path),
            mode="w",
        ) as results_file:
            dump(results, results_file, indent=2, default=str, ensure_ascii=False)
        return file_path
