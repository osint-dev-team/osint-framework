import ipaddress

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

from src.core.base.recon import ReconRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs

BASE_URL = 'http://ip-api.com/json/{query}?fields=18411513'


class Runner(ReconRunner):
    def __init__(self, logger: str = __name__) -> None:
        super(Runner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        response = self.__get_ip_info(kwargs.get('ip'))

        if type(response) == dict:
            msg = 'Query successful!' if response['status'] == 'success' else 'Query failed!'
            response.pop('status', None)  # we don't need duplicate status, let's get rid of it

            result = ScriptResponse.success(result=response, message=msg)
        else:
            result = ScriptResponse.error(result=response, message='Error occurred while trying to get data!')

        return result

    @staticmethod
    def __get_ip_info(ip: str):
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
            ipaddress.ip_address(ip)
        except ValueError:
            return 'Invalid IP address!'

        try:
            ipaddress.ip_address(ip)

            try:
                response = requests.get(BASE_URL.format(query=ip)).json()
            except HTTPError as err_http:
                response = 'HTTP error occurred: {}'.format(err_http)
            except ConnectionError as err_conn:
                response = 'Connection error occurred: {}'.format(err_conn)
            except Timeout as err_timeout:
                response = 'Timeout error occurred: {}'.format(err_timeout)
            except RequestException as err:
                response = 'Catastrophic error occurred: {}'.format(err)
        except ValueError:
            response = 'Invalid IP address!'

        return response


r = Runner()
res = r.run(ip='24.0.0.1')
print(res)
