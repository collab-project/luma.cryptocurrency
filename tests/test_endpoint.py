# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import unittest
from datetime import datetime

from dateutil.tz.tz import tzutc

import requests_mock

from luma.cryptocurrency.endpoint import bpi, coinmarketcap

from .helpers import get_reference_json


class EndpointTest(object):
    def setUp(self):
        self.ep = self.endpointClass()

    @requests_mock.Mocker()
    def assert_response(self, m):
        """
        A valid EndpointResponse is returned.
        """
        m.register_uri('GET', self.ep.get_url(), json=self.reference,
            status_code=200)
        result = self.ep.load()

        self.assertEqual(result.json_data, self.reference)
        self.assertEqual(result.price, self.price)
        self.assertEqual(result.price_in_btc, self.price_in_btc)
        self.assertEqual(result.timestamp, self.timestamp)

    def test_load(self):
        self.reference = get_reference_json(self.ref_json)
        self.assert_response()

    def test_supported_currencies(self):
        currencies = self.ep.get_supported_currencies()

        self.assertTrue(len(currencies) > 0)
        self.assertEqual(self.ep.currency_country, "United States Dollar")

    def test_supported_currency(self):
        currency = 'EUR'
        ep = self.endpointClass(currency=currency)

        self.assertEqual(ep.currency_country, "Euro")

    def test_unsupported_currency(self):
        currency = 'foo'
        with self.assertRaises(ValueError) as cm:
            self.endpointClass(currency=currency)

        self.assertEqual(str(cm.exception),
            'currency not supported: {}'.format(currency))


class BPITestCase(EndpointTest, unittest.TestCase):
    endpointClass = bpi.BPI
    ref_json = 'bpi/v1/currentprice/bitcoin/USD.json'

    price = 1259.232
    price_in_btc = 1
    timestamp = datetime(2017, 3, 16, 1, 26, tzinfo=tzutc())


class CoinmarketcapTestCase(EndpointTest, unittest.TestCase):
    endpointClass = coinmarketcap.Coinmarketcap
    ref_json = 'coinmarketcap/v1/currentprice/bitcoin/USD.json'

    price = 1255.26
    price_in_btc = 1
    timestamp = datetime(2017, 3, 16, 0, 59, 26, tzinfo=tzutc())
