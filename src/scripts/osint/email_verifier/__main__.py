#!/usr/bin/env python3

from src.core.base.osint import OsintRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs
from verify_email import verify_email


class Runner(OsintRunner):
    def __init__(self, logger: str = __name__):
        super(Runner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        kwargs = {"email": "johndoe@gmail.com"}
        email = kwargs.get("email")
        result = verify_email(email)
        if not result:
            return ScriptResponse.success(
                result=result, message=f"Sorry, email {email} does not exist :-( "
            )
        return ScriptResponse.success(result=result, message=f"Email {email} exist!")
