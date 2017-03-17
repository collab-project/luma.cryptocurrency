# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.

import json
import os.path

import requests
import requests_cache


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
        try:
            response = requests.get(url, timeout=timeout)
            return response.json()

        except requests.exceptions.ConnectionError:
            print('Connection failed!')


def load_json_file(path):
    """
    :param path:
    :type path:
    """
    with open(path) as json_data:
        return json.load(json_data)
