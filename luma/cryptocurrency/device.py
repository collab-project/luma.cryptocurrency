# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import sys

import luma.core.error

from .demo_opts import create_parser, load_config, create_device, display_types


def get_device(actual_args=None):
    """
    Create device from command-line arguments and return it.
    """
    if actual_args is None:
        actual_args = sys.argv[1:]
    parser = create_parser()

    # override defaults
    parser.set_defaults(
        display='pygame'
    )
    args = parser.parse_args(actual_args)

    if args.config:
        # load config from file
        config = load_config(args.config)
        args = parser.parse_args(config + actual_args)

    try:
        device = create_device(args, display_types)
    except luma.core.error.Error as e:
        parser.error(e)

    return device
