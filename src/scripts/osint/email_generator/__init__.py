#!/usr/bin/env python3
from json import loads
from random import shuffle, choice
from wordninja import LanguageModel


def factorial(n: int) -> int:
    """
    :param n: positive number
    :return: n! - factorial of positive number
    """
    if n < 0:
        raise ValueError("argument of factorial() must be positive!")
    return 1 if not n else factorial(n - 1) * n


class EmailGenerator:
    def __init__(
        self,
        limit: int or None = None,
        namebase: str or None = None,
        domenbase: str or None = None,
    ):
        """
        :param limit: max size of list of person's emails
        :param namebase: base of names written in translit as gzipped text file
        :param domenbase: base of email domens written in translit as text file
        """
        self.__limit = limit
        with open("settings/settings.json", "r", encoding="utf-8") as jfile:
            data = loads(jfile.read())
            self.__domen_base = (
                domenbase if domenbase is not None else data["domenBase"]
            )
            self.__domen_base_size = data["domenBaseSize"]
            self.__serv_syms = data["serviceSymbols"]
        self.__Divider = LanguageModel(
            namebase if namebase is not None else data["nameBase"]
        )

    def SetLimit(self, limit: int) -> None:
        """
        :param limit: max size of generator
        """
        self.__limit = limit

    def __GetLogin(self, parts: list) -> str:
        """
        :param parts: lexemes of the username
        :return: possible login
        """
        login = parts.copy()
        shuffle(login)
        shuffle(self.__serv_syms)
        while len(login) != 1:
            # int this we join the login with random dividers
            login[0] = choice(self.__serv_syms).join((login[0], login.pop(1)))
        return login.pop()

    def Generate(self, username: str) -> iter:
        """
        :param username: username to generate email
        :return: iterator of person's emails
        """
        parts = self.__Divider.split(username.lower())
        limit = self.__limit
        max_size = (
            factorial(len(parts))
            * len(self.__serv_syms) ** (len(parts) - 1)
            * self.__domen_base_size
        )
        if not limit or max_size < limit:
            limit = max_size
        loginbase = set()
        counter = 0
        while counter <= limit:
            login = self.__GetLogin(parts)
            while login in loginbase:
                login = self.__GetLogin(parts)
            loginbase.add(login)
            with open(self.__domen_base, "r") as domens:
                for domen in domens:
                    counter += 1
                    yield f"{login}@{domen.strip()}"
                    if counter == limit:
                        return
