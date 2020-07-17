#!/usr/bin/env python3

from pprint import pprint
from sys import argv

from src.core.utils.module import run_module
from src.scripts.osint.region_check import module

result = run_module(module, args=argv, arg_name="phone", arg_value="89138811111")
pprint(result)
