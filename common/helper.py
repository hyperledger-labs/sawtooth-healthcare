import hashlib

DISTRIBUTION_NAME = 'sawtooth-healthcare'

DEFAULT_URL = 'http://127.0.0.1:8008'

TP_FAMILYNAME = 'healthcare'
TP_VERSION = '1.0'
CLINIC_ENTITY_NAME = 'clinic'
DOCTOR_ENTITY_NAME = 'doctor'
PATIENT_ENTITY_NAME = 'patient'
CLAIM_ENTITY_NAME = 'claim'
EVENT_ENTITY_NAME = 'event'

CLAIM_ENTITY_HEX6 = hashlib.sha512(CLAIM_ENTITY_NAME.encode("utf-8")).hexdigest()[0:6]
CLINIC_ENTITY_HEX64 = hashlib.sha512(CLINIC_ENTITY_NAME.encode("utf-8")).hexdigest()[0:64]

CLINIC_ENTITY_CODE = '01'
DOCTOR_ENTITY_CODE = '02'
PATIENT_ENTITY_CODE = '03'
CLAIM_ENTITY_CODE = '04'
EVENT_ENTITY_CODE = '05'


def _hash(identifier):
    return hashlib.sha256(identifier.encode('utf-8')).hexdigest()


TP_PREFFIX_HEX6 = _hash(TP_FAMILYNAME)[0:6]


def make_clinic_address(clinic_pkey):
    return TP_PREFFIX_HEX6 + CLINIC_ENTITY_CODE + _hash(CLINIC_ENTITY_NAME)[0:6] + _hash(clinic_pkey)[:56]


def make_clinic_list_address():
    return TP_PREFFIX_HEX6 + CLINIC_ENTITY_CODE + _hash(CLINIC_ENTITY_NAME)[0:6]


def make_doctor_address(doctor_pkey):
    return TP_PREFFIX_HEX6 + DOCTOR_ENTITY_CODE + _hash(DOCTOR_ENTITY_NAME)[0:6] + _hash(doctor_pkey)[:56]


def make_doctor_list_address():
    return TP_PREFFIX_HEX6 + DOCTOR_ENTITY_CODE + _hash(DOCTOR_ENTITY_NAME)[0:6]


def make_patient_address(patient_pkey):
    return TP_PREFFIX_HEX6 + PATIENT_ENTITY_CODE + _hash(PATIENT_ENTITY_NAME)[0:6] + _hash(patient_pkey)[:56]


def make_patient_list_address():
    return TP_PREFFIX_HEX6 + PATIENT_ENTITY_CODE + _hash(PATIENT_ENTITY_NAME)[0:6]


def make_claim_address(claim_id, clinic_pkey):
    return TP_PREFFIX_HEX6 + CLAIM_ENTITY_CODE + _hash(CLAIM_ENTITY_NAME)[0:6] + _hash(claim_id)[:6] + \
           _hash(CLINIC_ENTITY_NAME)[0:6] + _hash(clinic_pkey)[:44]


def make_claim_list_address():
    return TP_PREFFIX_HEX6 + CLAIM_ENTITY_CODE + _hash(CLAIM_ENTITY_NAME)[0:6]


def make_event_address(claim_id, clinic_pkey, event_time):
    return TP_PREFFIX_HEX6 + EVENT_ENTITY_CODE + \
           _hash(CLAIM_ENTITY_NAME)[0:6] + _hash(claim_id)[:6] + \
           _hash(CLINIC_ENTITY_NAME)[0:6] + _hash(clinic_pkey)[:6] + \
           _hash(event_time)[:38]


def make_event_list_address(claim_id, clinic_pkey):
    return TP_PREFFIX_HEX6 + EVENT_ENTITY_CODE + \
           _hash(CLAIM_ENTITY_NAME)[0:6] + _hash(claim_id)[:6] + \
           _hash(CLINIC_ENTITY_NAME)[0:6] + _hash(clinic_pkey)[:6]
