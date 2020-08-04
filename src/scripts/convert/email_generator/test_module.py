#!/usr/bin/env python3

from .module import Runner
from pathlib import Path
from re import match as re_match
from unittest import TestCase


def syntax_check(email: str) -> bool:
    """
    function brought from verify-email library
    :param email: email for check
    :return: True if email is possible else false
    """
    if re_match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return True
    return False


class TestEmailGenerator(TestCase):
    def setUp(self) -> None:
        """
        Setup Runner before each test function
        :return: None
        """
        self.runner = Runner()
        with open(Path(__file__).parent.joinpath("settings/domain_base.txt"), "r") as f:
            self.len_domain_base = len(f.read().splitlines())

    def test_create_runner(self):
        """
        Test creation of the class instance
        :return: None
        """
        self.assertIsNotNone(self.runner)
        self.assertIsInstance(self.runner, Runner)

    def test_invalid_usernames(self):
        """
        Test failing on invalid usernames
        :return: False
        """
        self.assertEqual(self.runner.run(username="").get("status"), "error")
        self.assertEqual(self.runner.run(username=None).get("status"), "error")

    def test_divided_username(self):
        """
        Test passing on valid username with dividers
        :return: True
        """
        result = self.runner.run(username="john.doe")
        self.assertEqual(result.get("status"), "success")
        self.assertIsNotNone(result.get("result"))
        self.assertEqual(len(result.get("result")), 4 * 2 * self.len_domain_base)
        # 4 - DefaultValues.binders ** (number-of-parts - 1)
        # 2 - because we can divide and reverse login
        self.assertTrue(all(map(syntax_check, result.get("result"))))

    def test_inseparable_username(self):
        """
        Test passing on valid username without dividers
        :return: True
        """
        result = self.runner.run(username="johndoe")
        self.assertEqual(result.get("status"), "success")
        self.assertIsNotNone(result.get("result"))
        self.assertEqual(len(result.get("result")), self.len_domain_base)
        self.assertTrue(all(map(syntax_check, result.get("result"))))
