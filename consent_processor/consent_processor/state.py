from consent_processor.consent_common import helper
from consent_processor.consent_common.protobuf import consent_payload_pb2


class ConsentState(object):
    TIMEOUT = 3

    def __init__(self, context):
        """Constructor.
        Args:
            context (sawtooth_sdk.processor.context.Context): Access to
                validator state from within the transaction processor.
        """

        self._context = context

    def grant_access(self, doctor_pkey, patient_pkey):
        self._store_access(doctor_pkey, patient_pkey)

    def revoke_access(self, doctor_pkey, patient_pkey):
        self._revoke_access(doctor_pkey, patient_pkey)

    def has_access(self, doctor_pkey, patient_pkey):
        return self._load_access(doctor_pkey=doctor_pkey, patient_pkey=patient_pkey)

    def get_access_by_doctor(self, doctor_pkey):
        return self._load_access_by_doctor(doctor_pkey=doctor_pkey)

    def _load_access(self, doctor_pkey, patient_pkey):
        access_hex = [helper.make_consent_address(doctor_pkey=doctor_pkey, patient_pkey=patient_pkey)]
        state_entries = self._context.get_state(
            access_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            access = consent_payload_pb2.ActionOnAccess()
            access.ParseFromString(state_entries[0].data)
            return access
        return None

    def _load_access_by_doctor(self, doctor_pkey):
        access_hex = [helper.make_consent_list_address_by_doctor(doctor_pkey=doctor_pkey)]
        state_entries = self._context.get_state(
            access_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            access = consent_payload_pb2.ActionOnAccess()
            access.ParseFromString(state_entries[0].data)
            return access
        return None

    def _store_access(self, doctor_key, patient_pkey):
        address = helper.make_consent_address(doctor_pkey=doctor_key, patient_pkey=patient_pkey)

        access = consent_payload_pb2.ActionOnAccess()
        access.doctor_pkey = doctor_key
        access.patient_pkey = patient_pkey

        state_data = access.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    def _revoke_access(self, doctor_key, patient_pkey):
        address = helper.make_consent_address(doctor_pkey=doctor_key, patient_pkey=patient_pkey)

        self._context.delete_state(
            [address],
            timeout=self.TIMEOUT)
