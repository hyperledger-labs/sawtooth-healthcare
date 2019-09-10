import hashlib

DISTRIBUTION_NAME = 'sawtooth-consent'

DEFAULT_URL = 'http://127.0.0.1:8009'

TP_FAMILYNAME = 'consent'
TP_VERSION = '1.0'
# CONSENT_ENTITY_NAME = 'consent'
# DOCTOR_ENTITY_NAME = 'doctor'
# PATIENT_ENTITY_NAME = 'patient'
# CLAIM_ENTITY_HEX6 = hashlib.sha512(CLAIM_ENTITY_NAME.encode("utf-8")).hexdigest()[0:6]
# CLINIC_ENTITY_HEX64 = hashlib.sha512(CLINIC_ENTITY_NAME.encode("utf-8")).hexdigest()[0:64]

CONSENT_ENTITY_CODE = '01'
CLIENT_ENTITY_CODE = '02'
# PATIENT_ENTITY_CODE = '03'
# CLAIM_ENTITY_CODE = '04'
# EVENT_ENTITY_CODE = '05'
# LAB_TEST_ENTITY_CODE = '06'
# PULSE_ENTITY_CODE = '07'


def _hash(identifier):
    return hashlib.sha512(identifier.encode('utf-8')).hexdigest()


TP_PREFFIX_HEX6 = _hash(TP_FAMILYNAME)[0:6]


def make_client_address(public_key):
    return TP_PREFFIX_HEX6 + CLIENT_ENTITY_CODE + _hash(public_key)[:62]


def make_consent_address(dest_pkey, src_pkey):
    return TP_PREFFIX_HEX6 + CONSENT_ENTITY_CODE \
           + CLIENT_ENTITY_CODE + _hash(dest_pkey)[:29] \
           + CLIENT_ENTITY_CODE + _hash(src_pkey)[:29]


def make_consent_list_address():
    return TP_PREFFIX_HEX6 + CONSENT_ENTITY_CODE


def make_consent_list_address_by_destination_client(dest_pkey):
    return TP_PREFFIX_HEX6 + CONSENT_ENTITY_CODE \
           + CLIENT_ENTITY_CODE + _hash(dest_pkey)[:29]

