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

# from rest_api.common.protobuf import payload_pb2
from rest_api.common import helper
from rest_api.common.protobuf.payload_pb2 import AddPulseWithUser, CreateDoctor, CreatePatient, \
    AddLabTestWithUser, Claim

from rest_api.insurance_common import helper as insurance_helper
from rest_api.insurance_common.protobuf.insurance_payload_pb2 import Insurance, ContractWithUser

from rest_api.payment_common import helper as payment_helper
from rest_api.payment_common.protobuf.payment_payload_pb2 import Payment

from rest_api.consent_common import helper as consent_helper
from rest_api.consent_common.protobuf.consent_payload_pb2 import Client, Permission, ActionOnAccess
# from rest_api.consent_common.protobuf import consent_payload_pb2
# from rest_api.common.protobuf import payload_pb2
from rest_api.workflow import messaging
from rest_api.workflow.errors import ApiForbidden, ApiUnauthorized, ApiBadRequest

# from rest_api.workflow.errors import ApiBadRequest
# from rest_api.workflow.errors import ApiInternalError

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


async def add_insurance(conn, timeout, batches):
    await _send(conn, timeout, batches)


async def get_doctors(conn, client_key):
    client = await get_client(conn, client_key)
    doctors = {}
    if Permission(type=Permission.READ_DOCTOR) in client.permissions:
        list_doctors_address = helper.make_doctor_list_address()
        doctor_resources = await messaging.get_state_by_address(conn, list_doctors_address)
        for entity in doctor_resources.entries:
            doc = CreateDoctor()
            doc.ParseFromString(entity.data)
            doctors[entity.address] = doc
        return doctors
    raise ApiForbidden("Insufficient permission")


async def add_patient(conn, timeout, batches):
    await _send(conn, timeout, batches)


async def get_patients(conn, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.READ_PATIENT) in client.permissions:
        list_patient_address = helper.make_patient_list_address()
        return await messaging.get_state_by_address(conn, list_patient_address)
    raise ApiForbidden("Insufficient permission")


async def get_insurances(conn, client_key):
    client = await get_client(conn, client_key)
    insurances = {}
    if Permission(type=Permission.READ_INSURANCE_COMPANY) in client.permissions:
        list_insurance_address = insurance_helper.make_insurance_list_address()
        insurance_resources = await messaging.get_state_by_address(conn, list_insurance_address)
        for entity in insurance_resources.entries:
            ins = Insurance()
            ins.ParseFromString(entity.data)
            insurances[entity.address] = ins
        return insurances
    raise ApiForbidden("Insufficient permission")


async def get_patient(conn, patient_key):
    list_patient_address = helper.make_patient_address(patient_key)
    patient_resources = await messaging.get_state_by_address(conn, list_patient_address)
    for entity in patient_resources.entries:
        lt = CreatePatient()
        lt.ParseFromString(entity.data)
        return lt
    raise ApiBadRequest("No such patient exist: " + str(patient_key))


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
    raise ApiForbidden("Insufficient permission")


async def create_payment(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.WRITE_PAYMENT) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def add_pulse(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.WRITE_PULSE) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def add_claim(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.WRITE_CLAIM) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def add_contract(conn, timeout, batches, client_key):
    # LOGGER.debug('add_contract')
    # await _send(conn, timeout, batches)
    client = await get_client(conn, client_key)
    if Permission(type=Permission.WRITE_CONTRACT) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def revoke_access(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.REVOKE_ACCESS) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def grant_access(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.GRANT_ACCESS) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
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


async def has_consent(conn, dest_pkey, src_pkey):  # dest_pkey - doctor, src_pkey - patient
    consent_list = await get_consent(conn, dest_pkey)
    for address, data in consent_list.items():
        LOGGER.debug('consent_address: data -> ' + str(data) + '; src_key -> ' + str(src_pkey))
        if data.patient_pkey == src_pkey:
            LOGGER.debug('has consent!')
            return True
    return False


async def get_consent(conn, client_key):
    consent_address = consent_helper.make_consent_list_address_by_destination_client(client_key)
    LOGGER.debug('consent_address: ' + str(consent_address))
    consent_resources = await messaging.get_state_by_address(conn, consent_address)
    LOGGER.debug('consent_resources: ' + str(consent_resources))
    consent_list = {}
    for entity in consent_resources.entries:
        aoa = ActionOnAccess()
        aoa.ParseFromString(entity.data)
        consent_list[entity.address] = aoa
        LOGGER.debug('consent: ' + str(aoa))
    return consent_list


