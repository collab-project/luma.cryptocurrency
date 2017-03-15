# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import unittest

from luma.cryptocurrency import endpoint


class EndpointTestCase(unittest.TestCase):

    def test_get_bpi(self):
        endpoint.get_bpi()
