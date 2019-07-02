#!/usr/bin/env bash
bin/healthcare-protogen
python3 setup_rest_api.py clean --all
python3 setup_rest_api.py build
python3 setup_rest_api.py install

if [[ ! -f /root/.sawtooth/keys/clinicWEB.priv ]]; then
    sawtooth keygen clinicWEB
fi;

if [[ ! -f /root/.sawtooth/keys/doctorWEB.priv ]]; then
    sawtooth keygen doctorWEB
fi;

if [[ ! -f /root/.sawtooth/keys/patientWEB.priv ]]; then
    sawtooth keygen patientWEB
fi;
#healthcare-tp