#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace, SUPPRESS


def parse_args() -> Namespace:
    """
    Parse command line arguments
    :return: Namespace containing arguments
    """
    parser = ArgumentParser(
        description="All-in-one OSINT/RECON Swiss Knife", usage=SUPPRESS
    )
    parser.add_argument(
        "-s",
        "--scenario",
        action="store",
        help="JSON/YAML file containing search cases",
    )
    return parser.parse_args()
