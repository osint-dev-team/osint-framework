#!/usr/bin/env python3

from unittest import TestCase

from .module import Runner


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
