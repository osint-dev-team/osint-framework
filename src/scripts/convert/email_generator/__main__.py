#!/usr/bin/env python3
from pprint import pprint
from sys import argv

from src.core.utils.module import run_module
from src.scripts.convert.email_generator.module import Runner

result = run_module(Runner, args=argv, arg_name="username", arg_default="john.doe")
pprint(result)
