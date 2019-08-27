#!/usr/bin/env bash
bin/healthcare-protogen
cp -R common processor/processor
cd processor
#python3 setup.py clean --bdist-base ./processor/bdist.linux-x86_64 --build-lib ./processor/lib --all
#python3 setup.py build -b ./processor install
python3 setup.py clean --all
python3 setup.py build
python3 setup.py install
#healthcare-tp