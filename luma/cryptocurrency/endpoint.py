import time

import requests


def get_bpi():
    r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    result = r.json()

    return result


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
    url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
    r = requests.get(url)
    result = r.json()

    return result


def format_marketcap(data):
    record = data[0]
    usd = 'USD {}'.format(record.get('price_usd'))
    timestamp = time.gmtime(int(record.get('last_updated')))

    return usd, usd, time.strftime('%m/%d/%Y %H:%M:%S', timestamp)
