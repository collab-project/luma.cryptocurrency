# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import logging

from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator

from .util import make_font
from .endpoint.bpi import BPI


logger = logging.getLogger()


def run(device):
    regulator = framerate_regulator(fps=1)

    # font
    default_font = make_font()
    currency_font = make_font(size=17)

    # BPI endpoint
    ep = BPI()
    data = ep.load()

    try:
        while True:
            with regulator:
                # draw
                with canvas(device) as draw:
                    draw.text((0, 0), data.timestamp.isoformat(' '), font=default_font, fill="white")
                    draw.text((0, 16), str(data.price), font=currency_font, fill="white")

            if regulator.called % 60 == 0:
                # reload
                data = ep.load()
                logger.debug("-" * 20)

    except KeyboardInterrupt:
        pass
