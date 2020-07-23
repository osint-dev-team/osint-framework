#!/usr/bin/env python3

"""
Defines multiprocessing manager
"""

from concurrent.futures import ProcessPoolExecutor
from functools import partial
from src.core.utils.log import Logger

from src.core.case.base import BaseCase
from src.core.case.osint import OsintCase
from src.core.case.recon import ReconCase

logger = Logger.get_logger(name=__name__)


class CaseManager:
    """
    Defines multiprocessing manager for cases
    """

    MAPPING = {
        "recon": ReconCase,
        "osint": OsintCase,
        "base": BaseCase,
        "default": BaseCase,
    }

    def __init__(self, cases: list or None = None, max_workers: int = 3):
        """
        Init manager
        :param cases: cases to run
        :param max_workers: maximum processes
        """
        self.cases = cases
        self.max_workers = max_workers

    def single_case_runner(
        self,
        case_class: str,
        case_name: str or None = None,
        case_description: str or None = None,
        *args,
        **kwargs,
    ):
        """
        Define and smoke run the BaseCase
        :param case_class: original class of the case, name of it
        :param case_name: name of the case, can be any string
        :param case_description: description of the case
        :param args: some args
        :param kwargs: some kwargs
        :return: result of the execution
        """
        logger.info(
            f"start case '{case_name}' processing (class: '{self.MAPPING.get(case_class, 'default').__name__}')"
        )
        case = self.MAPPING.get(case_class, "default")()
        case.process(*args, **kwargs)
        return {
            "case_class": self.MAPPING.get(case_class, "default").__name__,
            "case_name": case_name,
            "case_description": case_description,
            "case_results": case.get_results() or {},
        }

    def multi_case_runner(
        self, cases: list or None = None, max_workers: int or None = None
    ):
        """
        Run multiple case in separated processes
        :param cases: cases to run
        :param max_workers: maximum processes
        :return: results
        """
        futures = []
        with ProcessPoolExecutor(
            max_workers=max_workers or self.max_workers
        ) as executor:
            for case in cases or self.cases:
                futures.append(
                    executor.submit(
                        partial(
                            self.single_case_runner,
                            case_class=case.get("case"),
                            case_name=case.get("name"),
                            case_description=case.get("description"),
                            *case.get("args", []),
                            **case.get("kwargs", {}),
                        )
                    )
                )
        for future in futures:
            yield future.result()
