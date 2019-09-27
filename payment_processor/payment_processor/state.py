from payment_processor.payment_common import helper
# from payment_processor.payment_common.protobuf import payment_payload_pb2


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
        address = helper.make_payment_address(payer_pkey=payment.public_key, uid=payment.id)

        state_data = payment.SerializeToString()
        self._context.set_state(
            {address: state_data},
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
