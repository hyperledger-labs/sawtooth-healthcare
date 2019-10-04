#!/usr/bin/env bash
bin/healthcare-protogen make_insurance_protobuf
cp -R insurance_common insurance_processor/processor
cd insurance_processor || exit
python3 setup.py clean --all
python3 setup.py build
python3 setup.py install