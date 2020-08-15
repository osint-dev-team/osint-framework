#!/usr/bin/env python3

import ipaddress

from ipwhois import IPWhois

from src.core.base.recon import ReconRunner, PossibleKeys
from src.core.utils.response import ScriptResponse
from src.core.utils.validators import validate_kwargs


class Runner(ReconRunner):
    """
    Class that performs RDAP lookup.
    """

    required = ["ip"]

    def __init__(self, logger: str = __name__) -> None:
        super(Runner, self).__init__(logger)

    @validate_kwargs(PossibleKeys.KEYS)
    def run(self, *args, **kwargs) -> ScriptResponse.success or ScriptResponse.error:
        """
        A method that performs RDAP lookup. You can get the following information:
        - query - The IP address
        - asn - The Autonomous System Number
        - asn_date - The ASN Allocation date
        - asn_registry - The assigned ASN registry
        - asn_cidr - The assigned ASN CIDR
        - asn_country_code - The assigned ASN country code
        - asn_description - The ASN description
        - network - Network information which consists of the following fields:
            - cidr - Network routing block and IP address belongs to
            - country - Country code registered with the RIR in ISO 3166-1 format
            - end_address - The last IP address in a network block
            - events - List of event dictionaries with the following fields:
                - action - The reason for an event
                - timestamp - The date an event occured in ISO 8601 format
                - actor - The identifier for an event initiator (if any)
            - handle - Unique identifier for a registered object
            - ip_version - IP protocol version (v4 or v6) of an IP address
            - links - HTTP/HTTPS links provided for an RIR object
            - name - he identifier assigned to the network registration for an IP address
            - parent_handle - Unique identifier for the parent network of a registered network
            - start_address - The first IP address in a network block
            - status - List indicating the state of a registered object
            - type - The RIR classification of a registered network
        objects  - The objects (entities) referenced by an RIR network or by other entities with the following fields:
            - contact - Contact information registered with an RIR object. See "contacts" in "nir" section for more
                        info.
            - entities - List of object names referenced by an RIR object. Map these to other objects dictionary keys.
            - events - List of event dictionaries. See "events" in "network" section for more info.
            - events_actor - List of event (no actor) dictionaries
            - handle - Unique identifier for a registered object
            - links - List of HTTP/HTTPS links provided for an RIR object
            - roles - List of roles assigned to a registered object
            - status - List indicating the state of a registered object
        nir  - The National Internet Registry results which consists of the following fields:
            - cidr - Network routing block and IP address belongs to
            - range - Network range an IP address belongs to
            - name - he identifier assigned to the network registration for an IP address
            - handle - Unique identifier for a registered object
            - country - Country code registered with the RIR in ISO 3166-1 format
            - address - The mailing address for a registered network
            - postal_code - The postal code for a registered network
            - nameservers - he nameservers listed for a registered network
            - created - Network registration date in ISO 8601 format
            - updated - Network registration updated date in ISO 8601 format
            - contacts - Dictionary with keys: admin, tech. Values map to contact dictionaries if found:
                - name - The contact’s name
                - organization - The contact’s organization
                - division - The contact’s division of the organization
                - email - Contact email address
                - reply_email - Contact reply email address
                - updated - Updated date in ISO 8601 format
                - phone - Contact phone number
                - fax - Contact fax number
                - title - The contact’s position or job title

        :param args: variable length argument list.
        :param kwargs: arbitrary keyword arguments.

        :return: ScriptResponse.error with error message: returned if IP address is invalid or RDAP query failed.
                 ScriptResponse.success with RDAP lookup results: returned if IP address is valid and RDAP query was
                 successful.
        """

        try:
            ip = self.__validate_ip(kwargs.get("ip"))
        except ValueError:
            return ScriptResponse.error(message="Invalid IP address.")

        try:
            rdap = IPWhois(ip).lookup_rdap()
        except Exception as e:
            return ScriptResponse.error(
                message="RDAP lookup failed. Unknown error occurred: " + str(e)
            )

        # notices and remarks sections contains some useless info, let's get rid of it
        rdap["network"].pop("notices", None)

        for obj in rdap["objects"].keys():
            rdap["objects"][obj].pop("notices", None)
            rdap["objects"][obj].pop("remarks", None)

        # entities section contains objects section keys, so we don't need it
        rdap.pop("entities", None)

        return ScriptResponse.success(result=rdap, message="RDAP lookup successful.")

    @staticmethod
    def __validate_ip(ip: str):
        """
        A function that checks if IP address is valid and converts it to standard format.

        :param ip: IP address.

        :return: standard format of the provided IP address.

        :raises: ValueError: thrown when IP address is invalid.
        """

        try:
            return str(ipaddress.ip_address(ip))
        except ValueError as err:
            raise ValueError("Invalid IP address!") from err
