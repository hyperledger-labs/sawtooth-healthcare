#!/usr/bin/env bash
bin/healthcare-protogen
python3 setup_rest_api.py clean --all
python3 setup_rest_api.py build
python3 setup_rest_api.py install
#healthcare-tp