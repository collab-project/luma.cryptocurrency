# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

from .ticker import run
from .device import get_device


def main():
    """
    Entry point for console script.
    """
    device = get_device()
    run(device)
