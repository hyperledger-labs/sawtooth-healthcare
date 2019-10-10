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
from rest_api.consent_common import transaction as consent_transaction
from rest_api.workflow import general, security_messaging
from rest_api.workflow.errors import ApiBadRequest, ApiInternalError

CLINICS_BP = Blueprint('clinics')


@CLINICS_BP.get('clinics')
async def get_all_clinics(request):
    """Fetches complete details of all Accounts in state"""
    client_key = general.get_request_key_header(request)
    clinic_list = await security_messaging.get_clinics(request.app.config.VAL_CONN, client_key)

    clinic_list_json = []
    for address, cl in clinic_list.items():
        clinic_list_json.append({
            'public_key': cl.public_key,
            'name': cl.name
        })
    return response.json(body={'data': clinic_list_json},
                         headers=general.get_response_headers())


@CLINICS_BP.post('clinics')
async def register_new_clinic(request):
    """Updates auth information for the authorized account"""
    # keyfile = common.get_keyfile(request.json.get['signer'])
    # client_key = general.get_request_key_header(request)
    required_fields = ['name']
    general.validate_fields(required_fields, request.json)

    name = request.json.get('name')

    # private_key = common.get_signer_from_file(keyfile)
    # signer = CryptoFactory(request.app.config.CONTEXT).new_signer(private_key)
    clinic_signer = request.app.config.SIGNER_CLINIC  # .get_public_key().as_hex()

    client_txn = consent_transaction.create_clinic_client(
        txn_signer=clinic_signer,
        batch_signer=clinic_signer
    )
    clinic_txn = transaction.create_clinic(
        txn_signer=clinic_signer,
        batch_signer=clinic_signer,
        name=name
    )
    batch, batch_id = transaction.make_batch_and_id([client_txn, clinic_txn], clinic_signer)
    # batch, batch_id = transaction.create_clinic(
    #     txn_signer=clinic_signer,
    #     batch_signer=clinic_signer,
    #     name=name)

    await security_messaging.add_clinic(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch])

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())
