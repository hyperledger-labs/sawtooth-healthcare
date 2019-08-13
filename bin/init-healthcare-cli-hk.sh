#!/usr/bin/env bash
bin/healthcare-protogen
#python3 setup_cli_hk.py clean --bdist-base ./cli_hk/bdist.linux-x86_64 --build-lib ./cli_hk/lib --all
#python3 setup_cli_hk.py build -b ./cli_hk install
python3 setup_cli_hk.py clean --all
python3 setup_cli_hk.py build
python3 setup_cli_hk.py install

#if [[ ! -f /root/.sawtooth/keys/clinicCLI.priv ]]; then
#    sawtooth keygen clinicCLI
#fi;
#
#if [[ ! -f /root/.sawtooth/keys/doctorCLI.priv ]]; then
#    sawtooth keygen doctorCLI
#fi;
#
#if [[ ! -f /root/.sawtooth/keys/patientCLI.priv ]]; then
#    sawtooth keygen patientCLI
#fi;
#healthcare-tp