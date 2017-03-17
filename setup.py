#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup


def read_file(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as r:
        return r.read()


README = read_file("README.rst")
CHANGES = read_file("CHANGES.rst")
version = read_file("VERSION.txt").strip()


setup(
    name="luma.cryptocurrency",
    version=version,
    author="Thijs Triemstra",
    author_email="info@collab.nl",
    description=("Monitor cryptocurrency statistics on tiny displays"),
    long_description="\n\n".join([README, CHANGES]),
    license="MIT",
    keywords="raspberry rpi oled lcd led display screen spi i2c bitcoin btc cryptocurrency currency",
    url="https://github.com/collab-project/luma.cryptocurrency",
    download_url="https://github.com/collab-project/luma.cryptocurrency/tarball/" + version,
    namespace_packages=['luma'],
    packages=['luma.cryptocurrency'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'luma-cryptocurrency = luma.cryptocurrency.console_script:main'
        ]
    },
    install_requires=[
        'luma.oled',
        'requests-cache',
        'dateutils'
    ],
    extras_require={
        'docs': [
            'sphinx >= 1.5.1'
        ],
        'qa': [
            'rstcheck',
            'flake8'
        ],
        'test': [
            'requests-mock',
            'coverage>=4.0'
        ]
    },
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: System :: Hardware",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ]
)
