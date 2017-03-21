# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import sys
import logging

import luma.core.error

from .ticker import run
from .endpoint import create_endpoint

from .demo_opts import create_parser, load_config, create_device, display_types


def main(actual_args=None):
    """
    Entry point for console script.
    """
    if actual_args is None:
        actual_args = sys.argv[1:]

    # ignore requests debug messages
    logging.getLogger("requests").setLevel(logging.ERROR)

    # parser
    device_parser = create_parser()
    subparsers = device_parser.add_subparsers()

    # override defaults
    device_parser.set_defaults(
        display='pygame'
    )

    # app parsers
    ticker = subparsers.add_parser('ticker', help='bar', description='foo')
    extra_group = ticker.add_argument_group('General')
    extra_group.add_argument('--source', default='coinmarketcap',
        help='Data provider.')
    extra_group.add_argument('--coin', default='bitcoin',
        help='Coin.')
    extra_group.add_argument('--currency', default='USD',
        help='Currency.')

    args = device_parser.parse_args(actual_args)
    if args.config:
        # load config from file
        config = load_config(args.config)
        args = device_parser.parse_args(config + actual_args)

    # create endpoint
    ep = create_endpoint(args.source, args.coin, args.currency)

    # create device
    try:
        device = create_device(args, display_types)
    except luma.core.error.Error as e:
        device_parser.error(e)

    run(device, ep)
