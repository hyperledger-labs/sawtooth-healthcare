#!/usr/bin/env bash
bin/healthcare-protogen
cp -R common rest_api/rest_api
cp -R consent_common rest_api/rest_api
cp -R insurance_common rest_api/rest_api
cp -R payment_common rest_api/rest_api
cd rest_api || exit
python3 setup.py clean --all
python3 setup.py build
python3 setup.py install

if [[ ! -f /root/.sawtooth/keys/clinicWEB.priv ]]; then
    sawtooth keygen clinicWEB
fi;

if [[ ! -f /root/.sawtooth/keys/doctorWEB.priv ]]; then
    sawtooth keygen doctorWEB
fi;

if [[ ! -f /root/.sawtooth/keys/patientWEB.priv ]]; then
    sawtooth keygen patientWEB
fi;

if [[ ! -f /root/.sawtooth/keys/labWEB.priv ]]; then
    sawtooth keygen labWEB
fi;

if [[ ! -f /root/.sawtooth/keys/insuranceWEB.priv ]]; then
    sawtooth keygen insuranceWEB
fi;