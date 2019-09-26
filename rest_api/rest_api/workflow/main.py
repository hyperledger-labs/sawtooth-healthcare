# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

import argparse
import asyncio
import logging
import os
from signal import signal, SIGINT
import sys
# import rethinkdb as r

from sanic import Sanic

from sawtooth_signing import create_context
from sawtooth_signing import ParseError
# from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_signing import CryptoFactory

# from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from zmq.asyncio import ZMQEventLoop
from rest_api.workflow.claims import CLAIMS_BP
from rest_api.workflow.clinics import CLINICS_BP
from rest_api.workflow.general import get_keyfile, get_signer_from_file
from rest_api.workflow.doctors import DOCTORS_BP
from rest_api.workflow.labs import LABS_BP
from rest_api.workflow.patients import PATIENTS_BP
from rest_api.workflow.insurances import INSURANCES_BP
from rest_api.workflow.clients import CLIENTS_BP
from rest_api.workflow.claim_details import CLAIM_DETAILS_BP
from rest_api.workflow.lab_tests import LAB_TESTS_BP
from rest_api.workflow.pulse import PULSE_BP
from sawtooth_rest_api.messaging import Connection

# from api.authorization import AUTH_BP
# from api.errors import ERRORS_BP
# from api.holdings import HOLDINGS_BP
# from api.offers import OFFERS_BP

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
DEFAULT_CONFIG = {
    'HOST': 'localhost',
    'PORT': 8000,
    'TIMEOUT': 500,
    'VALIDATOR_URL': 'tcp://localhost:4004',
    # 'DB_HOST': 'localhost',
    # 'DB_PORT': 28015,
    # 'DB_NAME': 'marketplace',
    'DEBUG': True,
    'KEEP_ALIVE': False,
    'SECRET_KEY': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890',
    'AES_KEY': 'ffffffffffffffffffffffffffffffff',
    'BATCHER_PRIVATE_KEY': '1111111111111111111111111111111111111111111111111111111111111111',
    'BATCHER_PRIVATE_KEY_FILE_NAME_CLINIC': None,
    'BATCHER_PRIVATE_KEY_FILE_NAME_PATIENT': None,
    'BATCHER_PRIVATE_KEY_FILE_NAME_DOCTOR': None,
    'BATCHER_PRIVATE_KEY_FILE_NAME_LAB': None,
    'BATCHER_PRIVATE_KEY_FILE_NAME_INSURANCE': None
}


async def open_connections(appl):
    # LOGGER.warning('opening database connection')
    # r.set_loop_type('asyncio')
    # app.config.DB_CONN = await r.connect(
    #     host=app.config.DB_HOST,
    #     port=app.config.DB_PORT,
    #     db=app.config.DB_NAME)

    appl.config.VAL_CONN = Connection(appl.config.VALIDATOR_URL)

    LOGGER.warning('opening validator connection: ' + str(appl.config.VALIDATOR_URL))
    appl.config.VAL_CONN.open()


def close_connections(appl):
    # LOGGER.warning('closing database connection')
    # app.config.DB_CONN.close()

    LOGGER.warning('closing validator connection')
    appl.config.VAL_CONN.close()


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        help='The host for the api to run on.')
    parser.add_argument('--port',
                        help='The port for the api to run on.')
    parser.add_argument('--timeout',
                        help='Seconds to wait for a validator response')
    parser.add_argument('--validator',
                        help='The url to connect to a running validator')
    # parser.add_argument('--db-host',
    #                     help='The host for the state database')
    # parser.add_argument('--db-port',
    #                     help='The port for the state database')
    # parser.add_argument('--db-name',
    #                     help='The name of the database')
    parser.add_argument('--debug',
                        help='Option to run Sanic in debug mode')
    parser.add_argument('--secret_key',
                        help='The API secret key')
    parser.add_argument('--aes-key',
                        help='The AES key used for private key encryption')
    parser.add_argument('--batcher-private-key',
                        help='The sawtooth key used for transaction signing')
    parser.add_argument('--batcher-private-key-file-name-clinic',
                        help='The sawtooth key used for batch signing having clinic role')
    parser.add_argument('--batcher-private-key-file-name-doctor',
                        help='The sawtooth key used for batch signing having doctor role')
    parser.add_argument('--batcher-private-key-file-name-patient',
                        help='The sawtooth key used for batch signing having patient role')
    parser.add_argument('--batcher-private-key-file-name-lab',
                        help='The sawtooth key used for batch signing having lab role')
    parser.add_argument('--batcher-private-key-file-name-insurance',
                        help='The sawtooth key used for batch signing having insurance role')

    return parser.parse_args(args)


