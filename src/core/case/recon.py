#!/usr/bin/env python3

from src.core.case.base import BaseCase


class ReconCase(BaseCase):
    def __init__(self, *args, **kwargs):
        super(ReconCase, self).__init__(category="recon", *args, **kwargs)
