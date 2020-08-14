#!/usr/bin/env python3

"""
This module is used to log information from scripts (and maybe other modules).
NOTE: As for now, this module is NOT used. Maybe in future we will add some additional formatting?
"""

from logging import getLogger, Formatter
from rich.logging import RichHandler


class Logger:
    @staticmethod
    def get_logger(name: str, separate_name: bool = True) -> getLogger:
        """
        Returns logger for the scripts
        :param name: name of the logger
        :param separate_name: take only the last part of the module
        :return: logger
        """
        # Take only the last part of the modules
        if "." in name and separate_name is True:
            name = name.split(".")[-1]

        # Set-up logger, suppress duplicate handlers
        logger = getLogger(name=name)
        logger.propagate = False

        formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        handler = RichHandler()
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger
