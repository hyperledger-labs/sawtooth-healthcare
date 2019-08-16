#!/usr/bin/env bash
bin/healthcare-protogen
#python3 setup_cli.py clean --bdist-base ./cli/bdist.linux-x86_64 --build-lib ./cli/lib --all
#python3 setup_cli.py build -b ./cli install
python3 setup_cli.py clean --all
python3 setup_cli.py build
python3 setup_cli.py install

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