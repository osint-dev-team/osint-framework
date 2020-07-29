#!/usr/bin/env python3

from verify_email import verify_email

from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Runner(OsintRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @staticmethod
    def email_verifier(email: str = "Unknown") -> bool or None:
        if email is None:
            return False
        return verify_email(email)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        email = kwargs.get("email")
        result = self.email_verifier(email)
        if not result:
            return ScriptResponse.success(
                result=result, message=f"Sorry, email {email} does not exist"
            )
        return ScriptResponse.success(result=result, message=f"Email {email} exists")
