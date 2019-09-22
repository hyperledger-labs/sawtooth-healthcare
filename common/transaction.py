import hashlib
import random
import time
import logging
from sawtooth_sdk.protobuf.batch_pb2 import BatchList, BatchHeader, Batch
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction, TransactionHeader

# import common.helper as helper
# from common.protobuf import payload_pb2
from . import helper as helper
from .protobuf import payload_pb2

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


def _make_transaction(payload, inputs, outputs, txn_signer, batch_signer):
    txn_header_bytes, signature = _transaction_header(txn_signer, batch_signer, inputs, outputs, payload)

    txn = Transaction(
        header=txn_header_bytes,
        header_signature=signature,
        payload=payload.SerializeToString()
    )

    return txn

    # transactions = [txn]
    #
    # batch_header_bytes, signature = _batch_header(batch_signer, transactions)
    #
    # batch = Batch(
    #     header=batch_header_bytes,
    #     header_signature=signature,
    #     transactions=transactions
    # )
    #
    # # batch_list = BatchList(batches=[batch])
    # # batch_id = batch_list.batches[0].header_signature
    # # return batch_list, batch_id
    # return batch, batch.header_signature


def make_batch_and_id(transactions, batch_signer):
    batch_header_bytes, signature = _batch_header(batch_signer, transactions)

    batch = Batch(
        header=batch_header_bytes,
        header_signature=signature,
        transactions=transactions
    )

    return batch, batch.header_signature


def _make_header_and_batch(payload, inputs, outputs, txn_signer, batch_signer):
    txn_header_bytes, signature = _transaction_header(txn_signer, batch_signer, inputs, outputs, payload)

    txn = Transaction(
        header=txn_header_bytes,
        header_signature=signature,
        payload=payload.SerializeToString()
    )

    transactions = [txn]

    batch_header_bytes, signature = _batch_header(batch_signer, transactions)

    batch = Batch(
        header=batch_header_bytes,
        header_signature=signature,
        transactions=transactions
    )

    # batch_list = BatchList(batches=[batch])
    # batch_id = batch_list.batches[0].header_signature
    # return batch_list, batch_id
    return batch, batch.header_signature


def _transaction_header(txn_signer, batch_signer, inputs, outputs, payload):
    txn_header_bytes = TransactionHeader(
        family_name=helper.TP_FAMILYNAME,
        family_version=helper.TP_VERSION,
        inputs=inputs,
        outputs=outputs,
        signer_public_key=txn_signer.get_public_key().as_hex(),  # signer.get_public_key().as_hex(),
        # In this example, we're signing the batch with the same private key,
        # but the batch can be signed by another party, in which case, the
        # public key will need to be associated with that key.
        batcher_public_key=batch_signer.get_public_key().as_hex(),  # signer.get_public_key().as_hex(),
        # In this example, there are no dependencies.  This list should include
        # an previous transaction header signatures that must be applied for
        # this transaction to successfully commit.
        # For example,
        # dependencies=['540a6803971d1880ec73a96cb97815a95d374cbad5d865925e5aa0432fcf1931539afe10310c122c5eaae15df61236079abbf4f258889359c4d175516934484a'],
        dependencies=[],
        nonce=random.random().hex().encode(),
        payload_sha512=hashlib.sha512(payload.SerializeToString()).hexdigest()
    ).SerializeToString()

    signature = txn_signer.sign(txn_header_bytes)
    return txn_header_bytes, signature


def _batch_header(batch_signer, transactions):
    batch_header_bytes = BatchHeader(
        signer_public_key=batch_signer.get_public_key().as_hex(),
        transaction_ids=[txn.header_signature for txn in transactions],
    ).SerializeToString()

    signature = batch_signer.sign(batch_header_bytes)

    return batch_header_bytes, signature


