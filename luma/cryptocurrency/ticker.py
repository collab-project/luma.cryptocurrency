# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import logging

from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator

from .endpoint import BPI
from .util import make_font


logger = logging.getLogger()


def run(device):
    regulator = framerate_regulator(fps=1)

    # font
    default_font = make_font()
    currency_font = make_font(size=17)

    # BPI
    ep = BPI()
    result = ep.load()

    try:
        while True:
            with regulator:
                # draw
                with canvas(device) as draw:
                    usd, timestamp = ep.format(result)
                    draw.text((0, 0), timestamp, font=default_font, fill="white")
                    draw.text((0, 16), usd, font=currency_font, fill="white")

            if regulator.called % 61 == 0:
                result = ep.load()
                logger.debug("-" * 20)

    except KeyboardInterrupt:
        pass
