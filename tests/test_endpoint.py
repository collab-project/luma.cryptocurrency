# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import unittest

import requests_mock

from luma.cryptocurrency import endpoint

from .helpers import get_reference_json


class EndpointTest(object):
    def setUp(self):
        self.ep = self.endpointClass()

    @requests_mock.Mocker()
    def assert_endpoint(self, m):
        m.register_uri('GET', self.ep.url, json=self.reference,
            status_code=200)
        result = self.ep.load()

        self.assertEqual(result.json_data, self.reference)

    def test_load(self):
        self.reference = get_reference_json(self.ref_json)
        self.assert_endpoint()

    def test_supported_currencies(self):
        currencies = self.ep.get_supported_currencies()

        self.assertTrue(len(currencies) > 0)
        self.assertEqual(self.ep.currency_country, "United States Dollar")

    def test_unsupported_currency(self):
        currency = 'foo'
        with self.assertRaises(ValueError) as cm:
            self.endpointClass(currency=currency)

        self.assertEqual(str(cm.exception),
            'currency not supported: {}'.format(currency))


class BPITestCase(EndpointTest, unittest.TestCase):
    endpointClass = endpoint.BPI
    ref_json = 'bpi/v1/currentprice/bitcoin/USD.json'


class CoinmarketcapTestCase(EndpointTest, unittest.TestCase):
    endpointClass = endpoint.Coinmarketcap
    ref_json = 'coinmarketcap/v1/currentprice/bitcoin/USD.json'
