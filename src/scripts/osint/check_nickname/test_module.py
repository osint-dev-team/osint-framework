#!/usr/bin/env python3

from unittest import TestCase
from .module import Runner
from random import choice, randrange
import string
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread


class NicknameCheckTest(TestCase):
    def setUp(self):
        """
        Setup something before each test function
        :return: None
        """
        self.runner = Runner()

    def test_create_runner(self) -> None:
        """
        Test creation of the class instance
        :return: None
        """
        self.assertIsNotNone(self.runner)
        self.assertIsInstance(self.runner, Runner)

    def test_nicknames(self) -> None:
        """
        Tests  different usernames with random acceptable
         characters
        :return: None
        """
        response = self.runner.run(username="")
        self.assertEqual(response.get("status"), "success")
        for _ in range(5):
            nickname = "".join(choice(string.ascii_letters) for _ in range(randrange(5, 10)))
            response = self.runner.run(username=nickname)
            self.assertEqual(response.get("status"), "success")

    def test_special_nicknames(self) -> None:
        """
        Tests  not acceptable characters in username
         and not acceptable formats of the stdin
        :return:
        """
        response = self.runner.run(username=None)
        self.assertEqual(response.get("status"), "error")
        for _ in range(5):
            nickname = ''.join(choice(string.punctuation) for _ in range(randrange(3,5)))
            response = self.runner.run(username=nickname)
            self.assertEqual(response.get("status"), "error")
