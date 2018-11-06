from common.protobuf import payload_pb2


class HealthCarePayload(object):

    def __init__(self, payload):
        self._transaction = payload_pb2.TransactionPayload()
        self._transaction.ParseFromString(payload)

    def create_clinic(self):
        return self._transaction.create_clinic

    def create_doctor(self):
        return self._transaction.create_doctor

    def create_patient(self):
        return self._transaction.create_patient

    def create_claim(self):
        return self._transaction.create_claim

    def assign_doctor(self):
        return self._transaction.assign_doctor

    def first_visit(self):
        return self._transaction.first_visit

    def pass_tests(self):
        return self._transaction.pass_tests

    def attend_procedures(self):
        return self._transaction.attend_procedures

    def eat_pills(self):
        return self._transaction.eat_pills

    def next_visit(self):
        return self._transaction.next_visit

    def is_create_clinic(self):
        return self._transaction.payload_type == payload_pb2.TransactionPayload.CREATE_CLINIC

    def is_create_doctor(self):
        return self._transaction.payload_type == payload_pb2.TransactionPayload.CREATE_DOCTOR

    def is_create_patient(self):
        return self._transaction.payload_type == payload_pb2.TransactionPayload.CREATE_PATIENT

    def is_create_claim(self):
        return self._transaction.payload_type == payload_pb2.TransactionPayload.CREATE_CLAIM

    def is_assign_doctor(self):
        return self._transaction.payload_type == payload_pb2.TransactionPayload.ASSIGN_DOCTOR

    def is_first_visit(self):
        return self._transaction.payload_type == payload_pb2.TransactionPayload.FIRST_VISIT

    def is_pass_tests(self):
        return self._transaction.payload_type == payload_pb2.TransactionPayload.PASS_TESTS

    def is_attend_procedures(self):
        return self._transaction.payload_type == payload_pb2.TransactionPayload.ATTEND_PROCEDURES

    def is_eat_pills(self):
        return self._transaction.payload_type == payload_pb2.TransactionPayload.EAT_PILLS

    def is_next_visit(self):
        return self._transaction.payload_type == payload_pb2.TransactionPayload.NEXT_VISIT

    def transaction_type(self):
        return self._transaction.payload_type