def create_doctor(txn_signer, batch_signer, name, surname):
    doctor_pkey = txn_signer.get_public_key().as_hex()
    LOGGER.debug('doctor_pkey: ' + str(doctor_pkey))
    doctor_hex = helper.make_doctor_address(doctor_pkey=doctor_pkey)
    LOGGER.debug('doctor_hex: ' + str(doctor_hex))
    # permissions = [payload_pb2.Permission(type=payload_pb2.Permission.READ_DOCTOR),
    #                payload_pb2.Permission(type=payload_pb2.Permission.READ_OWN_DOCTOR)]

    doctor = payload_pb2.CreateDoctor(
        public_key=doctor_pkey,
        name=name,
        surname=surname)

    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.CREATE_DOCTOR,
        create_doctor=doctor)

    return _make_transaction(
        payload=payload,
        inputs=[doctor_hex],
        outputs=[doctor_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def create_patient(txn_signer, batch_signer, name, surname):
    patient_pkey = txn_signer.get_public_key().as_hex()
    LOGGER.debug('patient_pkey: ' + str(patient_pkey))
    patient_hex = helper.make_patient_address(patient_pkey=patient_pkey)
    LOGGER.debug('patient_hex: ' + str(patient_hex))
    # permissions = [payload_pb2.Permission(type=payload_pb2.Permission.READ_PATIENT),
    #                payload_pb2.Permission(type=payload_pb2.Permission.READ_OWN_PATIENT)]
    patient = payload_pb2.CreatePatient(
        # public_key=txn_signer.get_public_key().as_hex(),
        name=name,
        surname=surname)

    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.CREATE_PATIENT,
        create_patient=patient)

    LOGGER.debug('payload: ' + str(payload))

    return _make_transaction(
        payload=payload,
        inputs=[patient_hex],
        outputs=[patient_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def create_clinic(txn_signer, batch_signer, name):
    clinic_pkey = txn_signer.get_public_key().as_hex()
    LOGGER.debug('clinic_pkey: ' + str(clinic_pkey))
    inputs = outputs = helper.make_clinic_address(clinic_pkey=clinic_pkey)
    LOGGER.debug('inputs: ' + str(inputs))
    # permissions = [payload_pb2.Permission(type=payload_pb2.Permission.READ_CLINIC),
    #                payload_pb2.Permission(type=payload_pb2.Permission.READ_OWN_CLINIC)]
    clinic = payload_pb2.CreateClinic(
        # public_key=clinic_pkey,
        name=name)

    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.CREATE_CLINIC,
        create_clinic=clinic)

    # account = payload_pb2.CreateAccount(
    #     label=label,
    #     description=description)
    # payload = payload_pb2.TransactionPayload(
    #     payload_type=payload_pb2.TransactionPayload.CREATE_ACCOUNT,
    #     create_account=account)

    return _make_transaction(
        payload=payload,
        inputs=[inputs],
        outputs=[outputs],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def create_lab(txn_signer, batch_signer, name):
    lab_pkey = txn_signer.get_public_key().as_hex()
    LOGGER.debug('lab_pkey: ' + str(lab_pkey))
    inputs = outputs = helper.make_lab_address(lab_pkey=lab_pkey)
    LOGGER.debug('inputs: ' + str(inputs))
    # permissions = [payload_pb2.Permission(type=payload_pb2.Permission.READ_CLINIC),
    #                payload_pb2.Permission(type=payload_pb2.Permission.READ_OWN_CLINIC)]
    lab = payload_pb2.CreateLab(
        # public_key=clinic_pkey,
        name=name)

    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.CREATE_LAB,
        create_lab=lab)

    return _make_transaction(
        payload=payload,
        inputs=[inputs],
        outputs=[outputs],
        txn_signer=txn_signer,
        batch_signer=batch_signer)

# def create_clinic(txn_signer, batch_signer, name):
#     clinic_pkey = txn_signer.get_public_key().as_hex()
#     LOGGER.debug('clinic_pkey: ' + str(clinic_pkey))
#     inputs = outputs = helper.make_clinic_address(clinic_pkey=clinic_pkey)
#     LOGGER.debug('inputs: ' + str(inputs))
#     permissions = [payload_pb2.Permission(type=payload_pb2.Permission.READ_CLINIC),
#                    payload_pb2.Permission(type=payload_pb2.Permission.READ_OWN_CLINIC)]
#     clinic = payload_pb2.CreateClinic(
#         # public_key=clinic_pkey,
#         name=name,
#         permissions=permissions)
#
#     payload = payload_pb2.TransactionPayload(
#         payload_type=payload_pb2.TransactionPayload.CREATE_CLINIC,
#         create_clinic=clinic)
#
#     # account = payload_pb2.CreateAccount(
#     #     label=label,
#     #     description=description)
#     # payload = payload_pb2.TransactionPayload(
#     #     payload_type=payload_pb2.TransactionPayload.CREATE_ACCOUNT,
#     #     create_account=account)
#
#     return _make_header_and_batch(
#         payload=payload,
#         inputs=[inputs],
#         outputs=[outputs],
#         txn_signer=txn_signer,
#         batch_signer=batch_signer)


def add_lab_test(txn_signer, batch_signer, height, weight, gender, a_g_ratio, albumin, alkaline_phosphatase, appearance,
                 bilirubin, casts, color, uid, client_pkey):
    # client_pkey = txn_signer.get_public_key().as_hex()
    # patient_hex = helper.make_patient_address(patient_pkey=client_pkey)
    lab_test_hex = helper.make_lab_test_address(lab_test_id=uid)
    lab_test_patient_rel_hex = helper.make_lab_test_patient__relation_address(uid, client_pkey)
    patient_lab_test_rel_hex = helper.make_patient_lab_test__relation_address(client_pkey, uid)
    current_times_str = str(time.time())
    # clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)

    lab_test = payload_pb2.AddLabTest(
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
        event_time=current_times_str,
        id=uid,
        client_pkey=client_pkey
    )

    LOGGER.debug('lab_test: ' + str(lab_test))

    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.ADD_LAB_TEST,
        lab_test=lab_test)

    return _make_transaction(
        payload=payload,
        inputs=[lab_test_hex, lab_test_patient_rel_hex, patient_lab_test_rel_hex],
        outputs=[lab_test_hex, lab_test_patient_rel_hex, patient_lab_test_rel_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def add_pulse(txn_signer, batch_signer, pulse, uid, timestamp, client_pkey):
    # patient_pkey = txn_signer.get_public_key().as_hex()

    pulse_hex = helper.make_pulse_address(uid)
    pulse_patient_rel_hex = helper.make_pulse_patient__relation_address(uid, client_pkey)
    patient_pulse_rel_hex = helper.make_patient_pulse__relation_address(client_pkey, uid)

    pulse_payload = payload_pb2.AddPulse(
        # public_key=patient_pkey,
        id=uid,
        pulse=str(pulse),
        timestamp=timestamp,
        client_pkey=client_pkey
    )

    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.ADD_PULSE,
        pulse=pulse_payload)

    return _make_header_and_batch(
        payload=payload,
        inputs=[pulse_hex, pulse_patient_rel_hex, patient_pulse_rel_hex],
        outputs=[pulse_hex, pulse_patient_rel_hex, patient_pulse_rel_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def register_claim(txn_signer, batch_signer, claim_id, patient_pkey):
    # batch_key = txn_key = self._signer.get_public_key().as_hex()
    clinic_pkey = txn_signer.get_public_key().as_hex()

    clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)
    claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=clinic_pkey)
    patient_hex = helper.make_patient_address(patient_pkey=patient_pkey)

    claim = payload_pb2.CreateClaim(
        claim_id=claim_id,
        clinic_pkey=clinic_pkey,
        patient_pkey=patient_pkey,
    )

    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.CREATE_CLAIM,
        create_claim=claim)

    return _make_header_and_batch(
        payload=payload,
        inputs=[claim_hex, clinic_hex, patient_hex],
        outputs=[claim_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def assign_doctor(txn_signer, batch_signer, claim_id, description, event_time):
    clinic_pkey = txn_signer.get_public_key().as_hex()
    clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)
    claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=clinic_pkey)
    event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=clinic_pkey, event_time=event_time)

    assign = payload_pb2.ActionOnClaim(
        claim_id=claim_id,
        clinic_pkey=clinic_pkey,
        description=description,
        event_time=event_time)

    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.ASSIGN_DOCTOR,
        assign_doctor=assign)

    return _make_header_and_batch(
        payload=payload,
        inputs=[claim_hex, event_hex, clinic_hex],
        outputs=[event_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def first_visit(txn_signer, batch_signer, claim_id, description, event_time):
    clinic_pkey = txn_signer.get_public_key().as_hex()
    clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)
    claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=clinic_pkey)
    event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=clinic_pkey, event_time=event_time)

    visit = payload_pb2.ActionOnClaim(
        claim_id=claim_id,
        clinic_pkey=clinic_pkey,
        description=description,
        event_time=event_time
    )

    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.FIRST_VISIT,
        first_visit=visit)

    # batch, signature = self._create_txn_and_batch(txn_key, BATCH_KEY, [claim_hex, event_hex, clinic_hex],
    #                                               [event_hex], payload)
    return _make_header_and_batch(
        payload=payload,
        inputs=[claim_hex, event_hex, clinic_hex],
        outputs=[event_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def pass_tests(txn_signer, batch_signer, claim_id, description, event_time):
    clinic_pkey = txn_signer.get_public_key().as_hex()
    clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)
    claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=clinic_pkey)

    event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=clinic_pkey, event_time=event_time)

    tests = payload_pb2.ActionOnClaim(
        claim_id=claim_id,
        clinic_pkey=clinic_pkey,
        description=description,
        event_time=event_time
    )

    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.PASS_TESTS,
        pass_tests=tests)

    return _make_header_and_batch(
        payload=payload,
        inputs=[claim_hex, event_hex, clinic_hex],
        outputs=[event_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def attend_procedures(txn_signer, batch_signer, claim_id, description, event_time):
    clinic_pkey = txn_signer.get_public_key().as_hex()
    clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)
    claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=clinic_pkey)

    event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=clinic_pkey, event_time=event_time)

    procedures = payload_pb2.ActionOnClaim(
        claim_id=claim_id,
        clinic_pkey=clinic_pkey,
        description=description,
        event_time=event_time
    )

    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.ATTEND_PROCEDURES,
        attend_procedures=procedures)

    # batch, signature = self._create_txn_and_batch(txn_key, BATCH_KEY, [claim_hex, event_hex, clinic_hex],
    #                                               [event_hex], payload)
    return _make_header_and_batch(
        payload=payload,
        inputs=[claim_hex, event_hex, clinic_hex],
        outputs=[event_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def eat_pills(txn_signer, batch_signer, claim_id, description, event_time):
    clinic_pkey = txn_signer.get_public_key().as_hex()
    clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)
    claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=clinic_pkey)

    event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=clinic_pkey, event_time=event_time)

    pills = payload_pb2.ActionOnClaim(
        claim_id=claim_id,
        clinic_pkey=clinic_pkey,
        description=description,
        event_time=event_time
    )

    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.EAT_PILLS,
        eat_pills=pills)

    # batch, signature = self._create_txn_and_batch(txn_key, BATCH_KEY, [claim_hex, event_hex, clinic_hex],
    #                                               [event_hex], payload)
    return _make_header_and_batch(
        payload=payload,
        inputs=[claim_hex, event_hex, clinic_hex],
        outputs=[event_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def next_visit(txn_signer, batch_signer, claim_id, description, event_time):
    clinic_pkey = txn_signer.get_public_key().as_hex()
    clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)
    claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=clinic_pkey)

    event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=clinic_pkey, event_time=event_time)

    visit = payload_pb2.ActionOnClaim(
        claim_id=claim_id,
        clinic_pkey=clinic_pkey,
        description=description,
        event_time=event_time
    )

    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.NEXT_VISIT,
        next_visit=visit)

    # batch, signature = self._create_txn_and_batch(txn_key, BATCH_KEY, [claim_hex, event_hex, clinic_hex],
    #                                               [event_hex], payload)
    return _make_header_and_batch(
        payload=payload,
        inputs=[claim_hex, event_hex, clinic_hex],
        outputs=[event_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)
