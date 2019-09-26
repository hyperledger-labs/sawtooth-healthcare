import hashlib
import time

DISTRIBUTION_NAME = 'sawtooth-insurance'

DEFAULT_URL = 'http://127.0.0.1:8008'

TP_FAMILYNAME = 'insurance'
TP_VERSION = '1.0'

# CLINIC_ENTITY_CODE = '01'
# DOCTOR_ENTITY_CODE = '02'
# PATIENT_ENTITY_CODE = '01'
# CLAIM_ENTITY_CODE = '04'
# EVENT_ENTITY_CODE = '05'
# LAB_TEST_ENTITY_CODE = '06'
# PULSE_ENTITY_CODE = '07'
# LAB_ENTITY_CODE = '08'
CONTRACT_ENTITY_CODE = '01'
INSURANCE_ENTITY_CODE = '02'


CONTRACT_INSURANCE__RELATION_CODE = "51"
INSURANCE_CONTRACT__RELATION_CODE = "52"

# PATIENT_COMPANY__RELATION_CODE = "51"
# COMPANY_PATIENT__RELATION_CODE = "52"

# PATIENT_CONTRACT__RELATION_CODE = "71"
# CONTRACT_PATIENT__RELATION_CODE = "72"


def _hash(identifier):
    return hashlib.sha512(identifier.encode('utf-8')).hexdigest()


TP_PREFFIX_HEX6 = _hash(TP_FAMILYNAME)[0:6]


def make_insurance_address(insurance_pkey):
    return TP_PREFFIX_HEX6 + INSURANCE_ENTITY_CODE + _hash(insurance_pkey)[:62]


def make_insurance_list_address():
    return TP_PREFFIX_HEX6 + INSURANCE_ENTITY_CODE


# Contract entity
def make_contract_address(contract_id):
    return TP_PREFFIX_HEX6 + CONTRACT_ENTITY_CODE + _hash(contract_id)[:62]


def make_contract_list_address():
    return TP_PREFFIX_HEX6 + CONTRACT_ENTITY_CODE


# Contract <-> Insurance relation
def make_contract_insurance__relation_address(contract_id, insurance_pkey):
    return TP_PREFFIX_HEX6 + CONTRACT_INSURANCE__RELATION_CODE + \
           CONTRACT_ENTITY_CODE + _hash(contract_id)[:30] + \
           INSURANCE_ENTITY_CODE + _hash(insurance_pkey)[:28]


def make_insurance_list_by_contract_address(contract_id):
    return TP_PREFFIX_HEX6 + CONTRACT_INSURANCE__RELATION_CODE + CONTRACT_ENTITY_CODE + _hash(contract_id)[:30]


# Insurance <-> Contract relation
def make_insurance_contract__relation_address(insurance_pkey, contract_id):
    return TP_PREFFIX_HEX6 + INSURANCE_CONTRACT__RELATION_CODE + \
           INSURANCE_ENTITY_CODE + _hash(insurance_pkey)[:30] + \
           CONTRACT_ENTITY_CODE + _hash(contract_id)[:28]


def make_contract_list_by_insurance_address(insurance_pkey):
    return TP_PREFFIX_HEX6 + INSURANCE_CONTRACT__RELATION_CODE + INSURANCE_ENTITY_CODE + _hash(insurance_pkey)[:30]


def get_current_timestamp():
    return int(round(time.time() * 1000))
