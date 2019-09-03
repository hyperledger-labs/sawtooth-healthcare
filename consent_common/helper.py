import hashlib

DISTRIBUTION_NAME = 'sawtooth-consent'

DEFAULT_URL = 'http://127.0.0.1:8009'

TP_FAMILYNAME = 'consent'
TP_VERSION = '1.0'
CONSENT_ENTITY_NAME = 'consent'
DOCTOR_ENTITY_NAME = 'doctor'
PATIENT_ENTITY_NAME = 'patient'
# CLAIM_ENTITY_HEX6 = hashlib.sha512(CLAIM_ENTITY_NAME.encode("utf-8")).hexdigest()[0:6]
# CLINIC_ENTITY_HEX64 = hashlib.sha512(CLINIC_ENTITY_NAME.encode("utf-8")).hexdigest()[0:64]

CONSENT_ENTITY_CODE = '01'
DOCTOR_ENTITY_CODE = '02'
PATIENT_ENTITY_CODE = '03'
# CLAIM_ENTITY_CODE = '04'
# EVENT_ENTITY_CODE = '05'
# LAB_TEST_ENTITY_CODE = '06'
# PULSE_ENTITY_CODE = '07'


def _hash(identifier):
    return hashlib.sha512(identifier.encode('utf-8')).hexdigest()


TP_PREFFIX_HEX6 = _hash(TP_FAMILYNAME)[0:6]


def make_consent_address(doctor_pkey, patient_pkey):
    return TP_PREFFIX_HEX6 + CONSENT_ENTITY_CODE \
           + _hash(DOCTOR_ENTITY_NAME)[:6] + _hash(doctor_pkey)[:25] \
           + _hash(PATIENT_ENTITY_NAME)[:6] + _hash(patient_pkey)[:25]


def make_consent_list_address():
    return TP_PREFFIX_HEX6 + CONSENT_ENTITY_CODE


def make_consent_list_address_by_doctor(doctor_pkey):
    return TP_PREFFIX_HEX6 + CONSENT_ENTITY_CODE \
           + _hash(DOCTOR_ENTITY_NAME)[:6] + _hash(doctor_pkey)[:25]


# def make_doctor_address(doctor_pkey):
#     return TP_PREFFIX_HEX6 + DOCTOR_ENTITY_CODE + _hash(DOCTOR_ENTITY_NAME)[0:6] + _hash(doctor_pkey)[:56]
#
#
# def make_patient_address(patient_pkey):
#     return TP_PREFFIX_HEX6 + PATIENT_ENTITY_CODE + _hash(PATIENT_ENTITY_NAME)[0:6] + _hash(patient_pkey)[:56]
#
#
# def make_patient_list_address():
#     return TP_PREFFIX_HEX6 + PATIENT_ENTITY_CODE + _hash(PATIENT_ENTITY_NAME)[0:6]
#
#
# def make_claim_address(claim_id, clinic_pkey):
#     return TP_PREFFIX_HEX6 + CLAIM_ENTITY_CODE + _hash(CLAIM_ENTITY_NAME)[0:6] + _hash(claim_id)[:6] + \
#            _hash(CLINIC_ENTITY_NAME)[0:6] + _hash(clinic_pkey)[:44]
#
#
# def make_claim_list_address():
#     return TP_PREFFIX_HEX6 + CLAIM_ENTITY_CODE + _hash(CLAIM_ENTITY_NAME)[0:6]
#
#
# def make_event_address(claim_id, clinic_pkey, event_time):
#     return TP_PREFFIX_HEX6 + EVENT_ENTITY_CODE + \
#            _hash(CLAIM_ENTITY_NAME)[0:6] + _hash(claim_id)[:6] + \
#            _hash(CLINIC_ENTITY_NAME)[0:6] + _hash(clinic_pkey)[:6] + \
#            _hash(event_time)[:38]
#
#
# def make_event_list_address(claim_id, clinic_pkey):
#     return TP_PREFFIX_HEX6 + EVENT_ENTITY_CODE + \
#            _hash(CLAIM_ENTITY_NAME)[0:6] + _hash(claim_id)[:6] + \
#            _hash(CLINIC_ENTITY_NAME)[0:6] + _hash(clinic_pkey)[:6]
#
#
# def make_lab_test_address(clinic_pkey, event_time):
#     return TP_PREFFIX_HEX6 + LAB_TEST_ENTITY_CODE + \
#            _hash(LAB_TEST_ENTITY_NAME)[0:6] + _hash(clinic_pkey)[:6] + \
#            _hash(event_time)[:50]
#
#
# def make_lab_test_list_by_clinic_address(clinic_pkey):
#     return TP_PREFFIX_HEX6 + LAB_TEST_ENTITY_CODE + \
#            _hash(LAB_TEST_ENTITY_NAME)[0:6] + _hash(clinic_pkey)[:6]
#
#
# def make_lab_test_list_address():
#     return TP_PREFFIX_HEX6 + LAB_TEST_ENTITY_CODE + \
#            _hash(LAB_TEST_ENTITY_NAME)[0:6]
#
#
# def make_pulse_address(public_key, timestamp):
#     return TP_PREFFIX_HEX6 + PULSE_ENTITY_CODE + \
#             _hash(PULSE_ENTITY_NAME)[:6] + \
#             _hash(public_key)[:6] + \
#             _hash(str(timestamp))[:50]
#
#
# def make_pulse_list_by_patient_address(patient_pkey):
#     return TP_PREFFIX_HEX6 + PULSE_ENTITY_CODE + \
#             _hash(PULSE_ENTITY_NAME)[:6] + \
#             _hash(patient_pkey)[:6]
#
#
# def make_pulse_list_address():
#     return TP_PREFFIX_HEX6 + PULSE_ENTITY_CODE + \
#             _hash(PULSE_ENTITY_NAME)[0:6]
