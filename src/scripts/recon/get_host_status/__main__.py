#!/usr/bin/env python3

from pprint import pprint
from sys import argv

from src.core.utils.module import run_module
from src.scripts.recon.get_host_status import module

result = run_module(module, args=argv, arg_name="url", arg_value="https://www.intel.com/")
pprint(result)
