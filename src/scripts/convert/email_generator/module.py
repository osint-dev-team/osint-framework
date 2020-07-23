#!/usr/bin/env python3
from json import loads
from time import time

from src.core.base.base import BaseRunner
from src.core.utils.response import ScriptResponse


class EmailGenerator:
    def __init__(self, domen_base: str or None = None, serv_syms: list or None = None):
        """
        :param domen_base: base of email domens written in translit as text file
        """
        with open("settings/settings.json", "r", encoding="utf-8") as jfile:
            data = loads(jfile.read())
            self.__domen_base = domen_base if domen_base is not None else data["domenBase"]
            self.__serv_syms = serv_syms if serv_syms is not None else data["serviceSymbols"]

    def divide(self, username: str) -> list:
        """
        :param username: username to generate email
        :return: login's lexemes
        """
        for sym in self.__serv_syms:
            if sym != '' and username.find(sym) != -1:
                username = username.replace(sym, '_')
        return username.split('_')

    def generate(self, username: str) -> iter:
        """
        :param username: username to generate email
        :return: iterator of person's emails
        """
        parts = self.divide(username.lower())
        login_base = []
        for i in range(2):
            login_base.extend([sym.join(parts) for sym in self.__serv_syms])
            parts.reverse()
        for login in login_base:
            with open(self.__domen_base, "r") as domens:
                for domen in domens:
                    yield f"{login}@{domen.strip()}"


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
                message=f"Successfully finished! Got {len(result)} logins, script lasted {(time() - tm):.2f} seconds"
            )
