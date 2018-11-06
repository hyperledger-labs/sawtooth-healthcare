from common import helper
from common.protobuf import payload_pb2


class HealthCareState(object):
    TIMEOUT = 3

    def __init__(self, context):
        """Constructor.
        Args:
            context (sawtooth_sdk.processor.context.Context): Access to
                validator state from within the transaction processor.
        """

        self._context = context

    def create_clinic(self, public_key, name):
        op = self._load_clinic(public_key=public_key)

        if op is None:
            self._store_clinic(public_key, name)

    def create_doctor(self, public_key, name, surname):
        op = self._load_doctor(public_key=public_key)

        if op is None:
            self._store_doctor(public_key, name, surname)

    def create_patient(self, public_key, name, surname):
        op = self._load_patient(public_key=public_key)

        if op is None:
            self._store_patient(public_key, name, surname)

    def create_claim(self, claim_id, clinic_pkey, patient_pkey):
        od = self._load_claim(clinic_pkey=clinic_pkey, claim_id=claim_id)

        if od is None:
            self._store_claim(clinic_pkey=clinic_pkey, claim_id=claim_id,
                              patient_pkey=patient_pkey)

    def assign_doctor(self, claim_id, clinic_pkey, description, event_time):
        self._store_event(claim_id=claim_id, clinic_pkey=clinic_pkey, description=description,
                          event_time=event_time, event=payload_pb2.ActionOnClaim.ASSIGN)

    def first_visit(self, claim_id, clinic_pkey, description, event_time):
        self._store_event(claim_id=claim_id, clinic_pkey=clinic_pkey, description=description,
                          event_time=event_time, event=payload_pb2.ActionOnClaim.FIRST_VISIT)

    def pass_tests(self, claim_id, clinic_pkey, description, event_time):
        self._store_event(claim_id=claim_id, clinic_pkey=clinic_pkey, description=description,
                          event_time=event_time, event=payload_pb2.ActionOnClaim.PASS_TEST)

    def attend_procedures(self, claim_id, clinic_pkey, description, event_time):
        self._store_event(claim_id=claim_id, clinic_pkey=clinic_pkey, description=description,
                          event_time=event_time, event=payload_pb2.ActionOnClaim.PASS_PROCEDURE)

    def eat_pills(self, claim_id, clinic_pkey, description, event_time):
        self._store_event(claim_id=claim_id, clinic_pkey=clinic_pkey, description=description,
                          event_time=event_time, event=payload_pb2.ActionOnClaim.EAT_PILLS)

    def next_visit(self, claim_id, clinic_pkey, description, event_time):
        self._store_event(claim_id=claim_id, clinic_pkey=clinic_pkey, description=description,
                          event_time=event_time, event=payload_pb2.ActionOnClaim.NEXT_VISIT)

    def get_clinic(self, public_key):
        clinic = self._load_clinic(public_key=public_key)
        return clinic

    def get_doctor(self, public_key):
        doctor = self._load_doctor(public_key=public_key)
        return doctor

    def get_patient(self, public_key):
        patient = self._load_patient(public_key=public_key)
        return patient

    def get_claim(self, claim_id, clinic_pkey):
        od = self._load_claim(claim_id=claim_id, clinic_pkey=clinic_pkey)
        return od

    def get_claim_hex(self, claim_hex):
        claim_hex = self._load_claim_hex(claim_hex=claim_hex)
        return claim_hex

    def get_clinics(self):
        clinic = self._load_clinic()
        return clinic

    def get_doctors(self):
        doctors = self._load_doctor()
        return doctors

    def get_patients(self):
        patient = self._load_patient()
        return patient

    def _load_clinic(self, public_key=None):
        clinic = None
        clinic_hex = [] if public_key is None else [helper.make_clinic_address(public_key)]
        state_entries = self._context.get_state(
            clinic_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            clinic = payload_pb2.CreateClinic()
            clinic.ParseFromString(state_entries[0].data)
        return clinic

    def _load_doctor(self, public_key=None):
        doctor = None
        doctor_hex = [] if public_key is None else [helper.make_doctor_address(public_key)]
        state_entries = self._context.get_state(
            doctor_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            doctor = payload_pb2.CreateDoctor()
            doctor.ParseFromString(state_entries[0].data)
        return doctor

    def _load_patient(self, public_key=None):
        patient = None
        patient_hex = [] if public_key is None else [helper.make_patient_address(public_key)]
        state_entries = self._context.get_state(
            patient_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            patient = payload_pb2.CreatePatient()
            patient.ParseFromString(state_entries[0].data)
        return patient

    def _load_claim_hex(self, claim_hex):
        claim = None
        state_entries = self._context.get_state(
            [claim_hex],
            timeout=self.TIMEOUT)
        if state_entries:
            claim = payload_pb2.CreateClaim()
            claim.ParseFromString(state_entries[0].data)
        return claim

    def _load_claim(self, claim_id, clinic_pkey):
        claim = None
        claim_hex = [] if clinic_pkey is None and claim_id is None \
            else [helper.make_claim_address(claim_id, clinic_pkey)]
        state_entries = self._context.get_state(
            claim_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            claim = payload_pb2.CreateClaim()
            claim.ParseFromString(state_entries[0].data)
        return claim

    def _store_clinic(self, public_key, name):
        address = helper.make_clinic_address(public_key)

        clinic = payload_pb2.CreateClinic()
        clinic.public_key = public_key
        clinic.name = name

        state_data = clinic.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    def _store_doctor(self, public_key, name, surname):
        address = helper.make_doctor_address(public_key)

        doctor = payload_pb2.CreateDoctor()
        doctor.public_key = public_key
        doctor.name = name
        doctor.surname = surname

        state_data = doctor.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    def _store_patient(self, public_key, name, surname):
        address = helper.make_patient_address(public_key)

        patient = payload_pb2.CreatePatient()
        patient.public_key = public_key
        patient.name = name
        patient.surname = surname

        state_data = patient.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    def _store_claim(self, claim_id, clinic_pkey, patient_pkey):
        claim_hex = helper.make_claim_address(claim_id, clinic_pkey)
        claim = payload_pb2.CreateClaim()
        claim.claim_id = claim_id
        claim.clinic_pkey = clinic_pkey
        claim.patient_pkey = patient_pkey

        state_data = claim.SerializeToString()
        self._context.set_state(
            {claim_hex: state_data},
            timeout=self.TIMEOUT)

    def _store_event(self, claim_id, clinic_pkey, description, event_time, event):
        address = helper.make_event_address(claim_id, clinic_pkey, event_time)
        ev = payload_pb2.ActionOnClaim()
        ev.claim_id = claim_id
        ev.clinic_pkey = clinic_pkey
        ev.description = description
        ev.event_time = event_time
        ev.event = event

        state_data = ev.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)
