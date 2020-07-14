#!/usr/bin/env python3

from src.core.case.base import BaseCase


class OsintCase(BaseCase):
    def __init__(self, *args, **kwargs):
        super(OsintCase, self).__init__(category="osint", *args, **kwargs)
