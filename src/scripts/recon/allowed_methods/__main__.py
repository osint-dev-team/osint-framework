#!/usr/bin/env python3

from pprint import pprint
from sys import argv

from src.core.utils.module import run_module
from src.scripts.recon.allowed_methods import module

result = run_module(module, args=argv, arg_name="url", arg_value="https://www.intel.com/")
pprint(result)
