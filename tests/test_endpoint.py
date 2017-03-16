# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import unittest

import requests
import requests_mock

from luma.cryptocurrency import endpoint


@requests_mock.Mocker()
class EndpointTestCase(unittest.TestCase):

    def test_get_bpi(self, m):
        m.register_uri('GET', 'https://api.coindesk.com/v1/bpi/currentprice.json', text='resp')
        f = endpoint.get_bpi()
        self.assertNotEqual(f, 'foo')
