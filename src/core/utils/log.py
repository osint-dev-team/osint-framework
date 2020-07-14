#!/usr/bin/env python3

"""
This module is used to log information from scripts (and maybe other modules)
"""

from logging import getLogger


class Logger:
    @staticmethod
    def get_logger(name: str) -> getLogger:
        """
        Returns logger for the scripts
        :param name: name of the logger
        :return: logger
        """
        return getLogger(name=name)
