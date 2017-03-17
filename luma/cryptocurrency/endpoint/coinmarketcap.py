# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

"""
Endpoint for coinmarketcap.com

:see: https://coinmarketcap.com/api/
"""

import time

from . import Endpoint


class Coinmarketcap(Endpoint):

    @property
    def url(self):
        base = 'https://api.coinmarketcap.com/{api_version}/ticker/{coin}/'

        return base.format(
            api_version=self.api_version,
            coin=self.coin
        )

    def format(self, data):
        record = data[0]
        usd = 'USD {}'.format(record.get('price_usd'))
        timestamp = time.strftime('%m/%d/%Y %H:%M:%S',
            time.gmtime(int(record.get('last_updated'))))

        return usd, timestamp
