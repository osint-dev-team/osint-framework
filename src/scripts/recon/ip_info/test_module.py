from unittest import TestCase
from .module import Runner


class IPInfoTest(TestCase):
    def setUp(self) -> None:
        """
        Setup before each test function.

        :return: None
        """

        self.runner = Runner()

    def test_invalid_ip(self) -> None:
        """
        This test function tests the case where the user entered an invalid IP (it can't be converted to a valid IP).

        :return: None
        """

        res = self.runner.run(ip='abcde')

        self.assertEqual(res.get('status'), 'error')

    def test_valid_ip_regular_format(self) -> None:
        """
        This test function tests the case where the user entered a valid ip in regular format.
        This IP was found here: https://ip-api.com/docs/api:json

        :return: None
        """

        res = self.runner.run(ip='24.48.0.1')

        self.assertEqual(res.get('status'), 'success')
        self.assertEqual(res.get('result').get('city'), 'Montreal')

    def test_valid_ip_dec_format(self) -> None:
        """
        This test function tests the case where the user entered a valid ip in decimal format.
        This IP was found here: https://ip-api.com/docs/api:json

        :return: None
        """

        res = self.runner.run(ip=405798913)  # this IP is the same as IP in previous test function.

        self.assertEqual(res.get('status'), 'success')
        self.assertEqual(res.get('result').get('city'), 'Montreal')
