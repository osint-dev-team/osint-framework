#!/usr/bin/env python3

from unittest import TestCase
from .module import Runner


class UserGreetingTest(TestCase):
    def setUp(self):
        self.runner = Runner()

    def test_create_runner(self):
        self.assertIsNotNone(self.runner)
        self.assertIsInstance(self.runner, Runner)

    def test_pass_argument(self):
        result = self.runner.run(username="john")
        self.assertEqual(result.get("result"), "Hello, john!")
        self.assertEqual(result.get("status"), "success")
