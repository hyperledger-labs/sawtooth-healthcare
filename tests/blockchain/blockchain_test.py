import hashlib
import logging
import random
import time
import unittest
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from uuid import uuid4

from sawtooth_cli.rest_client import RestClient
from sawtooth_sdk.protobuf import batch_pb2
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader, Batch
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader, Transaction
from sawtooth_signing import create_context, CryptoFactory

from sawtooth_healthcare.common import helper
from sawtooth_healthcare.processor.protobuf import payload_pb2

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def make_key():
    context = create_context('secp256k1')
    private_key = context.new_random_private_key()
    signer = CryptoFactory(context).new_signer(private_key)
    return signer


REST_URL = "localhost:8008"  # 'rest-api:8008'

BATCH_KEY = make_key()


class BlockchainTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        wait_for_rest_apis([REST_URL])
        cls.client = HealthCareClient(REST_URL)

        cls.signer_doctor_00 = make_key()
        cls.signer_doctor_01 = make_key()
        cls.signer_patient_00 = make_key()
        cls.signer_patient_01 = make_key()
        cls.signer_clinic_00 = make_key()
        cls.signer_clinic_01 = make_key()
        cls.signer_doctor_new_claim_00 = make_key()
        cls.signer_patient_new_claim_00 = make_key()
        cls.signer_clinic_new_claim_00 = make_key()

    def test_00_create_doctor(self):
        self.assertEqual(
            self.client.create_doctor(
                txn_key=self.signer_doctor_00,
                name="Doctor_Name_00_0_" + uuid4().hex,
                surname="Doctor_Surname_00_0_" + uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.create_doctor(
                txn_key=self.signer_doctor_00,
                name="Doctor_Name_00_0_" + uuid4().hex,
                surname="Doctor_Surname_00_0_" + uuid4().hex)[0]['status'],
            "INVALID",
            "There can only be 1 doctor per public key.")

        self.assertEqual(
            self.client.create_doctor(
                txn_key=self.signer_doctor_01,
                name="Doctor_Name_00_1_" + uuid4().hex,
                surname="Doctor_Surname_00_1_" + uuid4().hex)[0]['status'],
            "COMMITTED")

        LOGGER.info("Get doctors list")
        list_doctors = self.client.list_doctors()
        LOGGER.info("Response: {}".format(list_doctors))

    def test_01_create_patient(self):
        self.assertEqual(
            self.client.create_patient(
                txn_key=self.signer_patient_00,
                name="Patient_Name_01_0_" + uuid4().hex,
                surname="Patient_Surname_01_0_" + uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.create_patient(
                txn_key=self.signer_patient_00,
                name="Patient_Name_01_0_" + uuid4().hex,
                surname="Patient_Surname_01_0_" + uuid4().hex)[0]['status'],
            "INVALID",
            "There can only be 1 patient per public key.")

        self.assertEqual(
            self.client.create_patient(
                txn_key=self.signer_patient_01,
                name="Patient_Name_01_1_" + uuid4().hex,
                surname="Patient_Surname_01_1_" + uuid4().hex)[0]['status'],
            "COMMITTED")

        LOGGER.info("Get patients list")
        list_patients = self.client.list_patients()
        LOGGER.info("Response: {}".format(list_patients))

    def test_02_create_clinic(self):
        self.assertEqual(
            self.client.create_clinic(
                txn_key=self.signer_clinic_00,
                name="Clinic_Name_02_0_" + uuid4().hex)[0]['status'],
            "COMMITTED")

        self.assertEqual(
            self.client.create_clinic(
                txn_key=self.signer_clinic_00,
                name="Clinic_Name_02_0_" + uuid4().hex)[0]['status'],
            "INVALID",
            "There can only be 1 clinic per public key.")

        self.assertEqual(
            self.client.create_clinic(
                txn_key=self.signer_clinic_01,
                name="Clinic_Name_02_1_" + uuid4().hex)[0]['status'],
            "COMMITTED")

        LOGGER.info("Get clinics list")
        list_clinics = self.client.list_clinics()
        LOGGER.info("Response: {}".format(list_clinics))

    def test_03_create_claim(self):
        LOGGER.info("Prerequisite: create clinic 1")
        create_clinic = self.client.create_clinic(
            txn_key=self.signer_clinic_new_claim_00,
            name="Clinic_Name_03_0_" + uuid4().hex)
        LOGGER.info("Response: {}".format(create_clinic))

        self.assertEqual(
            create_clinic[0]['status'],
            "COMMITTED")

        LOGGER.info("Prerequisite: create doctor 1")
        create_doctor = self.client.create_doctor(
            txn_key=self.signer_doctor_new_claim_00,
            name="Doctor_Name_03_0_" + uuid4().hex,
            surname="Doctor_Surname_03_0_" + uuid4().hex)
        LOGGER.info("Response: {}".format(create_doctor))

        self.assertEqual(
            create_doctor[0]['status'],
            "COMMITTED")

        LOGGER.info("Prerequisite: create patient 1")
        create_patient = self.client.create_patient(
            txn_key=self.signer_patient_new_claim_00,
            name="Patient_Name_03_0_" + uuid4().hex,
            surname="Patient_Surname_03_0_" + uuid4().hex)
        LOGGER.info("Response: {}".format(create_doctor))

        self.assertEqual(
            create_patient[0]['status'],
            "COMMITTED")

        clinic1_claim_id = "1"
        LOGGER.info("Create claim by clinic 1 for patient 1")
        create_claim1 = self.client.create_claim(
            txn_key=self.signer_clinic_new_claim_00,
            claim_id=clinic1_claim_id,
            patient_pkey=self.signer_patient_new_claim_00.get_public_key().as_hex())
        LOGGER.info("Response: {}".format(create_claim1))

        self.assertEqual(
            create_claim1[0]['status'],
            "COMMITTED")

        LOGGER.info("Get clinics list")
        list_claims = self.client.list_claims()
        LOGGER.info("Response: {}".format(list_claims))

        LOGGER.info("Get doctors list")
        list_doctors = self.client.list_doctors()
        LOGGER.info("Response: {}".format(list_doctors))

        LOGGER.info("Get patients list")
        list_patients = self.client.list_patients()
        LOGGER.info("Response: {}".format(list_patients))

        LOGGER.info("Assign doctor 1 to the claim")
        assign_doctor = self.client.assign_doctor(
            txn_key=self.signer_clinic_new_claim_00,
            claim_id=clinic1_claim_id,
            doctor_pkey=self.signer_doctor_new_claim_00.get_public_key().as_hex())
        LOGGER.info("Response: {}".format(assign_doctor))

        self.assertEqual(
            assign_doctor[0]['status'],
            "COMMITTED")

        LOGGER.info("Pass first visit")
        initial_examination = self.client.first_visit(
            txn_key=self.signer_clinic_new_claim_00,
            claim_id=clinic1_claim_id,
            doctor_pkey=self.signer_doctor_new_claim_00.get_public_key().as_hex())
        LOGGER.info("Response: {}".format(initial_examination))

        self.assertEqual(
            initial_examination[0]['status'],
            "COMMITTED")

        LOGGER.info("Pass tests")
        tests = self.client.pass_tests(
            txn_key=self.signer_clinic_new_claim_00,
            claim_id=clinic1_claim_id)
        LOGGER.info("Response: {}".format(tests))

        self.assertEqual(
            tests[0]['status'],
            "COMMITTED")

        LOGGER.info("Attend procedures")
        procedures = self.client.attend_procedures(
            txn_key=self.signer_clinic_new_claim_00,
            claim_id=clinic1_claim_id)
        LOGGER.info("Response: {}".format(procedures))

        self.assertEqual(
            procedures[0]['status'],
            "COMMITTED")

        LOGGER.info("Eat pills")
        pills = self.client.eat_pills(
            txn_key=self.signer_clinic_new_claim_00,
            claim_id=clinic1_claim_id)
        LOGGER.info("Response: {}".format(pills))

        self.assertEqual(
            pills[0]['status'],
            "COMMITTED")

        LOGGER.info("Complete next visit")
        pills = self.client.next_visit(
            txn_key=self.signer_clinic_new_claim_00,
            claim_id=clinic1_claim_id,
            doctor_pkey=self.signer_doctor_new_claim_00.get_public_key().as_hex())
        LOGGER.info("Response: {}".format(pills))

        self.assertEqual(
            pills[0]['status'],
            "COMMITTED")

        LOGGER.info("Get claim details list")
        list_claim_details = self.client.list_claim_details(clinic1_claim_id,
                                                            self.signer_clinic_new_claim_00.get_public_key().as_hex())
        LOGGER.info("Response: {}".format(list_claim_details))


class HealthCareClient(object):

    def __init__(self, url):
        self._client = RestClient(base_url="http://{}".format(url))

    def create_doctor(self, txn_key, name, surname):
        doctor = payload_pb2.CreateDoctor(
            public_key=txn_key.get_public_key().as_hex(),
            name=name,
            surname=surname)

        payload = payload_pb2.TransactionPayload(
            payload_type=payload_pb2.TransactionPayload.CREATE_DOCTOR,
            create_doctor=doctor)

        doctor_hex = helper.make_doctor_address(doctor_pkey=txn_key.get_public_key().as_hex())

        batch, signature = self._create_txn_and_batch(txn_key, BATCH_KEY, [doctor_hex], [doctor_hex], payload)

        batch_list = batch_pb2.BatchList(batches=[batch])

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=40)

    def create_patient(self, txn_key, name, surname):
        patient = payload_pb2.CreatePatient(
            public_key=txn_key.get_public_key().as_hex(),
            name=name,
            surname=surname)

        payload = payload_pb2.TransactionPayload(
            payload_type=payload_pb2.TransactionPayload.CREATE_PATIENT,
            create_patient=patient)

        patient_hex = helper.make_patient_address(patient_pkey=txn_key.get_public_key().as_hex())

        batch, signature = self._create_txn_and_batch(txn_key, BATCH_KEY, [patient_hex], [patient_hex], payload)

        batch_list = batch_pb2.BatchList(batches=[batch])

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=40)

    def create_clinic(self, txn_key, name):
        clinic = payload_pb2.CreateClinic(
            public_key=txn_key.get_public_key().as_hex(),
            name=name)

        payload = payload_pb2.TransactionPayload(
            payload_type=payload_pb2.TransactionPayload.CREATE_CLINIC,
            create_clinic=clinic)

        clinic_hex = helper.make_clinic_address(clinic_pkey=txn_key.get_public_key().as_hex())

        batch, signature = self._create_txn_and_batch(txn_key, BATCH_KEY, [clinic_hex], [clinic_hex], payload)

        batch_list = batch_pb2.BatchList(batches=[batch])

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=40)

    def create_claim(self, txn_key, claim_id, patient_pkey):
        clinic_pkey = txn_key.get_public_key().as_hex()
        clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)
        claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=clinic_pkey)

        claim = payload_pb2.CreateClaim(
            claim_id=claim_id,
            clinic_pkey=clinic_pkey,
            patient_pkey=patient_pkey)

        payload = payload_pb2.TransactionPayload(
            payload_type=payload_pb2.TransactionPayload.CREATE_CLAIM,
            create_claim=claim)

        batch, signature = self._create_txn_and_batch(txn_key, BATCH_KEY, [claim_hex, clinic_hex], [claim_hex], payload)

        batch_list = batch_pb2.BatchList(batches=[batch])

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=40)

    def assign_doctor(self, txn_key, claim_id, doctor_pkey):
        clinic_pkey = txn_key.get_public_key().as_hex()
        clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)
        claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=clinic_pkey)
        current_times_str = str(time.time())
        event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=clinic_pkey, event_time=current_times_str)

        assign = payload_pb2.ActionOnClaim(
            claim_id=claim_id,
            clinic_pkey=clinic_pkey,
            description="Doctor: {}, assigned to claim: {}".format(doctor_pkey, claim_hex),
            event_time=current_times_str)

        payload = payload_pb2.TransactionPayload(
            payload_type=payload_pb2.TransactionPayload.ASSIGN_DOCTOR,
            assign_doctor=assign)

        batch, signature = self._create_txn_and_batch(txn_key, BATCH_KEY, [claim_hex, event_hex, clinic_hex],
                                                      [event_hex], payload)

        batch_list = batch_pb2.BatchList(batches=[batch])

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=80)

    def first_visit(self, txn_key, claim_id, doctor_pkey):
        clinic_pkey = txn_key.get_public_key().as_hex()
        clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)
        claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=clinic_pkey)
        current_times_str = str(time.time())
        event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=clinic_pkey, event_time=current_times_str)

        first_visit = payload_pb2.ActionOnClaim(
            claim_id=claim_id,
            clinic_pkey=clinic_pkey,
            description="Doctor: {}, completed first visit for claim: {}, \
            need to pass procedures and eat pills".format(doctor_pkey, claim_hex),
            event_time=current_times_str
        )

        payload = payload_pb2.TransactionPayload(
            payload_type=payload_pb2.TransactionPayload.FIRST_VISIT,
            first_visit=first_visit)

        batch, signature = self._create_txn_and_batch(txn_key, BATCH_KEY, [claim_hex, event_hex, clinic_hex],
                                                      [event_hex], payload)

        batch_list = batch_pb2.BatchList(batches=[batch])

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=80)

    def pass_tests(self, txn_key, claim_id):
        clinic_pkey = txn_key.get_public_key().as_hex()
        clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)
        claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=clinic_pkey)
        current_times_str = str(time.time())
        event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=clinic_pkey, event_time=current_times_str)

        tests = payload_pb2.ActionOnClaim(
            claim_id=claim_id,
            clinic_pkey=clinic_pkey,
            description="Pass tests in scope of claim: {}".format(claim_hex),
            event_time=current_times_str
        )

        payload = payload_pb2.TransactionPayload(
            payload_type=payload_pb2.TransactionPayload.PASS_TESTS,
            pass_tests=tests)

        batch, signature = self._create_txn_and_batch(txn_key, BATCH_KEY, [claim_hex, event_hex, clinic_hex],
                                                      [event_hex], payload)

        batch_list = batch_pb2.BatchList(batches=[batch])

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=80)

    def attend_procedures(self, txn_key, claim_id):
        clinic_pkey = txn_key.get_public_key().as_hex()
        clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)
        claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=clinic_pkey)
        current_times_str = str(time.time())
        event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=clinic_pkey, event_time=current_times_str)

        procedures = payload_pb2.ActionOnClaim(
            claim_id=claim_id,
            clinic_pkey=clinic_pkey,
            description="Complete procedure in scope of claim: {}".format(claim_hex),
            event_time=current_times_str
        )

        payload = payload_pb2.TransactionPayload(
            payload_type=payload_pb2.TransactionPayload.ATTEND_PROCEDURES,
            attend_procedures=procedures)

        batch, signature = self._create_txn_and_batch(txn_key, BATCH_KEY, [claim_hex, event_hex, clinic_hex],
                                                      [event_hex], payload)

        batch_list = batch_pb2.BatchList(batches=[batch])

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=80)

    def eat_pills(self, txn_key, claim_id):
        clinic_pkey = txn_key.get_public_key().as_hex()
        clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)
        claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=clinic_pkey)
        current_times_str = str(time.time())
        event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=clinic_pkey, event_time=current_times_str)

        pills = payload_pb2.ActionOnClaim(
            claim_id=claim_id,
            clinic_pkey=clinic_pkey,
            description="Eat pills in scope of claim: {}".format(claim_hex),
            event_time=current_times_str
        )

        payload = payload_pb2.TransactionPayload(
            payload_type=payload_pb2.TransactionPayload.EAT_PILLS,
            eat_pills=pills)

        batch, signature = self._create_txn_and_batch(txn_key, BATCH_KEY, [claim_hex, event_hex, clinic_hex],
                                                      [event_hex], payload)

        batch_list = batch_pb2.BatchList(batches=[batch])

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=80)

    def next_visit(self, txn_key, claim_id, doctor_pkey):
        clinic_pkey = txn_key.get_public_key().as_hex()
        clinic_hex = helper.make_clinic_address(clinic_pkey=clinic_pkey)
        claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=clinic_pkey)
        current_times_str = str(time.time())
        event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=clinic_pkey, event_time=current_times_str)

        next_visit = payload_pb2.ActionOnClaim(
            claim_id=claim_id,
            clinic_pkey=clinic_pkey,
            description="Doctor: {}, completed next visit for claim: {}".format(doctor_pkey, claim_hex),
            event_time=current_times_str
        )

        payload = payload_pb2.TransactionPayload(
            payload_type=payload_pb2.TransactionPayload.NEXT_VISIT,
            next_visit=next_visit)

        batch, signature = self._create_txn_and_batch(txn_key, BATCH_KEY, [claim_hex, event_hex, clinic_hex],
                                                      [event_hex], payload)

        batch_list = batch_pb2.BatchList(batches=[batch])

        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=80)

    def list_claims(self):
        claim_list_prefix = helper.make_claim_list_address()
        return self._client.list_state(subtree=claim_list_prefix)

    def list_doctors(self):
        doctor_list_prefix = helper.make_doctor_list_address()
        return self._client.list_state(subtree=doctor_list_prefix)

    def list_patients(self):
        patient_list_prefix = helper.make_patient_list_address()
        return self._client.list_state(subtree=patient_list_prefix)

    def list_clinics(self):
        clinic_list_prefix = helper.make_clinic_list_address()
        return self._client.list_state(subtree=clinic_list_prefix)

    def list_claim_details(self, claim_id, clinic_pkey):
        claim_details_prefix = helper.make_event_list_address(claim_id=claim_id, clinic_pkey=clinic_pkey)
        return self._client.list_state(subtree=claim_details_prefix)

    def _create_txn_and_batch(self, txn_key, batch_key, inputs, outputs, payload):
        txn_header_bytes, signature = self._transaction_header(txn_key, batch_key, inputs, outputs, payload)

        txn = Transaction(
            header=txn_header_bytes,
            header_signature=signature,
            payload=payload.SerializeToString()
        )

        transactions = [txn]

        batch_header_bytes, signature = self._batch_header(batch_key, transactions)

        batch = Batch(
            header=batch_header_bytes,
            header_signature=signature,
            transactions=transactions
        )
        return batch, signature

    @staticmethod
    def _transaction_header(txn_key, batch_key, inputs, outputs, payload):
        txn_header_bytes = TransactionHeader(
            family_name=helper.TP_FAMILYNAME,
            family_version=helper.TP_VERSION,
            inputs=inputs,
            outputs=outputs,
            signer_public_key=txn_key.get_public_key().as_hex(),  # signer.get_public_key().as_hex(),
            # In this example, we're signing the batch with the same private key,
            # but the batch can be signed by another party, in which case, the
            # public key will need to be associated with that key.
            batcher_public_key=batch_key.get_public_key().as_hex(),  # signer.get_public_key().as_hex(),
            # In this example, there are no dependencies.  This list should include
            # an previous transaction header signatures that must be applied for
            # this transaction to successfully commit.
            # For example,
            # dependencies=['540a6803971d1880ec73a96cb97815a95d374cbad5d865925e5aa0432fcf1931539afe10310c122c5eaae15df61236079abbf4f258889359c4d175516934484a'],
            dependencies=[],
            nonce=random.random().hex().encode(),
            payload_sha512=hashlib.sha512(payload.SerializeToString()).hexdigest()
        ).SerializeToString()

        signature = txn_key.sign(txn_header_bytes)
        return txn_header_bytes, signature

    @staticmethod
    def _batch_header(batch_key, transactions):
        batch_header_bytes = BatchHeader(
            signer_public_key=batch_key.get_public_key().as_hex(),
            transaction_ids=[txn.header_signature for txn in transactions]
        ).SerializeToString()

        signature = batch_key.sign(batch_header_bytes)

        return batch_header_bytes, signature


