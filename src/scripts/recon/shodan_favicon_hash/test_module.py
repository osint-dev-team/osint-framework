#!/usr/bin/env python3

from unittest import TestCase
from .module import Runner
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

from pathlib import Path


class DefaultValues:
    """
    Set default localhost values
    """

    HOST = "127.0.0.1"
    PORT = 1337


class TestClassHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Defines mocking server class
    """

    def do_GET(self) -> None:
        """
        Defines GET http method. Responses only to /favicon.ico
        :return: None
        """

        if self.path == "/favicon.ico":
            self.mock_endpoint()

    def mock_endpoint(self) -> None:
        """
        Mock '/favicon.ico' endpoint.
        :return: None
        """
        self.send_response(200)
        self.send_header("Content-type", "image/x-icon")
        self.end_headers()
        with open(Path(__file__).parent.joinpath("data/favicon.ico"), "rb") as favicon:
            self.wfile.write(favicon.read())


class FaviconHashTest(TestCase):
    """
    Defines basic tests for the Shodan favicon hash script.
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
        super(FaviconHashTest, cls).setUpClass()
        cls.server = HTTPServer(
            server_address=(DefaultValues.HOST, DefaultValues.PORT),
            RequestHandlerClass=TestClassHTTPRequestHandler,
        )
        server_daemon = Thread(target=cls.server.serve_forever, daemon=True)
        server_daemon.start()

    @classmethod
    def tearDownClass(cls) -> None:
        super(FaviconHashTest, cls).tearDownClass()
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
        Test favicon hash from the local server (favicon.ico with clown emodji)
        :return: None
        """
        response = self.runner.run(
            url=f"http://{DefaultValues.HOST}:{DefaultValues.PORT}"
        )
        self.assertIn("Successfully", response.get("message"))
        self.assertEqual(response.get("status"), "success")
        self.assertEqual(response.get("result"), -1285980612)


class FaviconHashFailTest(TestCase):
    """
    Defines basic tests for the Shodan favicon hash script, but on offline server
    """

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

    def test_no_response(self):
        """
        Tests module on offline server.
        """
        result = self.runner.run(
            url=f"http://{DefaultValues.HOST}:{DefaultValues.PORT}"
        )
        self.assertIsInstance(result, dict)
        self.assertIs(result["result"], None)
        self.assertIn("Error", result["message"])
