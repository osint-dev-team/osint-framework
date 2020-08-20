#!/usr/bin/env python3
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep
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
        Test Google search on multiple parallel requests
        """
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(self.runner.run, email="@gmail.com") for _ in range(10)
            }
        for future in as_completed(futures):
            print(future.result().get("message"))
            self.assertIn("successfully", future.result().get("message"))
            self.assertGreaterEqual(len(future.result().get("result")), 3)

    def test_unexpected_input(self) -> None:
        """
        Test Google search on unexpected input type
        """
        response = self.runner.run(email=None)
        self.assertIn("Can't make query", response.get("message"))
