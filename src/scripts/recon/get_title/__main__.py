#!/usr/bin/env python3

from pprint import pprint
from sys import argv

from src.core.utils.module import run_module
from .module import Runner

result = run_module(
    Runner, args=argv, arg_name="url", arg_default="https://www.vk.com/"
)
pprint(result)
