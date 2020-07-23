#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from unittest import TestCase

from .module import Runner
from src.core.values.defaults import TestDefaults


DefaultValues = TestDefaults()


class TestClassHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Defines mocking server class
    """

    def do_GET(self) -> None:
        """
        Defines basic handlers
        :return: None
        """
        if self.path == "/":
            self.mock_endpoint()

    def mock_endpoint(self) -> None:
        """
        Mock '/' endpoint. Return HTML with custom headers.
        :return: None
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<html><body><i>Mock page from Mocking Class</i></body></html>"
        )


class NetworkUsageTest(TestCase):
    """
    Defines basic tests for the network usage
    """

    server: Thread or None = None

    def setUp(self):
        """
        Setup something before each test function
        :return: None
        """
        self.runner = Runner()

    @classmethod
    def setUpClass(cls) -> None:
        """
        Start up server on class initialization in daemon thread
        :return: None
        """
        super(NetworkUsageTest, cls).setUpClass()
        cls.server = HTTPServer(
            server_address=(DefaultValues.HOST, DefaultValues.PORT),
            RequestHandlerClass=TestClassHTTPRequestHandler,
        )
        server_daemon = Thread(target=cls.server.serve_forever, daemon=True)
        server_daemon.start()

    @classmethod
    def tearDownClass(cls) -> None:
        super(NetworkUsageTest, cls).tearDownClass()
        cls.server.shutdown()

    def test_create_runner(self) -> None:
        """
        Test creation of the class instance
        :return: None
        """
        self.assertIsNotNone(self.runner)
        self.assertIsInstance(self.runner, Runner)

    def test_local_server(self) -> None:
        """
        Test values from the local server
        :return: None
        """
        response = self.runner.run(
            hostname=f"http://{DefaultValues.HOST}:{DefaultValues.PORT}"
        )
        self.assertEqual(response.get("message"), "Success")
        self.assertEqual(response.get("status"), "success")
        result = response.get("result")
        self.assertIn("BaseHTTP", result.get("Server"))
        self.assertIn("Python", result.get("Server"))
        self.assertEqual(result.get("Content-type"), "text/html; charset=utf-8")

    def test_remote_server(self) -> None:
        """
        Test values from the remote server
        :return: None
        """
        response = self.runner.run(hostname=f"http://www.example.com/")
        self.assertEqual(response.get("message"), "Success")
        self.assertEqual(response.get("status"), "success")
        result = response.get("result")
        self.assertIn("ECS", result.get("Server"))
        self.assertEqual(result.get("Content-type"), "text/html; charset=UTF-8")
