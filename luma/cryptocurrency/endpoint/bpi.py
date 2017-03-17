# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

"""
Endpoint for coindesk.com

:see: https://www.coindesk.com/api/
"""

from . import Endpoint


class BPI(Endpoint):

    @property
    def url(self):
        base = 'https://api.coindesk.com/{api_version}/bpi/currentprice/{currency}.json'

        return base.format(
            currency=self.currency_code,
            api_version=self.api_version
        )

    def format(self, data):
        record = data.get('bpi')
        timestamp = data.get('time').get('updated')

        # format
        usd = '{} {}'.format(
            record.get('USD').get('code'),
            record.get('USD').get('rate')
        )

        return usd, timestamp
