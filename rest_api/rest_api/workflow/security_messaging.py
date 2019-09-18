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

from rest_api.common import helper
from rest_api.common.protobuf import payload_pb2
from rest_api.consent_common import helper as consent_helper
# from rest_api.consent_common.protobuf import consent_payload_pb2
# from rest_api.common.protobuf import payload_pb2
from rest_api.consent_common.protobuf.consent_payload_pb2 import Client, Permission
from rest_api.workflow import messaging
# from rest_api.workflow.errors import ApiBadRequest
# from rest_api.workflow.errors import ApiInternalError
from rest_api.workflow.errors import ApiForbidden, ApiUnauthorized

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


async def get_clinics(conn, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.READ_CLINIC) in client.permissions:
        list_clinic_address = helper.make_clinic_list_address()
        return await messaging.get_state_by_address(conn, list_clinic_address)
    # client_address = consent_helper.make_client_address(client_key)
    # LOGGER.debug('client_address: ' + str(client_address))
    # client_resources = await messaging.get_state_by_address(conn, client_address)
    # LOGGER.debug('client_resources: ' + str(client_resources))
    # for entity in client_resources.entries:
    #     cl = Client()
    #     cl.ParseFromString(entity.data)
    #     LOGGER.debug('client: ' + str(cl))
    #     if Permission(type=Permission.READ_CLINIC) in cl.permissions:
    #         return await messaging.get_state_by_address(conn, address_suffix)
    raise ApiForbidden("Insufficient permission")


async def add_doctor(conn, timeout, batches):
    await _send(conn, timeout, batches)


async def get_doctors(conn, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.READ_DOCTOR) in client.permissions:
        list_doctors_address = helper.make_doctor_list_address()
        return await messaging.get_state_by_address(conn, list_doctors_address)
    # client_address = consent_helper.make_client_address(client_key)
    # LOGGER.debug('client_address: ' + str(client_address))
    # client_resources = await messaging.get_state_by_address(conn, client_address)
    # LOGGER.debug('client_resources: ' + str(client_resources))
    # for entity in client_resources.entries:
    #     cl = Client()
    #     cl.ParseFromString(entity.data)
    #     LOGGER.debug('client: ' + str(cl))
    #     if Permission(type=Permission.READ_DOCTOR) in cl.permissions:
    #         return await messaging.get_state_by_address(conn, address_suffix)
    raise ApiForbidden("Insufficient permission")


async def add_patient(conn, timeout, batches):
    await _send(conn, timeout, batches)


async def get_patients(conn, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.READ_PATIENT) in client.permissions:
        list_patient_address = helper.make_patient_list_address()
        return await messaging.get_state_by_address(conn, list_patient_address)
    # client_address = consent_helper.make_client_address(client_key)
    # LOGGER.debug('client_address: ' + str(client_address))
    # client_resources = await messaging.get_state_by_address(conn, client_address)
    # LOGGER.debug('client_resources: ' + str(client_resources))
    # for entity in client_resources.entries:
    #     cl = Client()
    #     cl.ParseFromString(entity.data)
    #     LOGGER.debug('client: ' + str(cl))
    #     if Permission(type=Permission.READ_PATIENT) in cl.permissions:
    #         return await messaging.get_state_by_address(conn, address_suffix)
    raise ApiForbidden("Insufficient permission")


async def add_lab(conn, timeout, batches):
    await _send(conn, timeout, batches)


async def add_lab_test(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.WRITE_LAB_TEST) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    # client_address = consent_helper.make_client_address(client_key)
    # LOGGER.debug('client_address: ' + str(client_address))
    # client_resources = await messaging.get_state_by_address(conn, client_address)
    # LOGGER.debug('client_resources: ' + str(client_resources))
    # for entity in client_resources.entries:
    #     cl = Client()
    #     cl.ParseFromString(entity.data)
    #     LOGGER.debug('client: ' + str(cl))
    #     if Permission(type=Permission.WRITE_LAB_TEST) in cl.permissions:
    #         LOGGER.debug('has permission: True')
    #         await _send(conn, timeout, batches)
    #         return
    #     else:
    #         LOGGER.debug('client_resources: False')
    raise ApiForbidden("Insufficient permission")


async def get_labs(conn, client_key):
    # client_address = consent_helper.make_client_address(client_key)
    # LOGGER.debug('client_address: ' + str(client_address))
    # client_resources = await messaging.get_state_by_address(conn, client_address)
    # LOGGER.debug('client_resources: ' + str(client_resources))
    # for entity in client_resources.entries:
    #     cl = Client()
    #     cl.ParseFromString(entity.data)
    #     LOGGER.debug('client: ' + str(cl))
    #     if Permission(type=Permission.READ_LAB) in cl.permissions:
    #         return await messaging.get_state_by_address(conn, address_suffix)
    client = await get_client(conn, client_key)
    if Permission(type=Permission.READ_LAB) in client.permissions:
        LOGGER.debug('has permission: True')
        list_lab_address = helper.make_lab_list_address()
        return await messaging.get_state_by_address(conn, list_lab_address)
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def get_client(conn, client_key):
    client_address = consent_helper.make_client_address(client_key)
    LOGGER.debug('client_address: ' + str(client_address))
    client_resources = await messaging.get_state_by_address(conn, client_address)
    LOGGER.debug('client_resources: ' + str(client_resources))
    for entity in client_resources.entries:
        cl = Client()
        cl.ParseFromString(entity.data)
        LOGGER.debug('client: ' + str(cl))
        return cl
    raise ApiUnauthorized("No such client registered")


async def get_lab_tests(conn, client_key):
    client = await get_client(conn, client_key)
    lab_tests = {}
    if Permission(type=Permission.READ_LAB_TEST) in client.permissions:
        lab_tests_address = helper.make_lab_test_list_address()
        LOGGER.debug('has READ_LAB_TEST permission: ' + str(lab_tests_address))
        lab_test_resources = await messaging.get_state_by_address(conn, lab_tests_address)
        for entity in lab_test_resources.entries:
            lt = payload_pb2.AddLabTest()
            lt.ParseFromString(entity.data)
            lab_tests[entity.address] = lt
        return lab_tests
    elif Permission(type=Permission.READ_OWN_LAB_TEST) in client.permissions:
        lab_test_ids_address = helper.make_lab_test_list_by_patient_address(client_key)
        LOGGER.debug('has READ_OWN_LAB_TEST permission: ' + str(lab_test_ids_address))
        lab_test_ids = await messaging.get_state_by_address(conn, lab_test_ids_address)
        for entity in lab_test_ids.entries:
            lab_test_id = entity.data.decode()
            lab_test_address = helper.make_lab_test_address(lab_test_id)
            LOGGER.debug('get lab test: ' + str(lab_test_address))
            lab_test_resources = await messaging.get_state_by_address(conn, lab_test_address)
            for entity2 in lab_test_resources.entries:
                LOGGER.debug('get lab test entity2: ' + str(entity2.address))
                lt = payload_pb2.AddLabTest()
                lt.ParseFromString(entity2.data)
                lab_tests[entity2.address] = lt
        return lab_tests
    else:
        LOGGER.debug('neither READ_OWN_LAB_TEST nor READ_LAB_TEST permissions')
    raise ApiForbidden("Insufficient permission")
