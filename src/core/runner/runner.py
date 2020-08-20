#!/usr/bin/env python3

"""
Defines basic scripts runner
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from importlib.machinery import SourceFileLoader
from pathlib import Path
from time import sleep
from types import ModuleType

import urllib3

from src.core.utils.log import Logger
from src.core.utils.response import ScriptResponse
from src.core.values.defaults import CoreDefaults

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = Logger.get_logger(name=__name__)


class Defaults:
    SCRIPTS_BASE = Path("src/scripts/")


class ScriptRunnerPaths:
    OSINT = Defaults.SCRIPTS_BASE.joinpath("osint")
    RECON = Defaults.SCRIPTS_BASE.joinpath("recon")
    CONVERT = Defaults.SCRIPTS_BASE.joinpath("convert")
    OTHER = Defaults.SCRIPTS_BASE.joinpath("other")


class ScriptRunner:
    def __init__(self):
        self.scripts = {}
        self.results = {}

    @staticmethod
    def exec_script(
        path: str or Path,
        script_class: str = "Runner",
        function: str = "run",
        args: list or None = None,
        kwargs: dict or None = None,
    ) -> ScriptResponse or dict:
        """
        Load and exec python script
        :param path: name of the script to load
        :param script_class: class to initialize when script is started
        :param function: name of the function to run from script
        :param args: args to pass into the module
        :param kwargs: kwargs to pass into the module
        :return: result of the function
        """
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        loader = SourceFileLoader(fullname=script_class, path=str(path))
        module = ModuleType(name=loader.name)
        result = {"script": Path(path).parent.stem}

        # Check if don't forget to install all the dependencies, and that module can
        # be successfully loaded.

        # fmt: off
        try:
            loader.exec_module(module)
        except Exception as unexp_err:
            message = f"Unexpected module error: {str(unexp_err)}"
            logger.warning(message)
            result.update(ScriptResponse.error(message=message))
            return result
        # fmt: on

        # Module successfully loaded. We can set some module-scope variables that
        # we missed.
        module.__file__ = path

        # Execute the runner and check if something goes wrong.

        # fmt: off
        try:
            module_class = getattr(module, script_class)
            applicable = set(module_class.required).intersection(kwargs.keys())
            # If the current script is not applicable for the current set of arguments - skip it
            if not applicable:
                return
            class_instance = module_class(logger=path.parent.stem)
            result.update(getattr(class_instance, function)(*args, **kwargs))
        except Exception as unexp_err:
            result.update(ScriptResponse.error(message=f"Unexpected execution error: {str(unexp_err)}"))
        # fmt: on

        # In any possible case, return result from the module or ScriptResponse.error + script name
        return result

    def get_scripts(self) -> dict:
        """
        Load the dictionary with all of the scripts
        :return: dict {'dir':['script1', 'script2', ...]}
        """
        for directory in [
            ScriptRunnerPaths.OSINT,
            ScriptRunnerPaths.RECON,
            ScriptRunnerPaths.OTHER,
            ScriptRunnerPaths.CONVERT,
        ]:
            self.scripts.update({directory.stem: list()})
            for file in directory.glob("*/module.py"):
                self.scripts[directory.stem].append(file)
        return self.scripts

    def run_category(
        self,
        category: str,
        max_workers: int = CoreDefaults.MAX_THREADS,
        timeout: int = CoreDefaults.CASE_TIMEOUT,
        *args,
        **kwargs,
    ) -> None:
        """
        Run a category with scripts
        :param category: category to run
        :param max_workers: max quantity of workers
        :param timeout: timeout to wait in seconds
        :return: nothing
        """
        if not self.scripts:
            self.get_scripts()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    self.exec_script, path=script, args=args, kwargs=kwargs
                ): sleep(0.1)
                for script in self.scripts.get(category, [])
            }
        try:
            for future in as_completed(futures, timeout=timeout):
                result = future.result()
                if not result:
                    continue
                self.results.update({result.get("script"): result})
        except TimeoutError:
            # Tasks took too much time - kill the execution process and return empty results
            self.results = {}

    def get_results(self) -> dict:
        """
        Return retrieved results
        :return:
        """
        return self.results
