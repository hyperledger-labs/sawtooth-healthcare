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
# import base64
#
# import bcrypt
#
# from itsdangerous import BadSignature
from sanic import Blueprint
from sanic import response

# from sawtooth_signing import CryptoFactory

# from rest_api.workflow.authorization import authorized
from rest_api.common.protobuf import payload_pb2
from rest_api.common import helper, transaction
from rest_api.consent_common import transaction as consent_transaction
from rest_api.workflow import general, security_messaging
from rest_api.workflow.errors import ApiBadRequest, ApiInternalError

DOCTORS_BP = Blueprint('doctors')


@DOCTORS_BP.get('doctors')
async def get_all_doctors(request):
    """Fetches complete details of all Accounts in state"""
    client_key = general.get_request_key_header(request)
    # list_doctors_address = helper.make_doctor_list_address()
    doctor_resources = await security_messaging.get_doctors(request.app.config.VAL_CONN, client_key)
    # account_resources2 = MessageToJson(account_resources)
    # account_resources3 = MessageToDict(account_resources)
    doctors = []
    for entity in doctor_resources.entries:
        # dec_cl = base64.b64decode(entity.data)
        doc = payload_pb2.CreateDoctor()
        doc.ParseFromString(entity.data)
        # permissions = []
        # for perm in doc.permissions:
        #     permissions.append(perm)
        # doctors.append({'name': doc.name, 'surname': doc.surname, 'permissions': str(permissions)})
        doctors.append({'name': doc.name, 'surname': doc.surname})

    # import json
    # result = json.dumps(clinics)
    # clinics_json = MessageToJson(account_resources)
    return response.json(body={'data': doctors},
                         headers=general.get_response_headers(general.get_request_origin(request)))


@DOCTORS_BP.post('doctors')
async def register_new_doctor(request):
    """Updates auth information for the authorized account"""
    # keyfile = common.get_keyfile(request.json.get['signer'])
    required_fields = ['name', 'surname']
    general.validate_fields(required_fields, request.json)

    name = request.json.get('name')
    surname = request.json.get('surname')

    # private_key = common.get_signer_from_file(keyfile)
    # signer = CryptoFactory(request.app.config.CONTEXT).new_signer(private_key)
    doctor_signer = request.app.config.SIGNER_DOCTOR  # .get_public_key().as_hex()

    client_txn = consent_transaction.create_doctor_client(
        txn_signer=doctor_signer,
        batch_signer=doctor_signer
    )

    doctor_txn = transaction.create_doctor(
        txn_signer=doctor_signer,
        batch_signer=doctor_signer,
        name=name,
        surname=surname)

    batch, batch_id = transaction.make_batch_and_id([client_txn, doctor_txn], doctor_signer)

    # await messaging.send(
    #     request.app.config.VAL_CONN,
    #     request.app.config.TIMEOUT,
    #     [batch])
    await security_messaging.add_doctor(
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

# @ACCOUNTS_BP.get('accounts/<key>')
# async def get_account(request, key):
#     """Fetches the details of particular Account in state"""
#     try:
#         auth_key = common.deserialize_auth_token(
#             request.app.config.SECRET_KEY,
#             request.token).get('public_key')
#     except (BadSignature, TypeError):
#         auth_key = None
#     account_resource = await accounts_query.fetch_account_resource(
#         request.app.config.DB_CONN, key, auth_key)
#     return response.json(account_resource)
#

# @ACCOUNTS_BP.patch('accounts')
# @authorized()
# async def update_account_info(request):
#     """Updates auth information for the authorized account"""
#     token = common.deserialize_auth_token(
#         request.app.config.SECRET_KEY, request.token)
#
#     update = {}
#     if request.json.get('password'):
#         update['hashed_password'] = bcrypt.hashpw(
#             bytes(request.json.get('password'), 'utf-8'), bcrypt.gensalt())
#     if request.json.get('email'):
#         update['email'] = request.json.get('email')
#
#     if update:
#         updated_auth_info = await auth_query.update_auth_info(
#             request.app.config.DB_CONN,
#             token.get('email'),
#             token.get('public_key'),
#             update)
#         new_token = common.generate_auth_token(
#             request.app.config.SECRET_KEY,
#             updated_auth_info.get('email'),
#             updated_auth_info.get('publicKey'))
#     else:
#         updated_auth_info = await accounts_query.fetch_account_resource(
#             request.app.config.DB_CONN,
#             token.get('public_key'),
#             token.get('public_key'))
#         new_token = request.token
#
#     return response.json(
#         {
#             'authorization': new_token,
#             'account': updated_auth_info
#         })

#
# def _create_account_dict(body, public_key):
#     keys = ['label', 'description', 'email']
#
#     account = {k: body[k] for k in keys if body.get(k) is not None}
#
#     account['publicKey'] = public_key
#     account['holdings'] = []
#
#     return account


# def _create_auth_dict(request, public_key, private_key):
#     auth_entry = {
#         'public_key': public_key,
#         'email': request.json['email']
#     }
#
#     auth_entry['encrypted_private_key'] = common.encrypt_private_key(
#         request.app.config.AES_KEY, public_key, private_key)
#     auth_entry['hashed_password'] = bcrypt.hashpw(
#         bytes(request.json.get('password'), 'utf-8'), bcrypt.gensalt())
#
# return auth_entry
