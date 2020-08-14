#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from threading import Thread
from unittest import TestCase

from src.core.values.defaults import TestDefaults
from .module import Runner


DefaultValues = TestDefaults()


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

        original_run = self.runner.run

        def patch_run(*args, **kwargs):
            """
            Patch run function from module to provide request timeout, monkey patching boi!
            :param args: original args
            :param kwargs: original kwargs
            :return: results of the original 'runner.run' function
            """
            import src.scripts.recon.shodan_favicon_hash.module

            original_request = src.scripts.recon.shodan_favicon_hash.module.get

            def patch_request(*_args, **_kwargs):
                """
                Patch Python 'requests' module 'get' method to provide timeout
                :param _args: original args
                :param _kwargs: original kwargs
                :return: patched request
                """
                return original_request(
                    *_args, **_kwargs, timeout=DefaultValues.DOWN_TIMEOUT
                )

            # Wrap runner in timeout request
            src.scripts.recon.shodan_favicon_hash.module.get = patch_request
            original_run_results = original_run(*args, **kwargs)
            src.scripts.recon.shodan_favicon_hash.module.get = original_request

            return original_run_results

        self.runner.run = patch_run

        result = self.runner.run(
            url=f"http://{DefaultValues.HOST}:{DefaultValues.PORT}"
        )
        self.assertIsInstance(result, dict)
        self.assertIs(result["result"], None)
        self.assertIn("Error", result["message"])
