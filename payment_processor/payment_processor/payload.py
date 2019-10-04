from payment_processor.payment_common.protobuf import payment_payload_pb2
from payment_processor.payment_common.protobuf.payment_payload_pb2 import PaymentTransactionPayload


class PaymentPayload(object):

    def __init__(self, payload):
        self._transaction = PaymentTransactionPayload()
        self._transaction.ParseFromString(payload)

    # def grant_access(self):
    #     return self._transaction.grant_access
    #
    # def revoke_access(self):
    #     return self._transaction.revoke_access

    def is_create_payment(self):
        return self._transaction.payload_type == payment_payload_pb2.PaymentTransactionPayload.ADD_PAYMENT

    # def is_revoke_access(self):
    #     return self._transaction.payload_type == consent_payload_pb2.ConsentTransactionPayload.REVOKE_ACCESS

    def transaction_type(self):
        return self._transaction.payload_type

    # def is_create_client(self):
    #     return self._transaction.payload_type == consent_payload_pb2.ConsentTransactionPayload.ADD_CLIENT
    #
    def create_payment(self):
        return self._transaction.create_payment
