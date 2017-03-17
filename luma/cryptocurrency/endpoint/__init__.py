# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import os.path

from .. import util


__all__ = ["Endpoint", "EndpointResponse"]


class EndpointResponse(object):
    """
    """
    def __init__(self, json_data, currency_code):
        self.json_data = json_data
        self.currency_code = currency_code
        self.price = self.parse_price()
        self.price_in_btc = self.parse_price_in_btc()
        self.timestamp = self.parse_timestamp()


class Endpoint(object):
    """
    Basic endpoint.
    """
    api_version = 'v1'
    responseType = EndpointResponse

    def __init__(self, coin='bitcoin', currency='USD', api_version=None,
                 timeout=4):
        self.coin = coin
        self.currency_code = currency
        if api_version is not None:
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
        """
        :rtype: dict
        """
        return next((
            x for x in self.currencies if x.get('currency') == self.currency_code),
            None)

    def get_supported_currencies(self):
        """
        :rtype: dict
        """
        json_path = util.get_reference_path(
            os.path.join('endpoint', util.get_module_name(self),
            self.api_version, 'supported-currencies.json'))

        return util.load_json_file(json_path)

    def load(self):
        """
        :rtype: dict
        """
        json_data = util.request_json(self.get_url(), timeout=self.timeout)
        response = self.responseType(json_data, self.currency_code)

        return response
