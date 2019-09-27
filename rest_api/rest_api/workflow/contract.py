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

from rest_api.insurance_common import transaction
from rest_api.workflow import general, security_messaging
from rest_api.workflow.errors import ApiBadRequest, ApiInternalError

CONTRACT_BP = Blueprint('contract')

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


@CONTRACT_BP.get('contract')
async def get_all_contacts(request):
    """Fetches complete details of all Accounts in state"""
    LOGGER.debug("Call 'contract' request")
    client_key = general.get_request_key_header(request)
    contract_list = await security_messaging.get_contracts(request.app.config.VAL_CONN, client_key)
    contract_list_json = []
    for address, con in contract_list.items():
        contract_list_json.append({
            'client_pkey': con.client_pkey,
            'id': con.id,
            'name': con.name,
            'surname': con.surname
        })

    return response.json(body={'data': contract_list_json},
                         headers=general.get_response_headers())


@CONTRACT_BP.post('contract')
async def add_new_contract(request):
    """Updates auth information for the authorized account"""
    client_key = general.get_request_key_header(request)
    required_fields = ['id', 'client_pkey']
    general.validate_fields(required_fields, request.json)

    uid = request.json.get('id')
    contractor_pkey = request.json.get('client_pkey')

    client_signer = general.get_signer(request, client_key)

    batch, batch_id = transaction.add_contract(
        txn_signer=client_signer,
        batch_signer=client_signer,
        uid=uid,
        client_pkey=contractor_pkey
    )

    await security_messaging.add_contract(
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
