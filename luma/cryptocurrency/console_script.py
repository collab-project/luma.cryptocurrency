# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import sys
import logging

from luma.core import error, cmdline

from .ticker import run
from .endpoint import create_endpoint


def main(actual_args=None):
    """
    Entry point for console script.
    """
    if actual_args is None:
        actual_args = sys.argv[1:]

    # logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s - %(message)s'
    )
    # ignore debug messages
    logging.getLogger("PIL").setLevel(logging.ERROR)
    logging.getLogger("requests").setLevel(logging.ERROR)

    # parser
    device_parser = cmdline.create_parser(description='luma.cryptocurrency')
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
        config = cmdline.load_config(args.config)
        args = device_parser.parse_args(config + actual_args)

    # create endpoint
    ep = create_endpoint(args.source, args.coin, args.currency)

    # create device
    try:
        display_types = cmdline.get_display_types()
        device = cmdline.create_device(args, display_types)
    except error.Error as e:
        device_parser.error(e)

    run(device, ep)