async def get_lab_tests(conn, client_key):
    client = await get_client(conn, client_key)
    lab_tests = {}
    if Permission(type=Permission.READ_LAB_TEST) in client.permissions:
        lab_tests_address = helper.make_lab_test_list_address()
        LOGGER.debug('has READ_LAB_TEST permission: ' + str(client_key))
        #
        consent = await get_consent(conn, client_key)
        patient_list = {}
        for address, pt in consent.items():
            LOGGER.debug('patient consent: ' + str(pt))
            patient = await get_patient(conn, pt.patient_pkey)
            patient_list[pt.patient_pkey] = patient
        #
        lab_test_resources = await messaging.get_state_by_address(conn, lab_tests_address)
        for entity in lab_test_resources.entries:
            lt = AddLabTestWithUser()
            lt.ParseFromString(entity.data)
            lab_tests[entity.address] = lt
            LOGGER.debug('lab_test: ' + str(lt))
        for patient_address, pt in patient_list.items():
            LOGGER.debug('patient: ' + str(pt))
            for pulse_address, lt in lab_tests.items():
                LOGGER.debug('lab_test: ' + str(lt))
                if patient_address == lt.client_pkey:
                    LOGGER.debug('match!')
                    pt_local = patient_list[patient_address]
                    lt.name = pt_local.name
                    lt.surname = pt_local.surname
                    lab_tests[pulse_address] = lt
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
                lt = AddLabTestWithUser()
                lt.ParseFromString(entity2.data)
                lab_tests[entity2.address] = lt
        return lab_tests
    else:
        LOGGER.debug('neither READ_OWN_LAB_TEST nor READ_LAB_TEST permissions')
    raise ApiForbidden("Insufficient permission")


async def get_pulse_list(conn, client_key):
    client = await get_client(conn, client_key)
    pulse_list = {}
    if Permission(type=Permission.READ_PULSE) in client.permissions:
        pulse_list_address = helper.make_pulse_list_address()
        LOGGER.debug('has READ_PULSE permission: ' + str(client_key))
        consent = await get_consent(conn, client_key)
        patient_list = {}
        for address, pt in consent.items():
            LOGGER.debug('patient consent: ' + str(pt))
            patient = await get_patient(conn, pt.patient_pkey)
            patient_list[pt.patient_pkey] = patient
        pulse_list_resources = await messaging.get_state_by_address(conn, pulse_list_address)
        for entity in pulse_list_resources.entries:
            pl = AddPulseWithUser()
            pl.ParseFromString(entity.data)
            pulse_list[entity.address] = pl
            LOGGER.debug('pulse: ' + str(pl))
        for patient_address, pt in patient_list.items():
            LOGGER.debug('patient: ' + str(pt))
            for pulse_address, pl in pulse_list.items():
                LOGGER.debug('pulse: ' + str(pl))
                if patient_address == pl.client_pkey:
                    LOGGER.debug('match!')
                    pt_local = patient_list[patient_address]
                    pl.name = pt_local.name
                    pl.surname = pt_local.surname
                    pulse_list[pulse_address] = pl
        return pulse_list
    elif Permission(type=Permission.READ_OWN_PULSE) in client.permissions:
        pulse_list_ids_address = helper.make_pulse_list_by_patient_address(client_key)
        LOGGER.debug('has READ_OWN_PULSE permission: ' + str(pulse_list_ids_address))
        pulse_list_ids = await messaging.get_state_by_address(conn, pulse_list_ids_address)
        for entity in pulse_list_ids.entries:
            pulse_id = entity.data.decode()
            pulse_address = helper.make_pulse_address(pulse_id)
            LOGGER.debug('get pulse: ' + str(pulse_address))
            pulse_resources = await messaging.get_state_by_address(conn, pulse_address)
            for entity2 in pulse_resources.entries:
                LOGGER.debug('get pulse entity2: ' + str(entity2.address))
                pl = AddPulseWithUser()
                pl.ParseFromString(entity2.data)
                pulse_list[entity2.address] = pl
        return pulse_list
    else:
        LOGGER.debug('neither READ_OWN_PULSE nor READ_PULSE permissions')
    raise ApiForbidden("Insufficient permission")


