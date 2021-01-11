#!/bin/bash

set -ex

pip install coveralls
coverage run --source=hkube_debbuging_python_api -m pytest tests/
coveralls