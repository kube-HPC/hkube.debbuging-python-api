#!/bin/bash

set -exo pipefail

pip install -U -r tests/requirements.txt
python setup.py bdist_wheel
pip install $PWD/dist/*

pylint hkube_debbuging_python_api
pytest --cov=. --cov-report html tests/