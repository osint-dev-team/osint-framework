#!/usr/bin/env python3
from .module import Runner
from unittest import TestCase


class TestEmailGenerator(TestCase):
    def setUp(self) -> None:
        """
        Setup Runner before each test function
        :return: None
        """
        self.runner = Runner()

    def test_create_runner(self):
        """
        Test creation of the class instance
        :return: None
        """
        self.assertIsNotNone(self.runner)
        self.assertIsInstance(self.runner, Runner)

    def test_fail_false_argument(self):
        """
        Test failing on false arguments
        :return: False
        """
        result = self.runner.run(username="")
        self.assertEqual(result.get("status"), "error")

    def test_pass_true_argument(self):
        """
        Test passing on true arguments
        :return: True
        """
        result = self.runner.run(username="john.doe")
        self.assertEqual(result.get("status"), "success")
        self.assertIsNotNone(result.get("result"))
