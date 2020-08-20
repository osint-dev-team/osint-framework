#!/usr/bin/env python3

from unittest import TestCase
from .module import Runner


class DefaultValues:
    # Set Google DNS Resolver as the default host to test
    HOST_IP = "8.8.8.8"
    HOST_IP_DECIMAL = 134744072
    HOST_ASN = "15169"
    HOST_NETWORK_CIDR = "8.8.8.0/24"


class RDAPTest(TestCase):
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

        res = self.runner.run(ip="abcde")

        self.assertEqual(res.get("status"), "error")

    def test_valid_ip_regular_format(self) -> None:
        """
        This test function tests the case where the user entered a valid ip in regular format.

        :return: None
        """

        res = self.runner.run(ip=DefaultValues.HOST_IP)

        self.assertEqual(res.get("status"), "success")
        self.assertEqual(res.get("result").get("asn"), DefaultValues.HOST_ASN)
        self.assertEqual(
            res.get("result").get("network").get("cidr"),
            DefaultValues.HOST_NETWORK_CIDR,
        )

    def test_valid_ip_dec_format(self) -> None:
        """
        This test function tests the case where the user entered a valid ip in decimal format.

        :return: None
        """

        # this IP is the same as IP in previous test function.
        res = self.runner.run(ip=DefaultValues.HOST_IP_DECIMAL)

        self.assertEqual(res.get("status"), "success")
        self.assertEqual(res.get("result").get("asn"), DefaultValues.HOST_ASN)
        self.assertEqual(
            res.get("result").get("network").get("cidr"),
            DefaultValues.HOST_NETWORK_CIDR,
        )
