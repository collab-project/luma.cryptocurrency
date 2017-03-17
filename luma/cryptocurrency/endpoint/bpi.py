# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

"""
Endpoint for coindesk.com

:see: https://www.coindesk.com/api/
"""

from dateutil.parser import parse

from . import Endpoint, EndpointResponse


class BPIResponse(EndpointResponse):

    def parse_price(self):
        return self.json_data.get('bpi').get('USD').get('rate_float')

    def parse_timestamp(self):
        timestamp = parse(self.json_data.get('time').get('updatedISO'))
        return timestamp


class BPI(Endpoint):
    responseType = BPIResponse

    def get_url(self):
        base = 'https://api.coindesk.com/{api_version}/bpi/currentprice/{currency}.json'

        return base.format(
            currency=self.currency_code,
            api_version=self.api_version
        )
