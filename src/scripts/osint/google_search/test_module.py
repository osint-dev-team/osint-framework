#!/usr/bin/env python3

from unittest import TestCase
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


class GoogleSearchTest(TestCase):
    """
    Defines basic tests for the Google search script.
    """

    def setUp(self):
        """
        Setup something before each test function
        :return: None
        """
        self.runner = Runner()

    def test_request(self) -> None:
        """
        Test Google search on typical request.
        :return: None
        """
        response = self.runner.run(email="@gmail.com")
        self.assertIn("successfully", response.get("message"))
        self.assertGreaterEqual(len(response.get("result")), 3)

    def test_empty_request(self) -> None:
        """
        Test Google search on empty request.
        :return: None
        """
        response = self.runner.run(email="")
        self.assertIn("successfully", response.get("message"))
        self.assertEqual(len(response.get("result")), 0)

    def test_random_string(self) -> None:
        """
        Test Google search on random string request.
        """
        request = get_random_string(30)
        response = self.runner.run(email=request)
        self.assertIn("successfully", response.get("message"))

    def test_multiple_requests(self) -> None:
        """
        Test Google search on multiple consequent requests
        """
        for _ in range(20):
            response = self.runner.run(email="@gmail.com")
            self.assertIn("successfully", response.get("message"))
            self.assertGreaterEqual(len(response.get("result")), 3)
