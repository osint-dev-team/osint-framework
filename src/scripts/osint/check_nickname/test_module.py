#!/usr/bin/env python3

from unittest import TestCase
from .module import Runner
from random import choice
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

    def test_special_nicknames(self) -> None:
        """
        Test values from the remote server
        :return: None
        """
        response = self.runner.run(username=None)
        self.assertEqual(response.get("status"), "error")
        response = self.runner.run(username="")
        self.assertEqual(response.get("status"), "success")
        for i in range(3, 10):
            for j in range(5):
                s = ''.join(choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(i))
                response = self.runner.run(username=s)
                self.assertEqual(response.get("status"), "success")
