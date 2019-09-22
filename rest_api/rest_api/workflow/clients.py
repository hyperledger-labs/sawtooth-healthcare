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

from rest_api.workflow import general

CLIENTS_BP = Blueprint('clients')


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


@CLIENTS_BP.get('clients')
async def get_all_clients(request):
    """Fetches complete details of all Accounts in state"""
    clinic_pkey = request.app.config.SIGNER_CLINIC.get_public_key().as_hex()
    doctor_pkey = request.app.config.SIGNER_DOCTOR.get_public_key().as_hex()
    patient_pkey = request.app.config.SIGNER_PATIENT.get_public_key().as_hex()
    lab_pkey = request.app.config.SIGNER_LAB.get_public_key().as_hex()
    clients = {'clinic': clinic_pkey, 'doctor': doctor_pkey, 'patient': patient_pkey, 'lab': lab_pkey}
    return response.json(body={'data': clients},
                         headers=general.get_response_headers(general.get_request_origin(request)))
    # return response.text(body={'data': clinics})  # , dumps=pd.json.dumps)
