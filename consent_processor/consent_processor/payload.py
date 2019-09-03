from consent_processor.consent_common.protobuf import consent_payload_pb2


class ConsentPayload(object):

    def __init__(self, payload):
        self._transaction = consent_payload_pb2.ConsentTransactionPayload()
        self._transaction.ParseFromString(payload)

    def grant_access(self):
        return self._transaction.grant_access

    def revoke_access(self):
        return self._transaction.revoke_access

    def is_grant_access(self):
        return self._transaction.payload_type == consent_payload_pb2.ConsentTransactionPayload.GRANT_ACCESS

    def is_revoke_access(self):
        return self._transaction.payload_type == consent_payload_pb2.ConsentTransactionPayload.REVOKE_ACCESS

    def transaction_type(self):
        return self._transaction.payload_type