def load_config(appl):  # pylint: disable=too-many-branches
    appl.config.update(DEFAULT_CONFIG)
    config_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        'config.py')
    try:
        appl.config.from_pyfile(config_file_path)
    except FileNotFoundError:
        LOGGER.warning("No config file provided")

    # CLI Options will override config file options
    opts = parse_args(sys.argv[1:])

    if opts.host is not None:
        appl.config.HOST = opts.host
    if opts.port is not None:
        appl.config.PORT = opts.port
    if opts.timeout is not None:
        appl.config.TIMEOUT = opts.timeout

    if opts.validator is not None:
        appl.config.VALIDATOR_URL = opts.validator
    # if opts.db_host is not None:
    #     app.config.DB_HOST = opts.db_host
    # if opts.db_port is not None:
    #     app.config.DB_PORT = opts.db_port
    # if opts.db_name is not None:
    #     app.config.DB_NAME = opts.db_name

    if opts.debug is not None:
        appl.config.DEBUG = opts.debug

    if opts.secret_key is not None:
        appl.config.SECRET_KEY = opts.secret_key
    if appl.config.SECRET_KEY is None:
        LOGGER.exception("API secret key was not provided")
        sys.exit(1)

    if opts.aes_key is not None:
        appl.config.AES_KEY = opts.aes_key
    if appl.config.AES_KEY is None:
        LOGGER.exception("AES key was not provided")
        sys.exit(1)

    if opts.batcher_private_key is not None:
        appl.config.BATCHER_PRIVATE_KEY = opts.batcher_private_key
    if appl.config.BATCHER_PRIVATE_KEY is None:
        LOGGER.exception("Batcher private key was not provided")
        sys.exit(1)

    if opts.batcher_private_key_file_name_clinic is not None:
        appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_CLINIC = opts.batcher_private_key_file_name_clinic
    if opts.batcher_private_key_file_name_doctor is not None:
        appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_DOCTOR = opts.batcher_private_key_file_name_doctor
    if opts.batcher_private_key_file_name_patient is not None:
        appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_PATIENT = opts.batcher_private_key_file_name_patient
    if opts.batcher_private_key_file_name_lab is not None:
        appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_LAB = opts.batcher_private_key_file_name_lab
    if opts.batcher_private_key_file_name_insurance is not None:
        appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_INSURANCE = opts.batcher_private_key_file_name_insurance

    if appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_CLINIC is None:
        LOGGER.exception("Batcher private key file name for Clinic entity was not provided")
        sys.exit(1)
    if appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_DOCTOR is None:
        LOGGER.exception("Batcher private key file name for Doctor entity was not provided")
        sys.exit(1)
    if appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_PATIENT is None:
        LOGGER.exception("Batcher private key file name for Patient entity was not provided")
        sys.exit(1)
    if appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_LAB is None:
        LOGGER.exception("Batcher private key file name for Lab entity was not provided")
        sys.exit(1)
    if appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_INSURANCE is None:
        LOGGER.exception("Batcher private key file name for Insurance entity was not provided")
        sys.exit(1)

    try:
        private_key_file_name_clinic = get_keyfile(appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_CLINIC)
        clinic_private_key = get_signer_from_file(private_key_file_name_clinic)
        private_key_file_name_doctor = get_keyfile(appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_DOCTOR)
        doctor_private_key = get_signer_from_file(private_key_file_name_doctor)
        private_key_file_name_patient = get_keyfile(appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_PATIENT)
        patient_private_key = get_signer_from_file(private_key_file_name_patient)
        private_key_file_name_lab = get_keyfile(appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_LAB)
        lab_private_key = get_signer_from_file(private_key_file_name_lab)
        private_key_file_name_insurance = get_keyfile(appl.config.BATCHER_PRIVATE_KEY_FILE_NAME_INSURANCE)
        insurance_private_key = get_signer_from_file(private_key_file_name_insurance)

        # private_key = Secp256k1PrivateKey.from_hex(
        #     app.config.BATCHER_PRIVATE_KEY)
    except ParseError as err:
        LOGGER.exception('Unable to load private key: %s', str(err))
        sys.exit(1)
    appl.config.CONTEXT = create_context('secp256k1')
    appl.config.SIGNER_CLINIC = CryptoFactory(
        appl.config.CONTEXT).new_signer(clinic_private_key)
    appl.config.SIGNER_DOCTOR = CryptoFactory(
        appl.config.CONTEXT).new_signer(doctor_private_key)
    appl.config.SIGNER_PATIENT = CryptoFactory(
        appl.config.CONTEXT).new_signer(patient_private_key)
    appl.config.SIGNER_LAB = CryptoFactory(
        appl.config.CONTEXT).new_signer(lab_private_key)
    appl.config.SIGNER_INSURANCE = CryptoFactory(
        appl.config.CONTEXT).new_signer(insurance_private_key)


app = Sanic(__name__)
app.config['CORS_AUTOMATIC_OPTIONS'] = True


def main():
    LOGGER.info('Starting Clinic Rest API server...')
    # CORS(app)

    app.blueprint(CLINICS_BP)
    app.blueprint(DOCTORS_BP)
    app.blueprint(PATIENTS_BP)
    app.blueprint(CLAIMS_BP)
    app.blueprint(CLAIM_DETAILS_BP)
    app.blueprint(LAB_TESTS_BP)
    app.blueprint(PULSE_BP)
    app.blueprint(CLIENTS_BP)
    app.blueprint(LABS_BP)
    app.blueprint(INSURANCES_BP)
    # app.blueprint(OFFERS_BP)

    load_config(app)
    zmq = ZMQEventLoop()
    asyncio.set_event_loop(zmq)
    server = app.create_server(
        host=app.config.HOST, port=app.config.PORT, debug=app.config.DEBUG, return_asyncio_server=True)
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(open_connections(app))
    asyncio.ensure_future(server)
    signal(SIGINT, lambda s, f: loop.close())
    try:
        LOGGER.info('Clinic Rest API server starting')
        loop.run_forever()
    except KeyboardInterrupt:
        LOGGER.info('Clinic Rest API started interrupted')
        close_connections(app)
        loop.stop()


if __name__ == "__main__":
    main()
