#!/usr/bin/env python3

from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs
from requests import get
from bs4 import BeautifulSoup
from re import search


class Runner(OsintRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        fullname = kwargs.get("fullname")
        if not fullname:
            return ScriptResponse.error(
                result="Couldn't run the script", message="No name was provided"
            )
        response = get("http://www.fedsfm.ru/documents/terrorists-catalog-portal-act")
        if response.status_code != 200:
            return ScriptResponse.error(
                result="Couldn't run the script",
                message="Extremists name base was not available",
            )
        soup = BeautifulSoup(response.text, "html.parser")
        russians = soup.find_all(name="ol", attrs={"class": "terrorist-list"})[
            3
        ].find_all(name="li")
        foreigners = soup.find_all(name="ol", attrs={"class": "terrorist-list"})[
            1
        ].find_all(name="li")
        persons = russians + foreigners
        totalOccurrences = list(
            map(
                lambda tag: tag.string,
                filter(
                    lambda person: search(
                        r"[0-9]+\. " + fullname.upper(), person.string
                    ),
                    persons,
                ),
            )
        )
        return ScriptResponse.success(
            result={"found": bool(totalOccurrences), "occurrences": totalOccurrences},
            message="Person was found on the Russian extremist list"
            if bool(totalOccurrences)
            else "Person was not found on the Russian extremist list",
        )
