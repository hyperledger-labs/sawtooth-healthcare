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
# from rest_api.consent_common import helper as consent_helper
from rest_api.consent_common import transaction as consent_transaction
from rest_api.workflow import general, security_messaging
from rest_api.workflow.errors import ApiBadRequest, ApiInternalError

LABS_BP = Blueprint('labs')


@LABS_BP.get('labs')
async def get_all_labs(request):
    """Fetches complete details of all Accounts in state"""
    client_key = general.get_request_key_header(request)
    list_lab_address = helper.make_lab_list_address()
    lab_resources = await security_messaging.get_labs(request.app.config.VAL_CONN,
                                                      list_lab_address, client_key)
    # account_resources2 = MessageToJson(account_resources)
    # account_resources3 = MessageToDict(account_resources)
    labs = []
    for entity in lab_resources.entries:
        # dec_cl = base64.b64decode(entity.data)
        lab = payload_pb2.CreateLab()
        lab.ParseFromString(entity.data)
        # permissions = []
        # for perm in cl.permissions:
        #     permissions.append(perm)
        labs.append({'name': lab.name})

    # import json
    # result = json.dumps(clinics)
    # clinics_json = MessageToJson(account_resources)
    return response.json(body={'data': labs},
                         headers=general.get_response_headers(general.get_request_origin(request)))
    # return response.text(body={'data': clinics})  # , dumps=pd.json.dumps)


@LABS_BP.post('labs')
async def register_new_lab(request):
    """Updates auth information for the authorized account"""
    # keyfile = common.get_keyfile(request.json.get['signer'])
    # client_key = general.get_request_key_header(request)
    required_fields = ['name']
    general.validate_fields(required_fields, request.json)

    name = request.json.get('name')

    # private_key = common.get_signer_from_file(keyfile)
    # signer = CryptoFactory(request.app.config.CONTEXT).new_signer(private_key)
    lab_signer = request.app.config.SIGNER_LAB  # .get_public_key().as_hex()

    client_txn = consent_transaction.create_lab_client(
        txn_signer=lab_signer,
        batch_signer=lab_signer
    )
    lab_txn = transaction.create_lab(
        txn_signer=lab_signer,
        batch_signer=lab_signer,
        name=name
    )
    batch, batch_id = transaction.make_batch_and_id([client_txn, lab_txn], lab_signer)
    # batch, batch_id = transaction.create_clinic(
    #     txn_signer=clinic_signer,
    #     batch_signer=clinic_signer,
    #     name=name)

    await security_messaging.add_lab(
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
                         headers=general.get_response_headers(general.get_request_origin(request)))
