# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import os
import time

from . import util


class Endpoint(object):
    """
    """
    def __init__(self, coin='bitcoin', currency='USD', api_version='v1',
                 timeout=4):
        self.coin = coin
        self.currency_code = currency
        self.api_version = api_version
        self.timeout = timeout
        self.currencies = self.get_supported_currencies()

        c = self.find_currency()
        if c is None:
            raise ValueError('currency not supported: {}'.format(
                self.currency_code))
        else:
            self.currency_country = c.get('country')

    def find_currency(self):
        return next((
            x for x in self.currencies if x.get('currency') == self.currency_code),
            None)

    def get_supported_currencies(self):
        json_path = util.get_reference_path(
            os.path.join('endpoint', self.id, self.api_version,
            'supported-currencies.json'))

        return util.load_json_file(json_path)

    def load(self):
        return util.request_json(self.url, timeout=self.timeout)


class BPI(Endpoint):
    """
    Endpoint for coindesk.com

    :see: https://www.coindesk.com/api/
    """
    id = 'bpi'

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


class Coinmarketcap(Endpoint):
    """
    Endpoint for coinmarketcap.com

    :see: https://coinmarketcap.com/api/
    """
    id = 'coinmarketcap'

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
