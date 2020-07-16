import ipaddress
import json

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

BASE_URL = 'http://ip-api.com/json/{query}?fields=18411513'


def get_ip_info(ip: str) -> dict or str:
    """

    :param ip: the IP address you want to know about.
    :return: string with error message in case of error or a dict with information about IP address.
    """
    try:
        ipaddress.ip_address(ip)

        try:
            response = json.loads(requests.get(BASE_URL.replace('{query}', ip)).text)
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
