#!/usr/bin/env python3

from pprint import pprint
from sys import argv

from .module import Runner

runner = Runner()
result = runner.run(
    phone=argv[1] if len(argv) >= 2 else "+79131161111",
    region=argv[2] if len(argv) >= 3 else "ru",
)
pprint(result)
