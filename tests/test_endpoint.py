# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

from unittest import TestCase
from datetime import datetime

from dateutil.tz.tz import tzutc

import requests_mock

from requests.exceptions import ConnectionError

from luma.cryptocurrency.endpoint import bpi, coinmarketcap, bitstamp

from .helpers import get_reference_json


class EndpointTest(object):
    api_version = None
    currency = 'USD'
    currency_country = 'United States Dollar'
    price_in_btc = 1

    def setUp(self):
        self.ep = self.endpointClass(
            currency=self.currency,
            api_version=self.api_version
        )

    @requests_mock.Mocker()
    def assert_valid_response(self, m):
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

    @requests_mock.Mocker()
    def assert_connection_error(self, exc, m):
        self.reference = get_reference_json(self.ref_json)
        m.register_uri('GET', self.ep.get_url(), exc=exc)

        with self.assertRaises(exc):
            self.ep.load()

    def test_load(self):
        self.reference = get_reference_json(self.ref_json)
        self.assert_valid_response()

    def test_connection_error(self):
        self.assert_connection_error(ConnectionError)

    def test_get_supported_currencies(self):
        currencies = self.ep.get_supported_currencies()

        self.assertTrue(len(currencies) > 0)
        self.assertEqual(self.ep.currency_country, self.currency_country)

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


class BPITestCase(EndpointTest, TestCase):
    api_version = 'v1'
    currency = 'CNY'
    currency_country = 'Chinese Yuan'
    endpointClass = bpi.BPI
    ref_json = 'bpi/v1/currentprice/bitcoin/CNY.json'

    price = 7952.5275
    timestamp = datetime(2017, 3, 16, 1, 25, tzinfo=tzutc())


class BitstampTestCase(EndpointTest, TestCase):
    endpointClass = bitstamp.Bitstamp
    ref_json = 'bitstamp/v2/currentprice/bitcoin/USD.json'

    price = 1103.2
    timestamp = datetime(2017, 3, 17, 3, 45, 13, tzinfo=tzutc())


class CoinmarketcapUSDTestCase(EndpointTest, TestCase):
    currency = 'USD'
    endpointClass = coinmarketcap.Coinmarketcap
    ref_json = 'coinmarketcap/v1/currentprice/bitcoin/USD.json'

    price = 1255.26
    timestamp = datetime(2017, 3, 16, 0, 59, 26, tzinfo=tzutc())


class CoinmarketcapConversionTestCase(CoinmarketcapUSDTestCase):
    currency = 'EUR'
    currency_country = 'Euro'
    ref_json = 'coinmarketcap/v1/currentprice/bitcoin/EUR.json'

    price = 966.41690066
    timestamp = datetime(2017, 3, 29, 22, 44, 6, tzinfo=tzutc())
