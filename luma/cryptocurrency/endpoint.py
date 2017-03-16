# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import time

import requests


def get_json(url):
    r = requests.get(url)
    result = r.json()

    return result


def get_bpi():
    return get_json('https://api.coindesk.com/v1/bpi/currentprice.json')


def format_bpi(data):
    bpi = data.get('bpi')
    timestamp = data.get('time').get('updated')

    # format
    eur = '{} {}'.format(
        bpi.get('EUR').get('code'),
        bpi.get('EUR').get('rate')
    )
    usd = '{} {}'.format(
        bpi.get('USD').get('code'),
        bpi.get('USD').get('rate')
    )

    return eur, usd, timestamp


def get_marketcap():
    return get_json('https://api.coinmarketcap.com/v1/ticker/bitcoin/')


def format_marketcap(data):
    record = data[0]
    usd = 'USD {}'.format(record.get('price_usd'))
    timestamp = time.gmtime(int(record.get('last_updated')))

    return usd, usd, time.strftime('%m/%d/%Y %H:%M:%S', timestamp)
