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
from sanic import Blueprint
from sanic import response

from rest_api.common.protobuf import payload_pb2
from rest_api.common import helper, transaction
from rest_api.consent_common import helper as consent_helper
from rest_api.consent_common import transaction as consent_transaction
from rest_api.consent_common.exceptions import ConsentException
from rest_api.workflow import general, messaging
from rest_api.workflow.errors import ApiBadRequest, ApiInternalError

PULSE_BP = Blueprint('pulse')


@PULSE_BP.get('pulse')
async def get_all_pulse_items(request):
    """Fetches complete details of all Accounts in state"""
    pulse_list_address = helper.make_pulse_list_address()
    pulse_resources = await messaging.get_state_by_address(request.app.config.VAL_CONN, pulse_list_address)
    # account_resources2 = MessageToJson(account_resources)
    # account_resources3 = MessageToDict(account_resources)
    pulse_list = []
    for entity in pulse_resources.entries:
        # dec_cl = base64.b64decode(entity.data)
        pl = payload_pb2.AddPulse()
        pl.ParseFromString(entity.data)
        pulse_list.append({
            'public_key': pl.public_key,
            'pulse': pl.pulse,
            'timestamp': pl.timestamp
        })

    return response.json(body={'data': pulse_list},
                         headers=general.get_response_headers(general.get_request_origin(request)))


@PULSE_BP.get('pulse/<patient_pkey>')
async def get_own_pulse_items(request, patient_pkey):
    """Fetches complete details of all Accounts in state"""
    # required_fields = ['patient_pkey']
    # general.validate_input_params(required_fields, request.args)
    # patient_pkey = request.args.get('patient_pkey')

    pulse_list_address = helper.make_pulse_list_by_patient_address(patient_pkey=patient_pkey)
    pulse_resources = await messaging.get_state_by_address(request.app.config.VAL_CONN, pulse_list_address)
    pulse_list = []
    for entity in pulse_resources.entries:
        # dec_cl = base64.b64decode(entity.data)
        pl = payload_pb2.AddPulse()
        pl.ParseFromString(entity.data)
        pulse_list.append({
            'public_key': pl.public_key,
            'pulse': pl.pulse,
            'timestamp': pl.timestamp
        })

    return response.json(body={'data': pulse_list},
                         headers=general.get_response_headers(general.get_request_origin(request)))


@PULSE_BP.get('pulse/<patient_pkey>/<doctor_pkey>')
async def get_pulse_items_by_consent(request, patient_pkey, doctor_pkey):
    """Fetches complete details of all Accounts in state"""
    # required_fields = ['doctor_pkey', 'patient_pkey']
    # general.validate_input_params(required_fields, request.args)
    # doctor_pkey = request.args.get('doctor_pkey')
    # patient_pkey = request.args.get('patient_pkey')
    access_address = consent_helper.make_consent_address(doctor_pkey=doctor_pkey, patient_pkey=patient_pkey)
    access_state = await messaging.get_state_by_address(request.app.config.VAL_CONN, access_address)
    if len(access_state.entries) == 0:
        raise ApiInternalError("No consent to retrieve such data")

    pulse_list_address = helper.make_pulse_list_by_patient_address(patient_pkey=patient_pkey)
    pulse_resources = await messaging.get_state_by_address(request.app.config.VAL_CONN, pulse_list_address)
    pulse_list = []
    for entity in pulse_resources.entries:
        # dec_cl = base64.b64decode(entity.data)
        pl = payload_pb2.AddPulse()
        pl.ParseFromString(entity.data)
        pulse_list.append({
            'public_key': pl.public_key,
            'pulse': pl.pulse,
            'timestamp': pl.timestamp
        })

    return response.json(body={'data': pulse_list},
                         headers=general.get_response_headers(general.get_request_origin(request)))


@PULSE_BP.post('pulse')
async def add_new_pulse(request):
    """Updates auth information for the authorized account"""
    # keyfile = common.get_keyfile(request.json.get['signer'])
    required_fields = ['pulse', 'timestamp']
    general.validate_fields(required_fields, request.json)

    pulse = request.json.get('pulse')
    timestamp = request.json.get('timestamp')

    # private_key = common.get_signer_from_file(keyfile)
    # signer = CryptoFactory(request.app.config.CONTEXT).new_signer(private_key)
    patient_signer = request.app.config.SIGNER  # .get_public_key().as_hex()

    batch, batch_id = transaction.add_pulse(
        txn_signer=patient_signer,
        batch_signer=patient_signer,
        pulse=pulse,
        timestamp=timestamp)

    await messaging.send(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch])

    try:
        await messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers(general.get_request_origin(request)))

