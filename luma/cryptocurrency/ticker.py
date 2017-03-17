# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import logging

from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator

from .util import make_font


logger = logging.getLogger()


def format_data(ep):
    data = ep.load()

    data.price = '{} {}'.format(data.currency_code, str(data.price))
    data.timestamp = data.timestamp.isoformat(' ')

    logger.debug('{} {}'.format(data.price, "*" * 10))
    return data


def run(device):
    regulator = framerate_regulator(fps=1)

    # font
    default_font = make_font()
    currency_font = make_font(size=17)

    # endpoint
    from .endpoint.coinmarketcap import Coinmarketcap
    from .endpoint.bpi import BPI
    # ep = Coinmarketcap(coin='ethereum', currency='EUR')
    ep = BPI()
    data = format_data(ep)

    try:
        while True:
            with regulator:
                # draw
                with canvas(device) as draw:
                    draw.text((0, 0), data.timestamp, font=default_font, fill="white")
                    draw.text((0, 16), data.price, font=currency_font, fill="white")

            if regulator.called % 60 == 0:
                # reload
                data = format_data(ep)

    except KeyboardInterrupt:
        pass
