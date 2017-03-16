# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import time

import requests
import requests_cache


class Endpoint(object):
    currency = 'USD'

    def get_json(self, url):
        with requests_cache.disabled():
            response = requests.get(url)
        result = response.json()
        return result

    def load(self):
        return self.get_json(self.url)


class BPI(Endpoint):
    @property
    def url(self):
        base = 'https://api.coindesk.com/v1/bpi/currentprice/{currency}.json'

        return base.format(
            currency=self.currency
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
    @property
    def url(self):
        return 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'

    def format(self, data):
        record = data[0]
        usd = 'USD {}'.format(record.get('price_usd'))
        timestamp = time.strftime('%m/%d/%Y %H:%M:%S',
            time.gmtime(int(record.get('last_updated'))))

        return usd, timestamp
