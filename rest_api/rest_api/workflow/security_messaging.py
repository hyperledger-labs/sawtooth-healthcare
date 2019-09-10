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

# from sawtooth_sdk.protobuf import client_batch_submit_pb2
import logging

from sawtooth_rest_api.protobuf import client_state_pb2
from sawtooth_rest_api.protobuf import validator_pb2

# from rest_api.common import helper
from rest_api.consent_common import helper as consent_helper
# from rest_api.consent_common.protobuf import consent_payload_pb2
# from rest_api.common.protobuf import payload_pb2
from rest_api.consent_common.protobuf.consent_payload_pb2 import Client, Permission
from rest_api.workflow import messaging
# from rest_api.workflow.errors import ApiBadRequest
# from rest_api.workflow.errors import ApiInternalError
from rest_api.workflow.errors import ApiForbidden

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


async def _send(conn, timeout, batches):
    await messaging.send(conn, timeout, batches)


async def check_batch_status(conn, batch_ids):
    await messaging.check_batch_status(conn, batch_ids)


async def get_state_by_address(conn, address_suffix):
    status_request = client_state_pb2.ClientStateListRequest(address=address_suffix)
    validator_response = await conn.send(
        validator_pb2.Message.CLIENT_STATE_LIST_REQUEST,
        status_request.SerializeToString())

    status_response = client_state_pb2.ClientStateListResponse()
    status_response.ParseFromString(validator_response.content)
    # resp = status_response

    return status_response  # resp.entries

    # batch_status = status_response.batch_statuses[0].status
    # if batch_status == client_batch_submit_pb2.ClientBatchStatus.INVALID:
    #     invalid = status_response.batch_statuses[0].invalid_transactions[0]
    #     raise ApiBadRequest(invalid.message)
    # elif batch_status == client_batch_submit_pb2.ClientBatchStatus.PENDING:
    #     raise ApiInternalError("Transaction submitted but timed out")
    # elif batch_status == client_batch_submit_pb2.ClientBatchStatus.UNKNOWN:
    #     raise ApiInternalError("Something went wrong. Try again later")


async def add_clinic(conn, timeout, batches):
    await _send(conn, timeout, batches)


async def get_clinics(conn, address_suffix, client_key):
    client_address = consent_helper.make_client_address(client_key)
    LOGGER.debug('client_address: ' + str(client_address))
    client_resources = await messaging.get_state_by_address(conn, client_address)
    LOGGER.debug('client_resources: ' + str(client_resources))
    for entity in client_resources.entries:
        cl = Client()
        cl.ParseFromString(entity.data)
        LOGGER.debug('client: ' + str(cl))
        if Permission(type=Permission.READ_CLINIC) in cl.permissions:
            return await messaging.get_state_by_address(conn, address_suffix)
    raise ApiForbidden("Insufficient permission")


async def add_doctor(conn, timeout, batches):
    await _send(conn, timeout, batches)


async def get_doctors(conn, address_suffix, client_key):
    client_address = consent_helper.make_client_address(client_key)
    LOGGER.debug('client_address: ' + str(client_address))
    client_resources = await messaging.get_state_by_address(conn, client_address)
    LOGGER.debug('client_resources: ' + str(client_resources))
    for entity in client_resources.entries:
        doc = Client()
        doc.ParseFromString(entity.data)
        LOGGER.debug('client: ' + str(doc))
        if Permission(type=Permission.READ_DOCTOR) in doc.permissions:
            return await messaging.get_state_by_address(conn, address_suffix)
    raise ApiForbidden("Insufficient permission")


async def add_patient(conn, timeout, batches):
    await _send(conn, timeout, batches)


async def get_patients(conn, address_suffix, client_key):
    client_address = consent_helper.make_client_address(client_key)
    LOGGER.debug('client_address: ' + str(client_address))
    client_resources = await messaging.get_state_by_address(conn, client_address)
    LOGGER.debug('client_resources: ' + str(client_resources))
    for entity in client_resources.entries:
        pat = Client()
        pat.ParseFromString(entity.data)
        LOGGER.debug('client: ' + str(pat))
        if Permission(type=Permission.READ_PATIENT) in pat.permissions:
            return await messaging.get_state_by_address(conn, address_suffix)
    raise ApiForbidden("Insufficient permission")
