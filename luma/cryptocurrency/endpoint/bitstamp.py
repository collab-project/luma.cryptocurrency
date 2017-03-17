# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

"""
Endpoint for bitstamp.net

:see: https://www.bitstamp.net/api/
"""

from datetime import datetime

from dateutil.tz.tz import tzutc

from . import Endpoint, EndpointResponse


class BitstampResponse(EndpointResponse):

    def parse_price(self):
        return float(self.json_data.get('last'))

    def parse_timestamp(self):
        return datetime.fromtimestamp(
            int(self.json_data.get('timestamp')), tz=tzutc())


class Bitstamp(Endpoint):
    api_version = 'v2'
    responseType = BitstampResponse

    def get_url(self):
        base = 'https://www.bitstamp.net/api/{api_version}/ticker/btc{currency}/'

        return base.format(
            currency=self.currency_code.lower(),
            api_version=self.api_version
        )