async def close_claim(conn, timeout, batches, dest_pkey, src_pkey):
    client = await get_client(conn, dest_pkey)
    if Permission(type=Permission.READ_CLAIM) in client.permissions \
            and Permission(type=Permission.UPDATE_CLAIM) in client.permissions:
        LOGGER.debug('has READ_CLAIM and UPDATE_CLAIM permission: True')
        # Has consent from patient
        consent = await has_consent(conn, dest_pkey, src_pkey)
        if not consent:
            LOGGER.debug('no consent from patient')
            raise ApiForbidden("Insufficient permission")
        #
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def get_claims(conn, client_key):
    client = await get_client(conn, client_key)
    claim_list = {}
    if Permission(type=Permission.READ_CLAIM) in client.permissions:
        claim_list_address = helper.make_claim_list_address()
        LOGGER.debug('has READ_CLAIM permission: ' + str(client_key))
        # consent = await get_consent(conn, client_key)
        # patient_list = {}
        # for address, pt in consent.items():
        #     LOGGER.debug('patient consent: ' + str(pt))
        #     patient = await get_patient(conn, pt.patient_pkey)
        #     patient_list[pt.patient_pkey] = patient
        claim_list_resources = await messaging.get_state_by_address(conn, claim_list_address)
        for entity in claim_list_resources.entries:
            cl = Claim()
            cl.ParseFromString(entity.data)
            claim_list[entity.address] = cl
            LOGGER.debug('claim: ' + str(cl))
        # for patient_address, pt in patient_list.items():
        #     LOGGER.debug('patient: ' + str(pt))
        #     for pulse_address, pl in pulse_list.items():
        #         LOGGER.debug('pulse: ' + str(pl))
        #         if patient_address == pl.client_pkey:
        #             LOGGER.debug('match!')
        #             pt_local = patient_list[patient_address]
        #             pl.name = pt_local.name
        #             pl.surname = pt_local.surname
        #             pulse_list[pulse_address] = pl
        return claim_list
    elif Permission(type=Permission.READ_OWN_CLAIM) in client.permissions:
        claim_list_ids_address = helper.make_claim_list_by_patient_address(client_key)
        LOGGER.debug('has READ_OWN_CLAIM permission: ' + str(claim_list_ids_address))
        claim_list_ids = await messaging.get_state_by_address(conn, claim_list_ids_address)
        for entity in claim_list_ids.entries:
            claim_id = entity.data.decode()
            claim_address = helper.make_claim_address(claim_id)
            LOGGER.debug('get claim: ' + str(claim_address))
            claim_resources = await messaging.get_state_by_address(conn, claim_address)
            for entity2 in claim_resources.entries:
                LOGGER.debug('get claim entity2: ' + str(entity2.address))
                cl = Claim()
                cl.ParseFromString(entity2.data)
                claim_list[entity2.address] = cl
        return claim_list
    else:
        LOGGER.debug('neither READ_OWN_CLAIM nor READ_CLAIM permissions')
    raise ApiForbidden("Insufficient permission")


async def get_contracts(conn, client_key):
    client = await get_client(conn, client_key)
    contract_list = {}
    if Permission(type=Permission.READ_CONTRACT) in client.permissions:
        contract_list_address = insurance_helper.make_contract_list_address()
        LOGGER.debug('has READ_CONTRACT permission: ' + str(client_key))
        contract_list_ids = await messaging.get_state_by_address(conn, contract_list_address)
        for entity in contract_list_ids.entries:
            con = ContractWithUser()
            con.ParseFromString(entity.data)
            contract_list[entity.address] = con
            LOGGER.debug('contract: ' + str(con))
        return contract_list
    elif Permission(type=Permission.READ_OWN_CONTRACT) in client.permissions:
        contract_list_ids_address = insurance_helper.make_contract_list_by_insurance_address(client_key)
        LOGGER.debug('has READ_OWN_CONTRACT permission: ' + str(contract_list_ids_address))
        contract_list_ids = await messaging.get_state_by_address(conn, contract_list_ids_address)
        for entity in contract_list_ids.entries:
            contract_id = entity.data.decode()
            contract_address = insurance_helper.make_contract_address(contract_id)
            LOGGER.debug('get contract: ' + str(contract_address))
            contract_resources = await messaging.get_state_by_address(conn, contract_address)
            for entity2 in contract_resources.entries:
                LOGGER.debug('get contract entity2: ' + str(entity2.address))
                con = ContractWithUser()
                con.ParseFromString(entity2.data)
                contract_list[entity2.address] = con
        return contract_list
    else:
        LOGGER.debug('neither READ_CONTRACT or READ_OWN_CONTRACT permissions')
    raise ApiForbidden("Insufficient permission")


async def get_payment_list(conn, client_key):
    client = await get_client(conn, client_key)
    payment_list = {}
    if Permission(type=Permission.READ_PAYMENT) in client.permissions or \
            Permission(type=Permission.READ_OWN_PAYMENT) in client.permissions:
        payment_list_address = payment_helper.make_payment_list_address()
        LOGGER.debug('has READ_PAYMENT or READ_OWN_PAYMENT permission: ' + str(client_key))
        payment_resources = await messaging.get_state_by_address(conn, payment_list_address)
        for entity in payment_resources.entries:
            LOGGER.debug('get payment entity: ' + str(entity.address))
            pay = Payment()
            pay.ParseFromString(entity.data)
            payment_list[entity.address] = pay
        return payment_list
    else:
        LOGGER.debug('neither READ_PAYMENT or READ_OWN_PAYMENT permissions')
    raise ApiForbidden("Insufficient permission")
