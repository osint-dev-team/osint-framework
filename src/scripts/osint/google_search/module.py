#!/usr/bin/env python3

from requests import get
from bs4 import BeautifulSoup

from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Defaults:
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"


class Runner(OsintRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        Make a Google search and return top results.
        :param args: user args
        :param kwargs: user kwargs
        :return: ScriptResponse message
        """

        query = kwargs.get("email", "")
        if query is not str:
            return ScriptResponse.success(
                result=None,
                message=f"Can't make query. Incorrect input type (got {type(query)}, need {type('')}).",
            )

        query = query.replace(" ", "+")
        url = f'https://www.google.com/search?q="{query}"'

        headers = {"User-Agent": Defaults.USER_AGENT}
        resp = get(url, headers=headers)
        results = []

        if resp.status_code == 413:
            return ScriptResponse.success(
                result=None,
                message=f"Can't make query. Request is too long. Server response: {resp.status_code}.",
            )
        elif resp.status_code != 200:
            return ScriptResponse.success(
                result=None,
                message=f"Can't make query. Server response: {resp.status_code}.",
            )

        soup = BeautifulSoup(resp.content, "html.parser")
        for g in soup.find_all("div", class_="r"):
            anchors = g.find_all("a")
            if not anchors:
                continue

            link = anchors[0]["href"]
            title = g.find("h3").text
            item = {"title": title, "link": link}
            results.append(item)

        return ScriptResponse.success(
            result=results, message="Search finished successfully."
        )
