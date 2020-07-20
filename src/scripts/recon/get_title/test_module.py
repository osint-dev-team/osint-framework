#!/usr/bin/env python3

from unittest import TestCase
from .module import Runner
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread


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


class GetTitleTest(TestCase):

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
        super(GetTitleTest, cls).setUpClass()
        cls.server = HTTPServer(
            server_address=(DefaultValues.HOST, DefaultValues.PORT),
            RequestHandlerClass=TestClassHTTPRequestHandler,
        )
        server_daemon = Thread(target=cls.server.serve_forever, daemon=True)
        server_daemon.start()

    @classmethod
    def tearDownClass(cls) -> None:
        super(GetTitleTest, cls).tearDownClass()
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
            url="http://{HOST}:{PORT}".format(
                HOST=DefaultValues.HOST, PORT=DefaultValues.PORT
            )
        )
        self.assertEqual(response.get("status"), "success")

    def test_remote_server(self) -> None:
        """
        Test values from the remote server
        :return: None
        """
        response = self.runner.run(url=f"https://facebook.com")
        self.assertEqual(response.get("status"), "success")