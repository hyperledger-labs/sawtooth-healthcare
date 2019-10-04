#!/usr/bin/env bash
bin/healthcare-protogen make_payment_protobuf
cp -R payment_common payment_processor/payment_processor
cd payment_processor || exit
python3 setup.py clean --all
python3 setup.py build
python3 setup.py install