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
from rest_api.workflow import general, security_messaging
from rest_api.workflow.errors import ApiBadRequest, ApiInternalError

CLINICS_BP = Blueprint('clinics')


@CLINICS_BP.get('clinics')
async def get_all_clinics(request):
    """Fetches complete details of all Accounts in state"""
    client_key = general.get_request_key_header(request)
    list_clinic_address = helper.make_clinic_list_address()
    account_resources = await security_messaging.get_clinics(request.app.config.VAL_CONN,
                                                             list_clinic_address, client_key)
    # account_resources2 = MessageToJson(account_resources)
    # account_resources3 = MessageToDict(account_resources)
    clinics = []
    for entity in account_resources.entries:
        # dec_cl = base64.b64decode(entity.data)
        cl = payload_pb2.CreateClinic()
        cl.ParseFromString(entity.data)
        permissions = []
        for perm in cl.permissions:
            permissions.append(perm)
        clinics.append({'name': cl.name, 'permissions': str(permissions)})

    # import json
    # result = json.dumps(clinics)
    # clinics_json = MessageToJson(account_resources)
    return response.json(body={'data': clinics},
                         headers=general.get_response_headers(general.get_request_origin(request)))
    # return response.text(body={'data': clinics})  # , dumps=pd.json.dumps)


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

    batch, batch_id = transaction.create_clinic(
        txn_signer=clinic_signer,
        batch_signer=clinic_signer,
        name=name)

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
                         headers=general.get_response_headers(general.get_request_origin(request)))

