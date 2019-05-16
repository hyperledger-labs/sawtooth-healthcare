import logging

from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.handler import TransactionHandler

import common.helper as helper
from processor.workflow.payload import HealthCarePayload
from processor.workflow.state import HealthCareState

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class HealthCareTransactionHandler(TransactionHandler):
    def __init__(self, namespace_prefix):
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        return helper.TP_FAMILYNAME

    @property
    def family_versions(self):
        return [helper.TP_VERSION]

    @property
    def namespaces(self):
        return [self._namespace_prefix]

    def apply(self, transaction, context):
        try:

            _display("i'm inside handler _display")
            print("i'm inside handler print")

            header = transaction.header
            signer = header.signer_public_key

            healthcare_payload = HealthCarePayload(payload=transaction.payload)

            healthcare_state = HealthCareState(context)

            if healthcare_payload.is_create_clinic():
                clinic = healthcare_payload.create_clinic()

                cl = healthcare_state.get_clinic(clinic.public_key)
                if cl is not None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic already exists: ' + clinic.name)

                healthcare_state.create_clinic(clinic.public_key, clinic.name)
            elif healthcare_payload.is_create_doctor():
                doctor = healthcare_payload.create_doctor()

                do = healthcare_state.get_doctor(doctor.public_key)
                if do is not None:
                    raise InvalidTransaction(
                        'Invalid action: Doctor already exists: ' + doctor.name)

                healthcare_state.create_doctor(doctor.public_key, doctor.name, doctor.surname)
            elif healthcare_payload.is_create_patient():
                patient = healthcare_payload.create_patient()

                pat = healthcare_state.get_patient(patient.public_key)
                if pat is not None:
                    raise InvalidTransaction(
                        'Invalid action: Patient already exists: ' + patient.name)

                healthcare_state.create_patient(patient.public_key, patient.name, patient.surname)
            elif healthcare_payload.is_create_claim():

                claim = healthcare_payload.create_claim()

                clinic = healthcare_state.get_clinic(signer)
                if clinic is None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic does not exist: ' + signer)

                cl = healthcare_state.get_claim(claim.claim_id, claim.clinic_pkey)
                if cl is not None:
                    raise InvalidTransaction(
                        'Invalid action: Claim ' + claim.claim_id + ' already exists in clinic having ' +
                        claim.clinic_pkey + ' public key')

                pat = healthcare_state.get_patient(claim.patient_pkey)
                if pat is None:
                    raise InvalidTransaction(
                        'Invalid action: Patient having ' + claim.patient_pkey + ' public key does not exist')

                healthcare_state.create_claim(claim.claim_id, claim.clinic_pkey, claim.patient_pkey)
            elif healthcare_payload.is_assign_doctor():
                assign = healthcare_payload.assign_doctor()

                clinic = healthcare_state.get_clinic(signer)
                if clinic is None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic does not exist: ' + signer)

                cl = healthcare_state.get_claim(assign.claim_id, assign.clinic_pkey)
                if cl is None:
                    raise InvalidTransaction(
                        'Invalid action: Claim does not exist: ' + assign.claim_id + '; clinic: ' + clinic.public_key)

                healthcare_state.assign_doctor(assign.claim_id, assign.clinic_pkey, assign.description,
                                               assign.event_time)
            elif healthcare_payload.is_first_visit():
                visit = healthcare_payload.first_visit()

                clinic = healthcare_state.get_clinic(signer)
                if clinic is None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic does not exist: ' + signer)

                cl = healthcare_state.get_claim(visit.claim_id, visit.clinic_pkey)
                if cl is None:
                    raise InvalidTransaction(
                        'Invalid action: Claim does not exist: ' + visit.claim_id)

                healthcare_state.first_visit(visit.claim_id, visit.clinic_pkey,
                                             visit.description, visit.event_time)
            elif healthcare_payload.is_pass_tests():
                tests = healthcare_payload.pass_tests()

                clinic = healthcare_state.get_clinic(signer)
                if clinic is None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic does not exist: ' + signer)

                cl = healthcare_state.get_claim(tests.claim_id, tests.clinic_pkey)
                if cl is None:
                    raise InvalidTransaction(
                        'Invalid action: Claim does not exist: ' + tests.claim_id)

                healthcare_state.pass_tests(tests.claim_id, tests.clinic_pkey, tests.description, tests.event_time)
            elif healthcare_payload.is_attend_procedures():
                procedures = healthcare_payload.attend_procedures()

                clinic = healthcare_state.get_clinic(signer)
                if clinic is None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic does not exist: ' + signer)

                cl = healthcare_state.get_claim(procedures.claim_id, procedures.clinic_pkey)
                if cl is None:
                    raise InvalidTransaction(
                        'Invalid action: Claim does not exist: ' + procedures.claim_id)

                healthcare_state.attend_procedures(procedures.claim_id, procedures.clinic_pkey, procedures.description,
                                                   procedures.event_time)
            elif healthcare_payload.is_eat_pills():
                pills = healthcare_payload.eat_pills()

                clinic = healthcare_state.get_clinic(signer)
                if clinic is None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic does not exist: ' + signer)

                cl = healthcare_state.get_claim(pills.claim_id, pills.clinic_pkey)
                if cl is None:
                    raise InvalidTransaction(
                        'Invalid action: Claim does not exist: ' + pills.claim_id)

                healthcare_state.eat_pills(pills.claim_id, pills.clinic_pkey, pills.description,
                                           pills.event_time)
            elif healthcare_payload.is_next_visit():
                examination = healthcare_payload.next_visit()

                clinic = healthcare_state.get_clinic(signer)
                if clinic is None:
                    raise InvalidTransaction(
                        'Invalid action: Clinic does not exist: ' + signer)

                cl = healthcare_state.get_claim(examination.claim_id, examination.clinic_pkey)
                if cl is None:
                    raise InvalidTransaction(
                        'Invalid action: Claim does not exist: ' + examination.claim_id)

                healthcare_state.next_visit(examination.claim_id, examination.clinic_pkey,
                                            examination.description,
                                            examination.event_time)
            else:
                raise InvalidTransaction('Unhandled action: {}'.format(healthcare_payload.transaction_type()))
        except Exception as e:
            print("Error: {}".format(e))
            logging.exception(e)
            raise e


def _display(msg):
    n = msg.count("\n")

    if n > 0:
        msg = msg.split("\n")
        length = max(len(line) for line in msg)
    else:
        length = len(msg)
        msg = [msg]

    # pylint: disable=logging-not-lazy
    LOGGER.debug("+" + (length + 2) * "-" + "+")
    for line in msg:
        LOGGER.debug("+ " + line.center(length) + " +")
    LOGGER.debug("+" + (length + 2) * "-" + "+")
