#!/usr/bin/env python3

from pprint import pprint
from sys import argv

from src.core.utils.module import run_module
from src.scripts.other.simple_example import module

result = run_module(module, args=argv, arg_name="username", arg_value="johndoe")
pprint(result)
