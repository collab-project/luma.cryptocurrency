# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

"""
Endpoint for coinmarketcap.com

:see: https://coinmarketcap.com/api/
"""

from . import Endpoint, EndpointResponse


class CoinmarketcapResponse(EndpointResponse):

    @property
    def data(self):
        return self.json_data[0]

    def parse_price(self):
        return float(self.data.get('price_usd'))

    def parse_timestamp(self):
        # timestamp = time.strftime('%m/%d/%Y %H:%M:%S',
        #    time.gmtime(int(record.get('last_updated'))))
        return self.data.get('last_updated')


class Coinmarketcap(Endpoint):
    responseType = CoinmarketcapResponse

    def get_url(self):
        base = 'https://api.coinmarketcap.com/{api_version}/ticker/{coin}/'

        return base.format(
            api_version=self.api_version,
            coin=self.coin
        )
