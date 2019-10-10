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
import logging

from sanic import Blueprint
from sanic import response

from rest_api.payment_common import helper, transaction
from rest_api.workflow import general, security_messaging
from rest_api.workflow.errors import ApiBadRequest, ApiInternalError

PAYMENT_BP = Blueprint('payment')

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


@PAYMENT_BP.get('payment')
async def get_all_payments(request):
    """Fetches complete details of all Accounts in state"""
    LOGGER.debug("Call 'payment' request")
    client_key = general.get_request_key_header(request)
    payment_list = await security_messaging.get_payments(request.app.config.VAL_CONN, client_key)
    payment_list_json = []
    for address, pay in payment_list.items():
        payment_list_json.append({
            'patient_pkey': pay.patient_pkey,
            'contract_id': pay.contract_id,
            'claim_id': pay.claim_id,
            'id': pay.id,
            'timestamp': pay.timestamp
        })

    return response.json(body={'data': payment_list_json},
                         headers=general.get_response_headers())


@PAYMENT_BP.post('payment')
async def add_new_payment(request):
    """Updates auth information for the authorized account"""
    # keyfile = common.get_keyfile(request.json.get['signer'])
    client_key = general.get_request_key_header(request)
    required_fields = ['patient_pkey', 'contract_id', 'claim_id']
    general.validate_fields(required_fields, request.json)

    # uid = request.json.get('id')
    patient_pkey = request.json.get('patient_pkey')
    contract_id = request.json.get('contract_id')
    claim_id = request.json.get('claim_id')

    client_signer = general.get_signer(request, client_key)
    payment_id = str(helper.get_current_timestamp())

    batch, batch_id = transaction.create_payment(
        txn_signer=client_signer,
        batch_signer=client_signer,
        payment_id=payment_id,
        patient_pkey=patient_pkey,
        contract_id=contract_id,
        claim_id=claim_id
    )

    await security_messaging.create_payment(
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
                         headers=general.get_response_headers())
