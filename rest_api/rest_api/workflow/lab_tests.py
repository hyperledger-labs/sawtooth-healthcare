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
import time

from sanic import Blueprint
from sanic import response

# from sawtooth_signing import CryptoFactory

# from rest_api.workflow.authorization import authorized
from rest_api.common.protobuf import payload_pb2
from rest_api.common import helper, transaction
from rest_api.workflow import general, security_messaging
from rest_api.workflow.errors import ApiBadRequest, ApiInternalError

# from rest_api.workflow.errors import ApiBadRequest
# from rest_api.workflow.errors import ApiInternalError
# from db import accounts_query
# from db import auth_query
# import pandas as pd
# from google.protobuf.json_format import MessageToJson
# from google.protobuf.json_format import MessageToDict

# from marketplace_transaction import transaction_creation


LAB_TESTS_BP = Blueprint('labtests')


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


@LAB_TESTS_BP.get('labtests')
async def get_all_lab_tests(request):
    """Fetches complete details of all Accounts in state"""
    client_key = general.get_request_key_header(request)
    # lab_tests_address = helper.make_lab_test_list_address()
    # lab_test_resources = await messaging.get_state_by_address(request.app.config.VAL_CONN, lab_tests_address)
    lab_test_resources = await security_messaging.get_lab_tests(request.app.config.VAL_CONN, client_key)
    # account_resources2 = MessageToJson(account_resources)
    # account_resources3 = MessageToDict(account_resources)
    lab_tests = []
    for entity in lab_test_resources.entries:
        # dec_cl = base64.b64decode(entity.data)
        lt = payload_pb2.AddLabTest()
        lt.ParseFromString(entity.data)
        lab_tests.append({
            'height': lt.height,
            'weight': lt.weight,
            'gender': lt.gender,
            'a_g_ratio': lt.a_g_ratio,
            'albumin': lt.albumin,
            'alkaline_phosphatase': lt.alkaline_phosphatase,
            'appearance': lt.appearance,
            'bilirubin': lt.bilirubin,
            'casts': lt.casts,
            'color': lt.color
        })

    # import json
    # result = json.dumps(clinics)
    # clinics_json = MessageToJson(account_resources)
    return response.json(body={'data': lab_tests},
                         headers=general.get_response_headers(general.get_request_origin(request)))


@LAB_TESTS_BP.post('labtests')
async def add_new_lab_test(request):
    """Updates auth information for the authorized account"""
    # keyfile = common.get_keyfile(request.json.get['signer'])
    client_key = general.get_request_key_header(request)
    required_fields = ['height', 'weight', 'gender', 'a_g_ratio', 'albumin', 'alkaline_phosphatase',
                       'appearance', 'bilirubin', 'casts', 'color']
    general.validate_fields(required_fields, request.json)

    height = request.json.get('height')
    weight = request.json.get('weight')
    gender = request.json.get('gender')
    a_g_ratio = request.json.get('a_g_ratio')
    albumin = request.json.get('albumin')
    alkaline_phosphatase = request.json.get('alkaline_phosphatase')
    appearance = request.json.get('appearance')
    bilirubin = request.json.get('bilirubin')
    casts = request.json.get('casts')
    color = request.json.get('color')

    # private_key = common.get_signer_from_file(keyfile)
    # signer = CryptoFactory(request.app.config.CONTEXT).new_signer(private_key)
    # client_signer = request.app.config.SIGNER  # .get_public_key().as_hex()
    if request.app.config.SIGNER_CLINIC.get_public_key().as_hex() == client_key:
        client_signer = request.app.config.SIGNER_CLINIC
    elif request.app.config.SIGNER_PATIENT.get_public_key().as_hex() == client_key:
        client_signer = request.app.config.SIGNER_PATIENT
    elif request.app.config.SIGNER_DOCTOR.get_public_key().as_hex() == client_key:
        client_signer = request.app.config.SIGNER_DOCTOR
    elif request.app.config.SIGNER_LAB.get_public_key().as_hex() == client_key:
        client_signer = request.app.config.SIGNER_LAB
    else:
        client_signer = request.app.config.SIGNER_PATIENT

    current_times_str = str(time.time())

    lab_test_txn = transaction.add_lab_test(
        txn_signer=client_signer,
        batch_signer=client_signer,
        height=height,
        weight=weight,
        gender=gender,
        a_g_ratio=a_g_ratio,
        albumin=albumin,
        alkaline_phosphatase=alkaline_phosphatase,
        appearance=appearance,
        bilirubin=bilirubin,
        casts=casts,
        color=color,
        id=current_times_str,
        client_pkey=client_key
    )

    batch, batch_id = transaction.make_batch_and_id([lab_test_txn], client_signer)

    await security_messaging.add_lab_test(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], client_key)

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers(general.get_request_origin(request)))
