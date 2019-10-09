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
from rest_api.common import transaction
from rest_api.payment_common import transaction as payment_transaction
from rest_api.payment_common import helper
from rest_api.workflow import general, security_messaging
from rest_api.workflow.errors import ApiBadRequest
from rest_api.workflow.errors import ApiInternalError

CLAIMS_BP = Blueprint('claims')


@CLAIMS_BP.get('claims')
async def get_all_claims(request):
    client_key = general.get_request_key_header(request)
    claim_list = await security_messaging.get_claims(request.app.config.VAL_CONN, client_key)

    claim_list_json = []
    for address, cl in claim_list.items():
        claim_list_json.append({
            'client_pkey': cl.client_pkey,
            'id': cl.id,
            'description': cl.description,
            'provided_service': cl.provided_service,
            'state': cl.state,
            'contract_id': cl.contract_id,
            'name': cl.name,
            'surname': cl.surname
        })

    return response.json(body={'data': claim_list_json},
                         headers=general.get_response_headers())


@CLAIMS_BP.post('claims')
async def register_new_claim(request):
    """Updates auth information for the authorized account"""
    # keyfile = common.get_keyfile(request.json.get['signer'])
    clinic_pkey = general.get_request_key_header(request)
    required_fields = ['patient_pkey', 'claim_id', 'description']
    general.validate_fields(required_fields, request.json)

    patient_pkey = request.json.get('patient_pkey')
    claim_id = request.json.get('claim_id')
    description = request.json.get('description')
    contract_id = request.json.get('contract_id')

    if contract_id is not None and contract_id != '':
        is_valid = await security_messaging.valid_contracts(request.app.config.VAL_CONN, patient_pkey, contract_id)
        if not is_valid:
            return response.text(body="Contract having '" + contract_id + "' id is not valid",
                                 status=ApiBadRequest.status_code,
                                 headers=general.get_response_headers())

    client_signer = general.get_signer(request, clinic_pkey)

    claim_txn = transaction.add_claim(
        txn_signer=client_signer,
        batch_signer=client_signer,
        uid=claim_id,
        description=description,
        client_pkey=patient_pkey,
        contract_id=contract_id
    )

    batch, batch_id = transaction.make_batch_and_id([claim_txn], client_signer)

    await security_messaging.add_claim(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], clinic_pkey, patient_pkey)

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())


@CLAIMS_BP.post('claims/close')
async def close_claim(request):
    """Updates auth information for the authorized account"""
    # keyfile = common.get_keyfile(request.json.get['signer'])
    clinic_pkey = general.get_request_key_header(request)
    required_fields = ['claim_id', 'provided_service', 'client_pkey', 'provided_service']
    general.validate_fields(required_fields, request.json)

    claim_id = request.json.get('claim_id')
    provided_service = request.json.get('provided_service')
    patient_pkey = request.json.get('client_pkey')
    contract_id = request.json.get('contract_id')

    client_signer = general.get_signer(request, clinic_pkey)

    close_claim_txn = transaction.close_claim(
        txn_signer=client_signer,
        batch_signer=client_signer,
        uid=claim_id,
        patient_pkey=patient_pkey,
        provided_service=provided_service)

    create_payment_txn = payment_transaction.create_payment(
        txn_signer=client_signer,
        batch_signer=client_signer,
        payment_id=str(helper.get_current_timestamp()),
        patient_pkey=patient_pkey,
        contract_id=contract_id,
        claim_id=claim_id
    )

    batch, batch_id = transaction.make_batch_and_id([close_claim_txn, create_payment_txn], client_signer)

    await security_messaging.close_claim(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], clinic_pkey, patient_pkey)

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())
