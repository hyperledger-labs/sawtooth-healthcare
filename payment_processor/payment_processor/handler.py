import logging

from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.handler import TransactionHandler

import payment_processor.payment_common.helper as helper
# from payment_processor.payload import PaymentPayload
# from payment_processor.state import PaymentState
from payment_processor.payload import PaymentPayload
from payment_processor.state import PaymentState

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class PaymentTransactionHandler(TransactionHandler):
    def __init__(self, namespace_prefix):
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        return helper.TP_FAMILYNAME

    @property
    def family_versions(self):
        return [helper.TP_VERSION]

    @property
    def namespaces(self):
        return [self._namespace_prefix]

    def apply(self, transaction, context):
        try:

            _display("i'm inside handler _display")
            print("i'm inside handler print")

            # header = transaction.header
            # signer = header.signer_public_key
            LOGGER.debug("transaction payload: " + str(transaction.payload))
            payload = PaymentPayload(payload=transaction.payload)

            state = PaymentState(context)

            if payload.is_create_payment():
                LOGGER.debug("Add Payment")
                payment = payload.create_payment()
                state.create_payment(payment)
            # elif consent_payload.is_grant_access():
            #     LOGGER.debug("Grant Access")
            #     access = consent_payload.grant_access()
            #     consent_state.grant_access(doctor_pkey=access.doctor_pkey, patient_pkey=access.patient_pkey)
            # elif consent_payload.is_create_client():
            #     LOGGER.debug("Create Client")
            #     client = consent_payload.create_client()
            #     consent_state.create_client(client)
            else:
                raise InvalidTransaction('Unhandled action: {}'.format(payload.transaction_type()))
        except Exception as e:
            print("Error: {}".format(e))
            logging.exception(e)
            raise InvalidTransaction(repr(e))


def _display(msg):
    n = msg.count("\n")

    if n > 0:
        msg = msg.split("\n")
        length = max(len(line) for line in msg)
    else:
        length = len(msg)
        msg = [msg]

    # pylint: disable=logging-not-lazy
    LOGGER.debug("+" + (length + 2) * "-" + "+")
    for line in msg:
        LOGGER.debug("+ " + line.center(length) + " +")
    LOGGER.debug("+" + (length + 2) * "-" + "+")
