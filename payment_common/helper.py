import hashlib
import time

DISTRIBUTION_NAME = 'sawtooth-payment'

DEFAULT_URL = 'http://127.0.0.1:8009'

TP_FAMILYNAME = 'payment'
TP_VERSION = '1.0'

PAYMENT_ENTITY_CODE = '01'
PATIENT_ENTITY_CODE = '02'
CONTRACT_ENTITY_CODE = '03'

CONTRACT_PAYMENT__RELATION_CODE = "51"
PAYMENT_CONTRACT__RELATION_CODE = "52"

PATIENT_PAYMENT__RELATION_CODE = "61"
PAYMENT_PATIENT__RELATION_CODE = "62"


def _hash(identifier):
    return hashlib.sha512(identifier.encode('utf-8')).hexdigest()


TP_PREFFIX_HEX6 = _hash(TP_FAMILYNAME)[0:6]


# Payment entity
def make_payment_address(payment_id):
    return TP_PREFFIX_HEX6 + PAYMENT_ENTITY_CODE + _hash(payment_id)[:62]


def make_payment_list_address():
    return TP_PREFFIX_HEX6 + PAYMENT_ENTITY_CODE


# Contract <-> Payment relation
def make_contract_payment__relation_address(contract_id, payment_id):
    return TP_PREFFIX_HEX6 + CONTRACT_PAYMENT__RELATION_CODE + \
           CONTRACT_ENTITY_CODE + _hash(contract_id)[:30] + \
           PAYMENT_ENTITY_CODE + _hash(payment_id)[:28]


def make_payment_list_by_contract_address(contract_id):
    return TP_PREFFIX_HEX6 + CONTRACT_PAYMENT__RELATION_CODE + CONTRACT_ENTITY_CODE + _hash(contract_id)[:30]


# Payment <-> Contract relation
def make_payment_contract__relation_address(payment_id, contract_id):
    return TP_PREFFIX_HEX6 + PAYMENT_CONTRACT__RELATION_CODE + \
           PAYMENT_ENTITY_CODE + _hash(payment_id)[:30] + \
           CONTRACT_ENTITY_CODE + _hash(contract_id)[:28]


def make_contract_list_by_payment_address(payment_id):
    return TP_PREFFIX_HEX6 + PAYMENT_CONTRACT__RELATION_CODE + PAYMENT_ENTITY_CODE + _hash(payment_id)[:30]


# Patient <-> Payment relation
def make_patient_payment__relation_address(patient_pkey, payment_id):
    return TP_PREFFIX_HEX6 + PATIENT_PAYMENT__RELATION_CODE + \
           PATIENT_ENTITY_CODE + _hash(patient_pkey)[:30] + \
           PAYMENT_ENTITY_CODE + _hash(payment_id)[:28]


def make_payment_list_by_patient_address(patient_pkey):
    return TP_PREFFIX_HEX6 + PATIENT_PAYMENT__RELATION_CODE + PATIENT_ENTITY_CODE + _hash(patient_pkey)[:30]


# Payment <-> Patient relation
def make_payment_patient__relation_address(payment_id, patient_pkey):
    return TP_PREFFIX_HEX6 + PAYMENT_PATIENT__RELATION_CODE + \
           PAYMENT_ENTITY_CODE + _hash(payment_id)[:30] + \
           PATIENT_ENTITY_CODE + _hash(patient_pkey)[:28]


def make_patient_list_by_payment_address(payment_id):
    return TP_PREFFIX_HEX6 + PAYMENT_PATIENT__RELATION_CODE + PAYMENT_ENTITY_CODE + _hash(payment_id)[:30]


def get_current_timestamp():
    return int(round(time.time() * 1000))
