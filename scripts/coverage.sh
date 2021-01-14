#!/bin/bash

set -ex

pip install coveralls
pip install -r tests/requirements.txt
python setup.py bdist_wheel
pip install $PWD/dist/*
coverage --service=github run --source=hkube_debbuging_python_api -m pytest tests/
coveralls