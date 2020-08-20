#!/usr/bin/env python3

from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs
from requests import get
from re import findall


class Runner(OsintRunner):
    """
    Class that performs Russian Extremists list check
    """
    required = ["fullname"]

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
                message="Extremists name base is not available",
            )
        occurences = findall(rf"<li>\d+\. ({fullname.upper()}.*);</li>", response.text)
        return ScriptResponse.success(
            result={"found": bool(occurences), "occurrences": occurences},
            message="Person found on the Russian extremists list"
            if bool(occurences)
            else "Person not found on the Russian extremists list",
        )
