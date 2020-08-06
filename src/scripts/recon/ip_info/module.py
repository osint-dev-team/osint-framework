#!/usr/bin/env python3

import ipaddress

import requests

from src.core.base.recon import ReconRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Runner(ReconRunner):
    """
    Class that performs IP information check
    """
    required = ["ip"]

    def __init__(self, logger: str = __name__) -> None:
        super(Runner, self).__init__(logger)
        self.__BASE_URL = "http://ip-api.com/json/{query}?fields=18411513"

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        # fmt: off
        response = self.__get_ip_info(kwargs.get("ip"))

        try:
            msg = (
                "Query successful!"
                if response["status"] == "success"
                else "Query failed!"
            )
            # we don't need duplicate status, let's get rid of it
            response.pop("status", None)
            return ScriptResponse.success(result=response, message=msg)
        except TypeError as type_err:
            return ScriptResponse.error(message=f"Error occurred while trying to get data: error status")
        except Exception as unexp_err:
            return ScriptResponse.error(message=f"Error occurred while trying to get data: {str(unexp_err)}")
        # fmt: on

    def __get_ip_info(self, ip: str) -> dict or str:
        """
        A function for retrieving location and provider info by IP address. You can get the following information:
        - continent name
        - country name
        - region/state name
        - city name
        - district name
        - zip code
        - latitude
        - longitude
        - timezone
        - ISP name
        - organization name
        - AS number and organization, separated by space (RIR). Empty for IP blocks not being announced in BGP
          tables.
        - hosting, colocated or data center.

        :param ip: the IP address you want to know about.
        :return: string with error message in case of error or a dict with information about IP address.
        """

        try:
            validated_ip = str(ipaddress.ip_address(ip))
        except ValueError:
            return "Invalid IP address!"

        try:
            return requests.get(self.__BASE_URL.format(query=validated_ip)).json()
        except Exception as err_unexp:
            return "Unexpected error occurred: {}".format(str(err_unexp))
