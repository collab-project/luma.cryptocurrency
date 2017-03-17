# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import json
import os.path

from PIL import ImageFont

import requests
import requests_cache
from requests.adapters import HTTPAdapter

from requests.packages.urllib3.util.retry import Retry


def get_reference_path(path):
    """
    :param path:
    :type path:
    """
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'reference',
        path
    ))


def request_json(url, timeout=4):
    """
    :param url:
    :type url:
    """
    with requests_cache.disabled():
        s = requests.Session()
        retries = Retry(total=5,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504])

        s.mount('https://', HTTPAdapter(max_retries=retries))

        try:
            response = s.get(url, timeout=timeout)
            return response.json()

        except requests.exceptions.ConnectionError:
            raise


def load_json_file(path):
    """
    :param path:
    :type path:
    """
    with open(path) as json_data:
        return json.load(json_data)


def make_font(name='red-alert.ttf', size=12):
    """
    Create new font instance.

    :param name:
    :type name:
    :param size:
    :type size:
    :return: A font object.
    """
    font_path = get_reference_path(os.path.join(
        'fonts', name))
    return ImageFont.truetype(font_path, size)


def get_module_name(obj):
    """
    Get module name for ``obj``, e.g.::

      from luma.cryptocurrency.endpoint.bpi import BPI
      get_module_name(BPI)  # returns 'bpi'
    """
    return obj.__module__.rsplit('.')[-1]
