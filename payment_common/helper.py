import hashlib
import time

DISTRIBUTION_NAME = 'sawtooth-payment'

DEFAULT_URL = 'http://127.0.0.1:8009'

TP_FAMILYNAME = 'payment'
TP_VERSION = '1.0'
PAYMENT_ENTITY_CODE = '01'
PAYER_ENTITY_CODE = '02'
PAYMENT_ID_ENTITY_CODE = '03'


def _hash(identifier):
    return hashlib.sha512(identifier.encode('utf-8')).hexdigest()


TP_PREFFIX_HEX6 = _hash(TP_FAMILYNAME)[0:6]


def make_payment_address(payer_pkey, uid):
    return TP_PREFFIX_HEX6 + PAYMENT_ENTITY_CODE \
            + PAYER_ENTITY_CODE + _hash(payer_pkey)[:40] \
            + PAYMENT_ID_ENTITY_CODE + _hash(uid)[:18]


def make_payment_list_by_payer_address(payer_pkey):
    return TP_PREFFIX_HEX6 + PAYMENT_ENTITY_CODE \
            + PAYER_ENTITY_CODE + _hash(payer_pkey)[:40]


def make_payment_list_address():
    return TP_PREFFIX_HEX6 + PAYMENT_ENTITY_CODE


def get_current_timestamp():
    return int(round(time.time() * 1000))
