#!/usr/bin/env bash
bin/healthcare-protogen
cp -R common rest_api/rest_api
cp -R consent_common rest_api/rest_api
cd rest_api || exit
#python3 setup.py clean --bdist-base ./rest_api/bdist.linux-x86_64 --build-lib ./rest_api/lib --all
#python3 setup.py build -b ./rest_api install
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
#healthcare-tp