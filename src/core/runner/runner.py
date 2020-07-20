#!/usr/bin/env python3

"""
Defines basic scripts runner
"""

from concurrent.futures import ThreadPoolExecutor
from functools import partial
from importlib.machinery import SourceFileLoader
from logging import basicConfig, INFO
from pathlib import Path
from types import ModuleType

from src.core.utils.response import ScriptResponse

basicConfig(level=INFO)


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
            result.update(ScriptResponse.error(message=f"Unexpected module error: {str(unexp_err)}"))
            return result
        # fmt: on

        # Module successfully loaded. We can set some module-scope variables that
        # we missed.
        module.__file__ = path

        # Execute the runner and check if something goes wrong.

        # fmt: off
        try:
            class_instance = getattr(module, script_class)(logger=path.parent.stem)
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

    def run_category(self, category: str, *args, **kwargs) -> None:
        """
        Run a category with scripts
        :return: nothing
        """
        if not self.scripts:
            self.get_scripts()
        futures = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for script in self.scripts.get(category, []):
                futures.append(
                    executor.submit(
                        fn=partial(
                            self.exec_script, path=script, args=args, kwargs=kwargs
                        )
                    )
                )
        for future in futures:
            result = future.result()
            self.results.update({result.get("script"): result})

    def get_results(self) -> dict:
        """
        Return retrieved results
        :return:
        """
        return self.results
