#!/usr/bin/env python3

from src.core.runner.runner import ScriptRunner


class BaseCase:
    """
    Defines base search case
    """

    def __init__(self, category: str = "other", *args, **kwargs):
        """
        Init base
        :param category: default category to search
        :param args: some args
        :param kwargs: some kwargs
        """
        self.runner = ScriptRunner()
        self.args = args
        self.kwargs = kwargs
        self.category = category

    def process(self, *args, **kwargs) -> dict:
        """
        Process results
        :param args: some args
        :param kwargs: some kwargs
        :return: results
        """
        _args = args or self.args
        _kwargs = kwargs or self.kwargs
        self.runner.run_category(category=self.category, *_args, **_kwargs)
        return self.runner.get_results()

    def get_results(self) -> dict:
        """
        Return results
        :return: dict with results
        """
        return self.runner.get_results()
