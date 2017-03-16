# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import os
import time
import pprint

from PIL import ImageFont

from luma.core.serial import spi
from luma.core.render import canvas
from luma.oled.device import sh1106

from luma.cryptocurrency.interval import Interval
from luma.cryptocurrency.endpoint import get_bpi, format_bpi


def draw(eur, usd, timestamp):
    # font
    font_path = os.path.join('fonts', 'red-alert.ttf')

    default_font = ImageFont.truetype(font_path, 12)
    currency_font = ImageFont.truetype(font_path, 17)

    # draw
    with canvas(device) as draw:
        draw.text((0, 0), timestamp, font=default_font, fill="white")
        draw.text((0, 16), usd, font=currency_font, fill="white")
        draw.text((0, 38), eur, font=currency_font, fill="white")


if __name__ == "__main__":
    # device
    Serial = spi(port=0, device=0, bus_speed_hz=8000000)
    device = sh1106(serial_interface=Serial)

    def clock(start=None):
        """
        Prints out the elapsed time when called from start.
        """
        if start is None:
            start = time.time()

        elapsed = time.time() - start
        if elapsed > 0:
            print("elapsed: {:0.3f} seconds".format(elapsed))

        # BPI
        data_source = get_bpi
        data_format = format_bpi

        # marketcap
        # data_source = get_marketcap
        # data_format = format_marketcap

        data = data_source()
        eur, usd, timestamp = data_format(data)

        pprint.pprint(data)
        print("-" * 20)

        draw(eur, usd, timestamp)

    clock()

    # Create an interval.
    speed = 60
    interval = Interval(speed, clock, args=[time.time(), ])
    print("Starting {} second interval, press CTRL+C to stop.".format(speed))
    interval.start()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("Shutting down interval...")
            interval.stop()
            break