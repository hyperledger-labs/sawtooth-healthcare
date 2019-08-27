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
from rest_api.workflow import general, messaging
from rest_api.workflow.errors import ApiInternalError, ApiBadRequest

# from workflow.errors import ApiBadRequest
# from workflow.errors import ApiInternalError
# from db import accounts_query
# from db import auth_query
# import pandas as pd
# from google.protobuf.json_format import MessageToJson
# from google.protobuf.json_format import MessageToDict

# from marketplace_transaction import transaction_creation


PATIENTS_BP = Blueprint('patients')


# @CLINICS_BP.post('accounts')
# async def create_account(request):
#     """Creates a new Account and corresponding authorization token"""
#     required_fields = ['email', 'password']
#     common.validate_fields(required_fields, request.json)
#
#     private_key = request.app.config.CONTEXT.new_random_private_key()
#     signer = CryptoFactory(request.app.config.CONTEXT).new_signer(private_key)
#     public_key = signer.get_public_key().as_hex()
#
#     auth_entry = _create_auth_dict(
#         request, public_key, pr ivate_key.as_hex())
#     await auth_query.create_auth_entry(request.app.config.DB_CONN, auth_entry)
#
#     account = _create_account_dict(request.json, public_key)
#
#     batches, batch_id = transaction_creation.create_account(
#         txn_key=signer,
#         batch_key=request.app.config.SIGNER,
#         label=account.get('label'),
#         description=account.get('description'))
#
#     await messaging.send(
#         request.app.config.VAL_CONN,
#         request.app.config.TIMEOUT,
#         batches)
#
#     try:
#         await messaging.check_batch_status(
#             request.app.config.VAL_CONN, batch_id)
#     except (ApiBadRequest, ApiInternalError) as err:
#         await auth_query.remove_auth_entry(
#             request.app.config.DB_CONN, request.json.get('email'))
#         raise err
#
#     token = common.generate_auth_token(
#         request.app.config.SECRET_KEY,
#         account.get('email'),
#         public_key)
#
#     return response.json(
#         {
#             'authorization': token,
#             'account': account
#         })


@PATIENTS_BP.get('patients')
async def get_all_patients(request):
    """Fetches complete details of all Accounts in state"""
    list_patient_address = helper.make_patient_list_address()
    patient_resources = await messaging.get_state_by_address(request.app.config.VAL_CONN, list_patient_address)
    # account_resources2 = MessageToJson(account_resources)
    # account_resources3 = MessageToDict(account_resources)
    patients = []
    for entity in patient_resources.entries:
        # dec_cl = base64.b64decode(entity.data)
        pat = payload_pb2.CreatePatient()
        pat.ParseFromString(entity.data)
        patients.append({'public_key': pat.public_key, 'name': pat.name, 'surname': pat.surname})

    # import json
    # result = json.dumps(clinics)
    # clinics_json = MessageToJson(account_resources)
    return response.json(body={'data': patients},
                         headers=general.get_response_headers(general.get_request_origin(request)))


@PATIENTS_BP.post('patients')
async def register_new_patient(request):
    """Updates auth information for the authorized account"""
    # keyfile = common.get_keyfile(request.json.get['signer'])
    required_fields = ['name', 'surname']
    general.validate_fields(required_fields, request.json)

    name = request.json.get('name')
    surname = request.json.get('surname')

    # private_key = common.get_signer_from_file(keyfile)
    # signer = CryptoFactory(request.app.config.CONTEXT).new_signer(private_key)
    clinic_signer = request.app.config.SIGNER  # .get_public_key().as_hex()

    batch, batch_id = transaction.create_patient(
        txn_signer=clinic_signer,
        batch_signer=clinic_signer,
        name=name,
        surname=surname)

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
