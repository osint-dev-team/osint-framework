from pprint import pprint
from sys import argv

from src.core.utils.module import run_module
from .module import Runner

result = run_module(Runner, args=argv, arg_name="ip", arg_default="8.8.8.8")

pprint(result)
