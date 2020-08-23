#!/usr/bin/env python3

from unittest import TestCase, SkipTest
from random import seed, choice
from string import ascii_uppercase

from .module import Runner


def get_random_string(length: int) -> str:
    """
    Generates random string.
    """
    seed()
    letters = ascii_uppercase
    string = "".join(choice(letters) for i in range(length))
    return string


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
        if "429" in response.get("message", ""):
            raise SkipTest("Server respond with 429 (Too many requests)")

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
        request = get_random_string(30)
        response = self.runner.run(email=request)
        if "429" in response.get("message", ""):
            raise SkipTest("Server respond with 429 (Too many requests)")
        self.assertIn("found in", response.get("message"))

    def test_unexpected_input(self) -> None:
        """
        Test email breach on unexpected input type
        """
        response = self.runner.run(email=None)
        if "429" in response.get("message", ""):
            raise SkipTest("Server respond with 429 (Too many requests)")
        self.assertIn("Can't make query", response.get("message"))
