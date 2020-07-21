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
        Defines GET method
        :return: None
        """
        if self.path == "/":
            self.response_ok()

    def do_HEAD(self) -> None:
        """
        Defines HEAD method
        :return: None
        """
        if self.path == "/":
            self.response_other()

    def do_POST(self) -> None:
        """
        Defines POST method
        :return: None
        """
        if self.path == "/":
            self.response_ok()

    def do_PUT(self) -> None:
        """
        Defines PUT method
        :return: None
        """
        if self.path == "/":
            self.response_disallow()

    def do_DELETE(self) -> None:
        """
        Defines DELETE method
        :return: None
        """
        if self.path == "/":
            self.response_disallow()

    def do_CONNECT(self) -> None:
        """
        Defines CONNECT method
        :return: None
        """
        if self.path == "/":
            self.response_other()

    def do_OPTIONS(self) -> None:
        """
        Defines OPTIONS method
        :return: None
        """
        if self.path == "/":
            self.response_ok()

    def do_TRACE(self) -> None:
        """
        Defines TRACE method
        :return: None
        """
        if self.path == "/":
            self.response_disallow()

    def do_PATCH(self) -> None:
        """
        Defines PATCH method
        :return: None
        """
        if self.path == "/":
            self.response_disallow()

    def response_ok(self) -> None:
        """
        Simulate OK response.
        :return: None
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<html><body><i>Mock page from Mocking Class</i></body></html>"
        )

    def response_disallow(self) -> None:
        """
        Simulate METHOD-NOT-ALLOWED response.
        :return: None
        """
        self.send_response(405)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<html><body><i>Mock page from Mocking Class</i></body></html>"
        )

    def response_other(self) -> None:
        """
        Simulate response with code 300.
        :return: None
        """
        self.send_response(300)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<html><body><i>Mock page from Mocking Class</i></body></html>"
        )


class AllowedMethodsTest(TestCase):
    """
    Defines basic tests for allowed_methods
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
        super(AllowedMethodsTest, cls).setUpClass()
        cls.server = HTTPServer(
            server_address=(DefaultValues.HOST, DefaultValues.PORT),
            RequestHandlerClass=TestClassHTTPRequestHandler,
        )
        server_daemon = Thread(target=cls.server.serve_forever, daemon=True)
        server_daemon.start()

    @classmethod
    def tearDownClass(cls) -> None:
        super(AllowedMethodsTest, cls).tearDownClass()
        cls.server.shutdown()

    def test_create_runner(self) -> None:
        """
        Test creation of the class instance
        :return: None
        """
        self.assertIsNotNone(self.runner)
        self.assertIsInstance(self.runner, Runner)

    def test_methods(self):
        """
        Tests all methods on mocked server (responses are hardcoded)
        """
        result = self.runner.run(url = f"http://{DefaultValues.HOST}:{DefaultValues.PORT}")
        self.assertIsInstance(result, dict)
        self.assertIs(result['status'], 'success')
        self.assertEqual(len(result['result']['allowed']), 3)
        self.assertEqual(len(result['result']['filtered']), 21)
        self.assertEqual(len(result['result']['forbidden']), 4)
        self.assertEqual(len(result['result']['server_error']), 0)


class AllowedMethodsFailTest(TestCase):
    """
    Defines basic tests for the allowed_methods script, but on offline server
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
        result = self.runner.run(url=f"http://{DefaultValues.HOST}:{DefaultValues.PORT}")
        self.assertIsInstance(result, dict)
        self.assertIs(result['status'], 'success')
        self.assertEqual(len(result['result']['allowed']), 0)
        self.assertEqual(len(result['result']['filtered']), 0)
        self.assertEqual(len(result['result']['forbidden']), 0)
        self.assertEqual(len(result['result']['server_error']), 28)
