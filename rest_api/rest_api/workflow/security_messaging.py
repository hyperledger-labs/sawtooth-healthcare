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


def _validate_permission(expected_permission, current_permissions):
    if payload_pb2.Permission(type=expected_permission) not in current_permissions:
        raise ApiForbidden("Insufficient permission")


async def add_clinic(conn, timeout, batches):
    await _send(conn, timeout, batches)


async def get_clinics(conn, address_suffix, client_key):
    client_address = helper.make_clinic_address(client_key)
    LOGGER.debug('client_address: ' + str(client_address))
    clinic_resources = await messaging.get_state_by_address(conn, client_address)
    LOGGER.debug('clinic_resources: ' + str(clinic_resources))
    for entity in clinic_resources.entries:
        cl = payload_pb2.CreateClinic()
        cl.ParseFromString(entity.data)
        LOGGER.debug('clinic: ' + str(cl))
        _validate_permission(payload_pb2.Permission.READ_CLINIC, cl.permissions)
    return await messaging.get_state_by_address(conn, address_suffix)


async def add_doctor(conn, timeout, batches):
    await _send(conn, timeout, batches)


async def get_doctors(conn, address_suffix, client_key):
    client_address = helper.make_doctor_address(client_key)
    LOGGER.debug('client_address: ' + str(client_address))
    doctor_resources = await messaging.get_state_by_address(conn, client_address)
    LOGGER.debug('doctor_resources: ' + str(doctor_resources))
    for entity in doctor_resources.entries:
        doc = payload_pb2.CreateDoctor()
        doc.ParseFromString(entity.data)
        LOGGER.debug('doctor: ' + str(doc))
        _validate_permission(payload_pb2.Permission.READ_DOCTOR, doc.permissions)
    return await messaging.get_state_by_address(conn, address_suffix)


async def add_patient(conn, timeout, batches):
    await _send(conn, timeout, batches)


async def get_patients(conn, address_suffix, client_key):
    client_address = helper.make_patient_address(client_key)
    LOGGER.debug('client_address: ' + str(client_address))
    patient_resources = await messaging.get_state_by_address(conn, client_address)
    LOGGER.debug('patient_resources: ' + str(patient_resources))
    for entity in patient_resources.entries:
        pat = payload_pb2.CreatePatient()
        pat.ParseFromString(entity.data)
        LOGGER.debug('patient: ' + str(pat))
        _validate_permission(payload_pb2.Permission.READ_PATIENT, pat.permissions)
    return await messaging.get_state_by_address(conn, address_suffix)
