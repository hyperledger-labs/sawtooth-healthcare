import logging

from payment_processor.payment_common import helper
# from payment_processor.payment_common.protobuf import payment_payload_pb2

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class PaymentState(object):
    TIMEOUT = 3

    def __init__(self, context):
        """Constructor.
        Args:
            context (sawtooth_sdk.processor.context.Context): Access to
                validator state from within the transaction processor.
        """

        self._context = context

    def create_payment(self, payment):
        self._store_payment(payment)

    # def revoke_access(self, doctor_pkey, patient_pkey):
    #     self._revoke_access(doctor_pkey, patient_pkey)
    #
    # def has_access(self, doctor_pkey, patient_pkey):
    #     return self._load_access(doctor_pkey=doctor_pkey, patient_pkey=patient_pkey)
    #
    # def get_access_by_doctor(self, doctor_pkey):
    #     return self._load_access_by_doctor(doctor_pkey=doctor_pkey)
    #
    # def _load_access(self, doctor_pkey, patient_pkey):
    #     access_hex = [helper.make_consent_address(dest_pkey=doctor_pkey, src_pkey=patient_pkey)]
    #     state_entries = self._context.get_state(
    #         access_hex,
    #         timeout=self.TIMEOUT)
    #     if state_entries:
    #         access = consent_payload_pb2.ActionOnAccess()
    #         access.ParseFromString(state_entries[0].data)
    #         return access
    #     return None
    #
    # def _load_access_by_doctor(self, doctor_pkey):
    #     access_hex = [helper.make_consent_list_address_by_destination_client(dest_pkey=doctor_pkey)]
    #     state_entries = self._context.get_state(
    #         access_hex,
    #         timeout=self.TIMEOUT)
    #     if state_entries:
    #         access = consent_payload_pb2.ActionOnAccess()
    #         access.ParseFromString(state_entries[0].data)
    #         return access
    #     return None

    def _store_payment(self, payment):
        payment_hex = helper.make_payment_address(payment.id)

        payment_contract_rel_hex = helper.make_payment_contract__relation_address(payment.id, payment.contract_id)
        contract_payment_rel_hex = helper.make_contract_payment__relation_address(payment.contract_id, payment.id)

        payment_patient_rel_hex = helper.make_payment_patient__relation_address(payment.id, payment.patient_pkey)
        patient_payment_rel_hex = helper.make_patient_payment__relation_address(payment.patient_pkey, payment.id)

        payment_data = payment.SerializeToString()

        states = {
            payment_hex: payment_data,
            payment_contract_rel_hex:  str.encode(payment.contract_id),
            contract_payment_rel_hex:  str.encode(payment.id),

            payment_patient_rel_hex: str.encode(payment.patient_pkey),
            patient_payment_rel_hex: str.encode(payment.id)
        }

        LOGGER.debug("_store_payment: " + str(states))
        self._context.set_state(
            states,
            timeout=self.TIMEOUT)

    # def _revoke_access(self, doctor_key, patient_pkey):
    #     address = helper.make_consent_address(dest_pkey=doctor_key, src_pkey=patient_pkey)
    #
    #     self._context.delete_state(
    #         [address],
    #         timeout=self.TIMEOUT)
    #
    # def create_client(self, client):
    #     address = helper.make_client_address(public_key=client.public_key)
    #
    #     # access = consent_payload_pb2.ActionOnAccess()
    #     # access.doctor_pkey = doctor_key
    #     # access.patient_pkey = patient_pkey
    #
    #     state_data = client.SerializeToString()
    #     self._context.set_state(
    #         {address: state_data},
    #         timeout=self.TIMEOUT)