def wait_until_status(url, status_code=200, tries=5):
    """Pause the program until the given url returns the required status.
    Args:
        url (str): The url to query.
        status_code (int, optional): The required status code. Defaults to 200.
        tries (int, optional): The number of attempts to request the url for
            the given status. Defaults to 5.
    Raises:
        AssertionError: If the status is not received in the given number of
            tries.
    """
    attempts = tries
    while attempts > 0:
        try:
            response = urlopen(url)
            if response.getcode() == status_code:
                return

        except HTTPError as err:
            if err.code == status_code:
                return

            LOGGER.debug('failed to read url: %s', str(err))
        except URLError as err:
            LOGGER.debug('failed to read url: %s', str(err))

        sleep_time = (tries - attempts + 1) * 2
        LOGGER.debug('Retrying in %s secs', sleep_time)
        time.sleep(sleep_time)

        attempts -= 1

    raise AssertionError(
        "{} is not available within {} attempts".format(url, tries))


def wait_for_rest_apis(endpoints, tries=5):
    """Pause the program until all the given REST API endpoints are available.
    Args:
        endpoints (list of str): A list of host:port strings.
        tries (int, optional): The number of attempts to request the url for
            availability.
    """
    for endpoint in endpoints:
        http = 'http://'
        url = endpoint if endpoint.startswith(http) else http + endpoint
        wait_until_status(
            '{}/blocks'.format(url),
            status_code=200,
            tries=tries)
