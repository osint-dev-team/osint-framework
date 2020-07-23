#!/usr/bin/env python3

from unittest import TestCase
from .module import Runner
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

    def test_remote_server(self) -> None:
        """
        Test values from the remote server
        :return: None
        """
        response = self.runner.run(username=None)
        self.assertEqual(response.get("status"), "success")
        response = self.runner.run(username="")
        self.assertEqual(response.get("status"), "success")
