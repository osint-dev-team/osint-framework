#!/usr/bin/env python3
from hashlib import sha1
from re import findall

from bs4 import BeautifulSoup
from requests import Session

from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Defaults:
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                             " Chrome/84.0.4147.105 Safari/537.36"}


class Runner(OsintRunner):
    """
    Check email in public breaches.
    """
    required = ["email"]

    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        Take email and look it up in breaches.
        Breaches info is provided by monitor.firefox.com (haveibeenpwned.com)
        """
        email = kwargs.get("email")
        email_hash = sha1(email.encode()).hexdigest()

        session = Session()
        session.headers.update(Defaults.headers)

        resp = session.get(r"https://monitor.firefox.com")
        if resp.status_code != 200:
            return ScriptResponse.success(
                result=None,
                message=f"Can't look up email in breaches. Server response: {resp.status_code}.",
            )

        csrf_re = findall(r'(?<="_csrf" value=").*(?=">)', resp.text)
        if len(csrf_re) == 0:
            return ScriptResponse.error(
                result=None,
                message=f"Can't find csrf token."
            )
        csrf = csrf_re[0]

        data = {"_csrf": csrf, 'emailHash': email_hash}
        resp = session.post(r"https://monitor.firefox.com/scan", data=data)
        if resp.status_code != 200:
            return ScriptResponse.success(
                result=None,
                message=f"Can't look up email in breaches. Server response: {resp.status_code}.",
            )

        session.close()

        breaches = []
        soup = BeautifulSoup(resp.text, 'lxml')
        for breach in soup.find_all("a", class_="breach-card"):
            title = breach.find("span", class_="breach-title").text
            breaches.append({'title': title})

        return ScriptResponse.success(
            result=breaches,
            message=f"Email is found in {len(breaches)} breaches.",
        )
