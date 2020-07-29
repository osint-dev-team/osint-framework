#!/usr/bin/env python3

from pprint import pprint
from sys import argv
from requests import get
from src.core.utils.module import run_module
from .module import Runner

result = run_module(Runner, args=argv, arg_name="ip", arg_default=get("https://ifconfig.me/").text)
pprint(result)
