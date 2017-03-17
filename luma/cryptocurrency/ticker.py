# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import os
import time
import pprint
import logging

from PIL import ImageFont

from luma.core.render import canvas

from .endpoint import BPI
from .interval import Interval
from .util import get_reference_path


logger = logging.getLogger()


def render(device, usd, timestamp):
    # font
    font_path = get_reference_path(os.path.join(
        'fonts', 'red-alert.ttf'))

    default_font = ImageFont.truetype(font_path, 12)
    currency_font = ImageFont.truetype(font_path, 17)

    # draw
    with canvas(device) as draw:
        draw.text((0, 0), timestamp, font=default_font, fill="white")
        draw.text((0, 16), usd, font=currency_font, fill="white")


def clock(start=None, device=None):
    """
    Prints out the elapsed time when called from start.
    """
    if start is None:
        start = time.time()

    elapsed = time.time() - start
    if elapsed > 0:
        logger.debug("elapsed: {:0.3f} seconds".format(elapsed))

    # BPI
    ep = BPI()

    result = ep.load()
    usd, timestamp = ep.format(result)

    pprint.pprint(result)
    logger.debug("-" * 20)

    render(device, usd, timestamp)


def run(device):

    # ignore requests debug messages
    logging.getLogger("requests").setLevel(logging.ERROR)

    clock(device=device)

    # Create an interval.
    #speed = 60
    #interval = Interval(speed, clock, args=[time.time(), device])
    #logger.info("Starting {} second interval, press CTRL+C to stop.".format(
    #    speed))
    #interval.start()

    #while True:
    #    try:
    #        time.sleep(0.1)
    #    except KeyboardInterrupt:
    #        print("Shutting down interval...")
    #        interval.stop()
    #        break
