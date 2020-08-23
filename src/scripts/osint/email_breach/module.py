#!/usr/bin/env python3

from hashlib import sha1
from re import findall

from bs4 import BeautifulSoup
from requests import Session

from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Defaults:
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/84.0.4147.105 Safari/537.36",
    }


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
        if not isinstance(email, str):
            return ScriptResponse.error(
                result=None,
                message=f"Can't make query. Incorrect input type (got {type(email)}, need {type('')}).",
            )
        email_hash = sha1(email.encode()).hexdigest()

        with Session() as session:
            session.headers.update(Defaults.headers)

            resp = session.get(r"https://monitor.firefox.com")
            if resp.status_code != 200:
                return ScriptResponse.success(
                    result=None,
                    message=f"Can't look up email in breaches. Server response: {resp.status_code}.",
                )

            csrf_re = findall(r'(?<="_csrf" value=").*(?=">)', resp.text)
            if not csrf_re:
                return ScriptResponse.error(
                    result=None, message=f"Can't find csrf token."
                )

            csrf = csrf_re[0]
            resp = session.post(
                r"https://monitor.firefox.com/scan",
                data={"_csrf": csrf, "emailHash": email_hash},
            )
            if resp.status_code != 200:
                return ScriptResponse.success(
                    result=None,
                    message=f"Can't look up email in breaches. Server response: {resp.status_code}.",
                )

        breaches = []
        soup = BeautifulSoup(resp.text, "html.parser")
        for breach in soup.find_all("a", class_="breach-card"):
            title = breach.find("span", class_="breach-title").text
            info = breach.find_all("span", class_="breach-value")
            if len(info) < 2:
                continue
            breaches.append(
                {"title": title, "date": info[0].text, "compromised": info[1].text}
            )

        return ScriptResponse.success(
            result=breaches,
            message=f"Email {email} is found in {len(breaches)} breaches.",
        )
