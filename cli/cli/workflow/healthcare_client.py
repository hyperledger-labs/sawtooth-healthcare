import base64
import time

import requests
import yaml
from sawtooth_sdk.protobuf import batch_pb2, transaction_pb2
from sawtooth_signing import ParseError, CryptoFactory, create_context
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from cli.common import transaction
from cli.common import helper
from cli.common.protobuf import payload_pb2
from cli.common.exceptions import HealthCareException


class HealthCareClient:

    def __init__(self, base_url, keyfile=None):

        self._base_url = base_url

        if keyfile is None:
            self._signer = None
            return

        try:
            with open(keyfile) as fd:
                private_key_str = fd.read().strip()
        except OSError as err:
            raise HealthCareException(
                'Failed to read private key {}: {}'.format(
                    keyfile, str(err)))

        try:
            private_key = Secp256k1PrivateKey.from_hex(private_key_str)
        except ParseError as e:
            raise HealthCareException(
                'Unable to load private key: {}'.format(str(e)))

        self._signer = CryptoFactory(create_context('secp256k1')) \
            .new_signer(private_key)

    def create_clinic(self, name, wait=None, auth_user=None, auth_password=None):

        batch, batch_id = transaction.create_clinic(
            txn_signer=self._signer,
            batch_signer=self._signer,
            name=name)

        batch_list = batch_pb2.BatchList(batches=[batch])
        # inputs = outputs = helper.make_clinic_address(clinic_pkey=txn_key)
        #
        # clinic = payload_pb2.CreateClinic(
        #     public_key=txn_key,
        #     name=name)
        #
        # payload = payload_pb2.TransactionPayload(
        #     payload_type=payload_pb2.TransactionPayload.CREATE_CLINIC,
        #     create_clinic=clinic)
        #
        # return self._send_healthcare_txn(txn_key, batch_key, [inputs], [outputs], payload,
        #                                  wait=wait,
        #                                  auth_user=auth_user,
        #                                  auth_password=auth_password)

        return self._send_batches(batch_list=batch_list,
                                  batch_id=batch_id,
                                  wait=wait,
                                  auth_user=auth_user,
                                  auth_password=auth_password)

    # def create_clinic(self, name, wait=None, auth_user=None, auth_password=None):
    #     batch_key = txn_key = self._signer.get_public_key().as_hex()
    #
    #     address = helper.make_clinic_address(clinic_pkey=txn_key)
    #
    #     clinic = payload_pb2.CreateClinic(
    #         public_key=txn_key,
    #         name=name)
    #
    #     payload = payload_pb2.TransactionPayload(
    #         payload_type=payload_pb2.TransactionPayload.CREATE_CLINIC,
    #         create_clinic=clinic)
    #
    #     return self._send_healthcare_txn(txn_key, batch_key, [address], [address], payload,
    #                                      wait=wait,
    #                                      auth_user=auth_user,
    #                                      auth_password=auth_password)

    def create_doctor(self, name, surname, wait=None, auth_user=None, auth_password=None):
        # batch_key = txn_key = self._signer.get_public_key().as_hex()
        #
        # address = helper.make_doctor_address(doctor_pkey=txn_key)
        #
        # doctor = payload_pb2.CreateDoctor(
        #     public_key=txn_key,
        #     name=name,
        #     surname=surname)
        #
        # payload = payload_pb2.TransactionPayload(
        #     payload_type=payload_pb2.TransactionPayload.CREATE_DOCTOR,
        #     create_doctor=doctor)
        #
        # return self._send_healthcare_txn(txn_key, batch_key, [address], [address], payload,
        #                                  wait=wait,
        #                                  auth_user=auth_user,
        #                                  auth_password=auth_password)
        batch, batch_id = transaction.create_doctor(
            txn_signer=self._signer,
            batch_signer=self._signer,
            name=name,
            surname=surname)

        batch_list = batch_pb2.BatchList(batches=[batch])

        return self._send_batches(batch_list=batch_list,
                                  batch_id=batch_id,
                                  wait=wait,
                                  auth_user=auth_user,
                                  auth_password=auth_password)

    def create_patient(self, name, surname, wait=None, auth_user=None, auth_password=None):
        # batch_key = txn_key = self._signer.get_public_key().as_hex()
        #
        # address = helper.make_patient_address(patient_pkey=txn_key)
        #
        # patient = payload_pb2.CreatePatient(
        #     public_key=txn_key,
        #     name=name,
        #     surname=surname)
        #
        # payload = payload_pb2.TransactionPayload(
        #     payload_type=payload_pb2.TransactionPayload.CREATE_PATIENT,
        #     create_patient=patient)
        #
        # return self._send_healthcare_txn(txn_key, batch_key, [address], [address], payload,
        #                                  wait=wait,
        #                                  auth_user=auth_user,
        #                                  auth_password=auth_password)

        batch, batch_id = transaction.create_patient(
            txn_signer=self._signer,
            batch_signer=self._signer,
            name=name,
            surname=surname)

        batch_list = batch_pb2.BatchList(batches=[batch])

        return self._send_batches(batch_list=batch_list,
                                  batch_id=batch_id,
                                  wait=wait,
                                  auth_user=auth_user,
                                  auth_password=auth_password)

    def add_claim(self, claim_id, patient_pkey, wait=None, auth_user=None,
                  auth_password=None):
        # batch_key = txn_key = self._signer.get_public_key().as_hex()
        #
        # clinic_hex = helper.make_clinic_address(clinic_pkey=txn_key)
        # claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=txn_key)
        #
        # claim = payload_pb2.CreateClaim(
        #     claim_id=claim_id,
        #     clinic_pkey=txn_key,
        #     patient_pkey=patient_pkey,
        # )
        #
        # payload = payload_pb2.TransactionPayload(
        #     payload_type=payload_pb2.TransactionPayload.CREATE_CLAIM,
        #     create_claim=claim)
        #
        # return self._send_healthcare_txn(txn_key, batch_key, [claim_hex, clinic_hex], [claim_hex], payload,
        #                                  wait=wait,
        #                                  auth_user=auth_user,
        #                                  auth_password=auth_password)
        batch, batch_id = transaction.register_claim(
            txn_signer=self._signer,
            batch_signer=self._signer,
            claim_id=claim_id,
            patient_pkey=patient_pkey)

        batch_list = batch_pb2.BatchList(batches=[batch])

        return self._send_batches(batch_list=batch_list,
                                  batch_id=batch_id,
                                  wait=wait,
                                  auth_user=auth_user,
                                  auth_password=auth_password)

    def assign_doctor(self, claim_id, doctor_pkey, wait=None, auth_user=None,
                      auth_password=None):
        # batch_key = txn_key = self._signer.get_public_key().as_hex()
        #
        # clinic_hex = helper.make_clinic_address(clinic_pkey=txn_key)
        # claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=txn_key)
        # current_times_str = str(time.time())
        # event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=txn_key, event_time=current_times_str)
        #
        # assign = payload_pb2.ActionOnClaim(
        #     claim_id=claim_id,
        #     clinic_pkey=txn_key,
        #     description="Doctor pkey: {}, assigned to claim: {}".format(doctor_pkey, claim_hex),
        #     event_time=current_times_str)
        #
        # payload = payload_pb2.TransactionPayload(
        #     payload_type=payload_pb2.TransactionPayload.ASSIGN_DOCTOR,
        #     assign_doctor=assign)
        #
        # return self._send_healthcare_txn(txn_key, batch_key, [claim_hex, event_hex, clinic_hex], [event_hex], payload,
        #                                  wait=wait,
        #                                  auth_user=auth_user,
        #                                  auth_password=auth_password)
        current_times_str = str(time.time())

        batch, batch_id = transaction.assign_doctor(
            txn_signer=self._signer,
            batch_signer=self._signer,
            claim_id=claim_id,
            description="Doctor pkey: {}, assigned to claim: {}".format(doctor_pkey, claim_id),
            event_time=current_times_str)

        batch_list = batch_pb2.BatchList(batches=[batch])

        return self._send_batches(batch_list=batch_list,
                                  batch_id=batch_id,
                                  wait=wait,
                                  auth_user=auth_user,
                                  auth_password=auth_password)

    def first_visit(self, claim_id, description, doctor_pkey, wait=None, auth_user=None,
                    auth_password=None):
        # batch_key = txn_key = self._signer.get_public_key().as_hex()
        #
        # clinic_hex = helper.make_clinic_address(clinic_pkey=txn_key)
        # claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=txn_key)
        # current_times_str = str(time.time())
        # event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=txn_key, event_time=current_times_str)
        #
        # first_visit = payload_pb2.ActionOnClaim(
        #     claim_id=claim_id,
        #     clinic_pkey=txn_key,
        #     description="Doctor pkey: {}, claim hex: {}, description: {}".format(doctor_pkey, claim_hex, description),
        #     event_time=current_times_str)
        #
        # payload = payload_pb2.TransactionPayload(
        #     payload_type=payload_pb2.TransactionPayload.FIRST_VISIT,
        #     first_visit=first_visit)
        #
        # return self._send_healthcare_txn(txn_key, batch_key, [claim_hex, event_hex, clinic_hex], [event_hex], payload,
        #                                  wait=wait,
        #                                  auth_user=auth_user,
        #                                  auth_password=auth_password)

        current_times_str = str(time.time())

        batch, batch_id = transaction.first_visit(
            txn_signer=self._signer,
            batch_signer=self._signer,
            claim_id=claim_id,
            description="Doctor pkey: {}, claim hex: {}, description: {}".format(doctor_pkey, claim_id, description),
            event_time=current_times_str)

        batch_list = batch_pb2.BatchList(batches=[batch])

        return self._send_batches(batch_list=batch_list,
                                  batch_id=batch_id,
                                  wait=wait,
                                  auth_user=auth_user,
                                  auth_password=auth_password)

    def pass_tests(self, claim_id, description, wait=None, auth_user=None,
                   auth_password=None):
        # batch_key = txn_key = self._signer.get_public_key().as_hex()
        #
        # clinic_hex = helper.make_clinic_address(clinic_pkey=txn_key)
        # claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=txn_key)
        # current_times_str = str(time.time())
        # event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=txn_key, event_time=current_times_str)
        #
        # pass_tests = payload_pb2.ActionOnClaim(
        #     claim_id=claim_id,
        #     clinic_pkey=txn_key,
        #     description=description,
        #     event_time=current_times_str)
        #
        # payload = payload_pb2.TransactionPayload(
        #     payload_type=payload_pb2.TransactionPayload.PASS_TESTS,
        #     pass_tests=pass_tests)
        #
        # return self._send_healthcare_txn(txn_key, batch_key, [claim_hex, event_hex, clinic_hex], [event_hex], payload,
        #                                  wait=wait,
        #                                  auth_user=auth_user,
        #                                  auth_password=auth_password)

        current_times_str = str(time.time())

        batch, batch_id = transaction.pass_tests(
            txn_signer=self._signer,
            batch_signer=self._signer,
            claim_id=claim_id,
            description=description,
            event_time=current_times_str)

        batch_list = batch_pb2.BatchList(batches=[batch])

        return self._send_batches(batch_list=batch_list,
                                  batch_id=batch_id,
                                  wait=wait,
                                  auth_user=auth_user,
                                  auth_password=auth_password)

    def attend_procedures(self, claim_id, description, wait=None, auth_user=None,
                          auth_password=None):
        # batch_key = txn_key = self._signer.get_public_key().as_hex()
        #
        # clinic_hex = helper.make_clinic_address(clinic_pkey=txn_key)
        # claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=txn_key)
        # current_times_str = str(time.time())
        # event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=txn_key, event_time=current_times_str)
        #
        # attend_procedures = payload_pb2.ActionOnClaim(
        #     claim_id=claim_id,
        #     clinic_pkey=txn_key,
        #     description=description,
        #     event_time=current_times_str)
        #
        # payload = payload_pb2.TransactionPayload(
        #     payload_type=payload_pb2.TransactionPayload.ATTEND_PROCEDURES,
        #     attend_procedures=attend_procedures)
        #
        # return self._send_healthcare_txn(txn_key, batch_key, [claim_hex, event_hex, clinic_hex], [event_hex], payload,
        #                                  wait=wait,
        #                                  auth_user=auth_user,
        #                                  auth_password=auth_password)

        current_times_str = str(time.time())

        batch, batch_id = transaction.attend_procedures(
            txn_signer=self._signer,
            batch_signer=self._signer,
            claim_id=claim_id,
            description=description,
            event_time=current_times_str)

        batch_list = batch_pb2.BatchList(batches=[batch])

        return self._send_batches(batch_list=batch_list,
                                  batch_id=batch_id,
                                  wait=wait,
                                  auth_user=auth_user,
                                  auth_password=auth_password)

    def eat_pills(self, claim_id, description, wait=None, auth_user=None,
                  auth_password=None):
        # batch_key = txn_key = self._signer.get_public_key().as_hex()
        #
        # clinic_hex = helper.make_clinic_address(clinic_pkey=txn_key)
        # address = helper.make_claim_address(claim_id=claim_id, clinic_pkey=txn_key)
        # current_times_str = str(time.time())
        # event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=txn_key, event_time=current_times_str)
        #
        # eat_pills = payload_pb2.ActionOnClaim(
        #     claim_id=claim_id,
        #     clinic_pkey=txn_key,
        #     description=description,
        #     event_time=current_times_str)
        #
        # payload = payload_pb2.TransactionPayload(
        #     payload_type=payload_pb2.TransactionPayload.EAT_PILLS,
        #     eat_pills=eat_pills)
        #
        # return self._send_healthcare_txn(txn_key, batch_key, [address, event_hex, clinic_hex], [event_hex], payload,
        #                                  wait=wait,
        #                                  auth_user=auth_user,
        #                                  auth_password=auth_password)

        current_times_str = str(time.time())

        batch, batch_id = transaction.eat_pills(
            txn_signer=self._signer,
            batch_signer=self._signer,
            claim_id=claim_id,
            description=description,
            event_time=current_times_str)

        batch_list = batch_pb2.BatchList(batches=[batch])

        return self._send_batches(batch_list=batch_list,
                                  batch_id=batch_id,
                                  wait=wait,
                                  auth_user=auth_user,
                                  auth_password=auth_password)

    def next_visit(self, claim_id, description, doctor_pkey, wait=None, auth_user=None,
                   auth_password=None):
        # batch_key = txn_key = self._signer.get_public_key().as_hex()
        #
        # clinic_hex = helper.make_clinic_address(clinic_pkey=txn_key)
        # claim_hex = helper.make_claim_address(claim_id=claim_id, clinic_pkey=txn_key)
        # current_times_str = str(time.time())
        # event_hex = helper.make_event_address(claim_id=claim_id, clinic_pkey=txn_key, event_time=current_times_str)
        #
        # next_visit = payload_pb2.ActionOnClaim(
        #     claim_id=claim_id,
        #     clinic_pkey=txn_key,
        #     description="Doctor pkey: {}, claim hex: {}, description: {}".format(doctor_pkey, claim_hex, description),
        #     event_time=current_times_str)
        #
        # payload = payload_pb2.TransactionPayload(
        #     payload_type=payload_pb2.TransactionPayload.NEXT_VISIT,
        #     next_visit=next_visit)
        #
        # return self._send_healthcare_txn(txn_key, batch_key, [claim_hex, event_hex, clinic_hex], [event_hex], payload,
        #                                  wait=wait,
        #                                  auth_user=auth_user,
        #                                  auth_password=auth_password)

        current_times_str = str(time.time())

        batch, batch_id = transaction.next_visit(
            txn_signer=self._signer,
            batch_signer=self._signer,
            claim_id=claim_id,
            description="Doctor pkey: {}, claim hex: {}, description: {}".format(doctor_pkey, claim_id, description),
            event_time=current_times_str)

        batch_list = batch_pb2.BatchList(batches=[batch])

        return self._send_batches(batch_list=batch_list,
                                  batch_id=batch_id,
                                  wait=wait,
                                  auth_user=auth_user,
                                  auth_password=auth_password)

    def list_claims(self, auth_user=None, auth_password=None):
        claim_list_prefix = helper.make_claim_list_address()

        result = self._send_request(
            "state?address={}".format(claim_list_prefix),
            auth_user=auth_user,
            auth_password=auth_password)
        orders = {}

        try:
            data = yaml.safe_load(result)["data"]
            if data is not None:
                for value in data:
                    dec_ord = base64.b64decode(value["data"])
                    o = payload_pb2.CreateClaim()
                    o.ParseFromString(dec_ord)
                    orders[value["address"]] = o

        except BaseException:
            pass

        return orders

    def list_patients(self, auth_user=None, auth_password=None):
        patient_list_prefix = helper.make_patient_list_address()

        result = self._send_request(
            "state?address={}".format(patient_list_prefix),
            auth_user=auth_user,
            auth_password=auth_password)
        patients = {}

        try:
            data = yaml.safe_load(result)["data"]
            if data is not None:
                for value in data:
                    dec_pt = base64.b64decode(value["data"])
                    pt = payload_pb2.CreatePatient()
                    pt.ParseFromString(dec_pt)
                    patients[value["address"]] = pt

        except BaseException:
            pass

        return patients

    def list_clinics(self, auth_user=None, auth_password=None):
        operator_list_prefix = helper.make_clinic_list_address()

        result = self._send_request(
            "state?address={}".format(operator_list_prefix),
            auth_user=auth_user,
            auth_password=auth_password)
        clinics = {}

        try:
            data = yaml.safe_load(result)["data"]
            if data is not None:
                for value in data:
                    dec_cl = base64.b64decode(value["data"])
                    cl = payload_pb2.CreateClinic()
                    cl.ParseFromString(dec_cl)
                    clinics[value["address"]] = cl

        except BaseException:
            pass

        return clinics

    def list_doctors(self, auth_user=None, auth_password=None):
        doctor_list_prefix = helper.make_doctor_list_address()

        result = self._send_request(
            "state?address={}".format(doctor_list_prefix),
            auth_user=auth_user,
            auth_password=auth_password)
        doctors = []

        try:
            data = yaml.safe_load(result)["data"]
            if data is not None:
                for value in data:
                    dec_dc = base64.b64decode(value["data"])
                    dc = payload_pb2.CreateDoctor()
                    dc.ParseFromString(dec_dc)
                    doctors.append(dc)

        except BaseException:
            pass

        return doctors

    def list_claim_details(self, claim_id, clinic_hex, auth_user=None, auth_password=None):
        claim_details_prefix = helper.make_event_list_address(claim_id=claim_id, clinic_pkey=clinic_hex)

        result = self._send_request(
            "state?address={}".format(claim_details_prefix),
            auth_user=auth_user,
            auth_password=auth_password)
        orders = {}

        try:
            data = yaml.safe_load(result)["data"]
            if data is not None:
                for value in data:
                    dec_ord = base64.b64decode(value["data"])
                    o = payload_pb2.ActionOnClaim()
                    o.ParseFromString(dec_ord)
                    orders[value["address"]] = o

        except BaseException:
            pass

        return orders

    def _send_request(self,
                      suffix,
                      data=None,
                      content_type=None,
                      name=None,
                      auth_user=None,
                      auth_password=None):
        if self._base_url.startswith("http://"):
            url = "{}/{}".format(self._base_url, suffix)
        else:
            url = "http://{}/{}".format(self._base_url, suffix)

        headers = {}
        if auth_user is not None:
            auth_string = "{}:{}".format(auth_user, auth_password)
            b64_string = base64.b64encode(auth_string.encode()).decode()
            auth_header = 'Basic {}'.format(b64_string)
            headers['Authorization'] = auth_header

        if content_type is not None:
            headers['Content-Type'] = content_type

        try:
            if data is not None:
                result = requests.post(url, headers=headers, data=data)
            else:
                result = requests.get(url, headers=headers)

            if result.status_code == 404:
                raise HealthCareException("No such operator: {}".format(name))

            elif not result.ok:
                raise HealthCareException("Error {}: {}".format(
                    result.status_code, result.reason))

        except requests.ConnectionError as err:
            raise HealthCareException(
                'Failed to connect to {}: {}'.format(url, str(err)))

        except BaseException as err:
            raise HealthCareException(err)

        return result.text

    def _send_batches(self, batch_list, batch_id, wait, auth_user, auth_password):
        if wait and wait > 0:
            wait_time = 0
            start_time = time.time()
            response = self._send_request(
                "batches", batch_list.SerializeToString(),
                'application/octet-stream',
                auth_user=auth_user,
                auth_password=auth_password)
            while wait_time < wait:
                status = self._get_status(
                    batch_id,
                    wait - int(wait_time),
                    auth_user=auth_user,
                    auth_password=auth_password)
                wait_time = time.time() - start_time

                if status != 'PENDING':
                    return response

            return response

        return self._send_request(
            "batches", batch_list.SerializeToString(),
            'application/octet-stream',
            auth_user=auth_user,
            auth_password=auth_password)

    # def _send_healthcare_txn(self, txn_key, batch_key, inputs, outputs, payload, wait,
    #                          auth_user, auth_password):
    #
    #     txn_header_bytes, signature = self._transaction_header(txn_key, inputs, outputs, payload)
    #
    #     txn = Transaction(
    #         header=txn_header_bytes,
    #         header_signature=signature,
    #         payload=payload.SerializeToString()
    #     )
    #
    #     transactions = [txn]
    #
    #     batch_header_bytes, signature = self._batch_header(batch_key, transactions)
    #
    #     batch = Batch(
    #         header=batch_header_bytes,
    #         header_signature=signature,
    #         transactions=transactions
    #     )
    #
    #     batch_list = BatchList(batches=[batch])
    #     batch_id = batch_list.batches[0].header_signature
    #
    #     if wait and wait > 0:
    #         wait_time = 0
    #         start_time = time.time()
    #         response = self._send_request(
    #             "batches", batch_list.SerializeToString(),
    #             'application/octet-stream',
    #             auth_user=auth_user,
    #             auth_password=auth_password)
    #         while wait_time < wait:
    #             status = self._get_status(
    #                 batch_id,
    #                 wait - int(wait_time),
    #                 auth_user=auth_user,
    #                 auth_password=auth_password)
    #             wait_time = time.time() - start_time
    #
    #             if status != 'PENDING':
    #                 return response
    #
    #         return response
    #
    #     return self._send_request(
    #         "batches", batch_list.SerializeToString(),
    #         'application/octet-stream',
    #         auth_user=auth_user,
    #         auth_password=auth_password)

    def _get_status(self, batch_id, wait, auth_user=None, auth_password=None):
        try:
            result = self._send_request(
                'batch_statuses?id={}&wait={}'.format(batch_id, wait),
                auth_user=auth_user,
                auth_password=auth_password)
            return yaml.safe_load(result)['data'][0]['status']
        except BaseException as err:
            raise HealthCareException(err)

    # def _transaction_header(self, txn_key, inputs, outputs, payload):
    #     txn_header_bytes = TransactionHeader(
    #         family_name=helper.TP_FAMILYNAME,
    #         family_version=helper.TP_VERSION,
    #         inputs=inputs,
    #         outputs=outputs,
    #         signer_public_key=txn_key,  # signer.get_public_key().as_hex(),
    #         # In this example, we're signing the batch with the same private key,
    #         # but the batch can be signed by another party, in which case, the
    #         # public key will need to be associated with that key.
    #         batcher_public_key=txn_key,  # signer.get_public_key().as_hex(),
    #         # In this example, there are no dependencies.  This list should include
    #         # an previous transaction header signatures that must be applied for
    #         # this transaction to successfully commit.
    #         # For example,
    #         # dependencies=['540a6803971d1880ec73a96cb97815a95d374cbad5d865925e5aa0432fcf1931539afe10310c122c5eaae15df61236079abbf4f258889359c4d175516934484a'],
    #         dependencies=[],
    #         nonce=random.random().hex().encode(),
    #         payload_sha512=hashlib.sha512(payload.SerializeToString()).hexdigest()
    #     ).SerializeToString()
    #
    #     signature = self._signer.sign(txn_header_bytes)
    #     return txn_header_bytes, signature
    #
    # def _batch_header(self, batch_key, transactions):
    #     batch_header_bytes = BatchHeader(
    #         signer_public_key=batch_key,
    #         transaction_ids=[txn.header_signature for txn in transactions],
    #     ).SerializeToString()
    #
    #     signature = self._signer.sign(batch_header_bytes)
    #
    #     return batch_header_bytes, signature