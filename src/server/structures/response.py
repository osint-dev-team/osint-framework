#!/usr/bin/env python3


class DefaultValues:
    """
    Define some default values
    """

    EMPTY = ""


class ResponseStatus:
    """
    Define basic structure for the response
    """

    ERROR = "error"
    SUCCESS = "success"


class ServerResponse:
    """
    Define basic status responses from server
    """

    def __init__(self):
        ...

    @staticmethod
    def __basic_response(status: str, msg: str) -> dict:
        """
        Define basic response
        :param status: status message
        :param msg: additional message
        :return: dict with status
        """
        return {"status": str(status), "message": str(msg)}

    def success(self, msg: str = DefaultValues.EMPTY) -> dict:
        """
        Define success message
        :param msg: additional message
        :return: dict with status
        """
        return self.__basic_response(status=ResponseStatus.SUCCESS, msg=msg)

    def error(self, msg: str = DefaultValues.EMPTY) -> dict:
        """
        Define error message
        :param msg: additional message
        :return: dict with status
        """
        return self.__basic_response(status=ResponseStatus.ERROR, msg=msg)
