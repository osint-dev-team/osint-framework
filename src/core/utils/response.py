#!/usr/bin/env python3

from typing import Any

"""
This module defines basic answers from the scripts
"""


class ScriptStatus:
    SUCCESS = "success"
    ERROR = "error"
    UNKNOWN = "unknown"


class ScriptResponse:
    @staticmethod
    def response(
        result: Any = None, message: str or None = None, status: str or None = None
    ) -> dict:
        """
        Defines response message
        :param result: result of the script
        :param message: message (additional)
        :param status: status from 'ScriptStatus'
        :return: dictionary with full response
        """
        if status not in [ScriptStatus.SUCCESS, ScriptStatus.ERROR]:
            status = ScriptStatus.UNKNOWN
        return {"result": result, "message": message, "status": status}

    @staticmethod
    def success(result: Any = None, message: str or None = None) -> dict:
        """
        Defines success message
        :param result: result of the script
        :param message: message (additional)
        :return: dictionary with full response
        """
        return ScriptResponse.response(
            result=result, message=message, status=ScriptStatus.SUCCESS
        )

    @staticmethod
    def error(result: Any = None, message: str or None = None) -> dict:
        """
        Defines error message
        :param result: result of the script
        :param message: message (additional)
        :return: dictionary with full response
        """
        return ScriptResponse.response(
            result=result, message=message, status=ScriptStatus.ERROR
        )
