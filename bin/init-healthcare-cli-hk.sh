#!/usr/bin/env bash
bin/healthcare-protogen
cp -R common cli_hk/cli
cd cli_hk
#python3 setup.py clean --bdist-base ./cli_hk/bdist.linux-x86_64 --build-lib ./cli_hk/lib --all
#python3 setup.py build -b ./cli_hk install
python3 setup.py clean --all
python3 setup.py build
python3 setup.py install

if [[ ! -f /root/.sawtooth/keys/clinicCLI.priv ]]; then
    sawtooth keygen clinicCLI
fi;

if [[ ! -f /root/.sawtooth/keys/doctorCLI.priv ]]; then
    sawtooth keygen doctorCLI
fi;

if [[ ! -f /root/.sawtooth/keys/patientCLI.priv ]]; then
    sawtooth keygen patientCLI
fi;
#healthcare-tp