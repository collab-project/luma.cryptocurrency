# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import os

from .. import util


class EndpointResponse(object):
    """
    """
    def __init__(self, json_data):
        self.json_data = json_data

    def format(self):
        pass


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
        json_data = util.request_json(self.url, timeout=self.timeout)
        response = EndpointResponse(json_data)

        return response
