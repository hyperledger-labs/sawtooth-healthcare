#!/usr/bin/env bash
bin/healthcare-protogen
python3 setup.py clean --all
python3 setup.py build
python3 setup.py install
#healthcare-tp