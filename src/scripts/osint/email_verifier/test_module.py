#!/usr/bin/env python3

from unittest import TestCase
from .module import Runner


class email_verifier_test(TestCase):
    def setUp(self):
        """
        Setup something before each test function
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

    def test_pass_argument(self):
        """
        Test passing an arguments
        :return: None
        """
        result = self.runner.run(email="john@gmail.com")
        self.assertEqual(result.get("result"), False)
        self.assertEqual(result.get("status"), "success")

    def test_no_arguments(self):
        """
        Test passing no arguments
        :return: None
        """
        result = self.runner.run()
        self.assertEqual(result.get("result"), False)
        self.assertEqual(result.get("status"), "success")

    def test_wrong_argument(self):
        """
        Test case when we can't pass the validator (exception)
        :return: None
        """

        def exception_func():
            self.runner.run(wrong_argument="john@gmail.com")

        self.assertRaises(KeyError, exception_func)
