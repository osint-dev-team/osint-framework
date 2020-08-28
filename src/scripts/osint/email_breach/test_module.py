#!/usr/bin/env python3

from unittest import TestCase, SkipTest
from random import choices
from string import ascii_uppercase

from .module import Runner


def get_random_string(length: int = 30) -> str:
    """
    Generates random string.
    :param length: string length
    :return: random string
    """
    return "".join(choices(ascii_uppercase, k=length))


def check_response_msg(message: str = "") -> None:
    """
    Check that response message is valid and applicable
    :param message: message of the response
    :return: None
    """
    if "429" in message:
        raise SkipTest("Server respond with 429 (Too many requests)")


class EmailBreachTest(TestCase):
    """
    Defines basic tests for the email breach script.
    """

    def setUp(self):
        """
        Setup something before each test function
        :return: None
        """
        self.runner = Runner()

    def test_request(self) -> None:
        """
        Test email breach on johndoe@gmail.com.
        :return: None
        """
        response = self.runner.run(email="johndoe@gmail.com")
        check_response_msg(response.get("message", ""))

        self.assertIn("found in", response.get("message"))
        self.assertGreaterEqual(len(response.get("result")), 10)
        self.assertIn(
            {
                "compromised": "Passwords, Email addresses",
                "date": "December 4, 2013",
                "title": "Adobe",
            },
            response.get("result"),
        )

    def test_random_string(self) -> None:
        """
        Test email breach on random string request.
        """
        response = self.runner.run(email=get_random_string())
        check_response_msg(response.get("message", ""))
        self.assertIn("found in", response.get("message"))

    def test_unexpected_input(self) -> None:
        """
        Test email breach on unexpected input type
        """
        response = self.runner.run(email=None)
        check_response_msg(response.get("message", ""))
        self.assertIn("Can't make query", response.get("message"))
