# -*- coding: utf-8 -*-
# Copyright (c) 2017 Thijs Triemstra and contributors
# See LICENSE.rst for details.


import json
import os.path


def get_reference_path(fname):
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'reference',
        fname
    ))


def get_reference_json(fname):
    path = get_reference_path(fname)
    with open(path) as json_data:
        return json.load(json_data)
