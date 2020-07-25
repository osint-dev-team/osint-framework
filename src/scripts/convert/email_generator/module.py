#!/usr/bin/env python3
from time import time
from pathlib import Path

from src.core.base.base import BaseRunner
from src.core.utils.response import ScriptResponse


class DefaultValues:
    dividers = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    binders = ("-", "_", ".", "")


class EmailGenerator:
    def __init__(self, domain_base: str = "settings/domain_base.txt"):
        """
        :param domain_base: base of email domains written in translit as text file
        """
        with open(Path(__file__).parent.joinpath(domain_base), "r") as domains:
            self.__domains = domains.read().splitlines()

    @staticmethod
    def divide(username: str) -> list:
        """
        :param username: username to generate email
        :return: login's lexemes
        """
        for sym in DefaultValues.dividers:
            username = username.replace(sym, " ")
        return username.split()

    def generate(self, username: str) -> iter:
        """
        :param username: username to generate email
        :return: iterator of person's emails
        """
        parts = self.divide(username.lower())
        logins = []
        for i in range(2):
            logins.extend([sym.join(parts) for sym in DefaultValues.binders])
            parts.reverse()
        for login in logins:
            for domain in self.__domains:
                yield f"{login}@{domain}"


class Runner(BaseRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        Main runner function for the script
        :param args: args from core runner
        :param kwargs: kwargs from core runner
        :return: ScriptResponse message
        """
        try:
            tm = time()
            email_gen = EmailGenerator()
            username = kwargs.get("username")
            if username is None:
                raise KeyError("EmailGenerator can't work without username!")
            result = list(email_gen.generate(username))
        except Exception as err:
            return ScriptResponse.error(message=str(err))
        else:
            return ScriptResponse.success(
                result=result,
                message=f"Successfully finished! Got {len(result)} logins, script lasted {(time() - tm):.2f} seconds",
            )
