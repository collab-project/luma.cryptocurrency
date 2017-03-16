# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import unittest

import requests_mock

from luma.cryptocurrency import endpoint

from .helpers import get_reference_json


class EndpointTestCase(unittest.TestCase):

    @requests_mock.Mocker()
    def assert_endpoint(self, ep, m):
        m.register_uri('GET', ep.url, json=self.reference, status_code=200)
        result = ep.load()
        self.assertEqual(result, self.reference)

    def test_load_bpi(self):
        self.reference = get_reference_json('bpi/currentprice/USD.json')
        ep = endpoint.BPI()
        ep.currency = 'USD'

        self.assert_endpoint(ep)

    def test_load_coinmarketcap(self):
        self.maxDiff = None
        self.reference = get_reference_json('coinmarketcap.json')
        ep = endpoint.Coinmarketcap()

        self.assert_endpoint(ep)
