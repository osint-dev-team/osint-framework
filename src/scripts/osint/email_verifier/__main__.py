#!/usr/bin/env python3

from pprint import pprint
from sys import argv

from src.core.utils.module import run_module
from src.scripts.osint.email_verifier import module

result = run_module(module, args=argv, arg_name="email", arg_value="johndoe@gmail.com")
pprint(result)
