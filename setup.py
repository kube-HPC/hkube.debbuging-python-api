#!/usr/bin/env python

import setuptools
import os

here = os.path.abspath(os.path.dirname(__file__))

packages = setuptools.find_packages()

VERSION = '0.0.5'
requires = [
    'Events>=0.3',
    'websocket-client==0.53.0',
    'simplejson'
]

with open("README.md", "r") as f:
    long_description = f.read()

about = {}
with open(os.path.join(here, 'hkube_debbuging_python_api', '__version__.py'), 'r') as f:
    exec(f.read(), about)

setuptools.setup(
    name=about['__title__'],
    version=VERSION,
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    license=about['__license__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about['__url__'],
    packages=packages,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
