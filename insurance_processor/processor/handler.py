import logging

from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.handler import TransactionHandler

import processor.insurance_common.helper as helper
from processor.payload import InsurancePayload
from processor.state import InsuranceState

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class InsuranceTransactionHandler(TransactionHandler):
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

            header = transaction.header
            signer = header.signer_public_key
            LOGGER.debug("signer_public_key: " + str(signer))
            LOGGER.debug("transaction payload: " + str(transaction.payload))
            payload = InsurancePayload(payload=transaction.payload)

            state = InsuranceState(context)

            if payload.is_create_insurance():
                insurance = payload.create_insurance()

                ins = state.get_insurance(insurance.public_key)
                if ins is not None:
                    raise InvalidTransaction(
                        'Invalid action: Insurance already exists: ' + ins.name)

                state.create_insurance(insurance)
            elif payload.is_add_contract():
                contract = payload.add_contract()

                con = state.get_contract(contract.client_pkey)
                if con is not None:
                    raise InvalidTransaction(
                        'Invalid action: Contract already exists: ' + con.id)

                state.add_contract(contract)
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
