from processor.insurance_common.protobuf import insurance_payload_pb2 as payload_pb2


class InsurancePayload(object):

    def __init__(self, payload):
        self._transaction = payload_pb2.TransactionPayload()
        self._transaction.ParseFromString(payload)

    def create_insurance(self):
        return self._transaction.create_insurance

    def add_contract(self):
        return self._transaction.add_contract

    # def create_patient(self):
    #     return self._transaction.create_patient
    #
    # def create_lab(self):
    #     return self._transaction.create_lab
    #
    # def create_claim(self):
    #     return self._transaction.create_claim
    #
    # def assign_doctor(self):
    #     return self._transaction.assign_doctor
    #
    # def first_visit(self):
    #     return self._transaction.first_visit
    #
    # def pass_tests(self):
    #     return self._transaction.pass_tests
    #
    # def attend_procedures(self):
    #     return self._transaction.attend_procedures
    #
    # def eat_pills(self):
    #     return self._transaction.eat_pills
    #
    # def next_visit(self):
    #     return self._transaction.next_visit
    #
    # def lab_test(self):
    #     return self._transaction.lab_test
    #
    # def pulse(self):
    #     return self._transaction.pulse

    def is_create_insurance(self):
        return self._transaction.payload_type == payload_pb2.TransactionPayload.CREATE_INSURANCE

    def is_add_contract(self):
        return self._transaction.payload_type == payload_pb2.TransactionPayload.ADD_CONTRACT

    # def is_create_patient(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.CREATE_PATIENT
    #
    # def is_create_lab(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.CREATE_LAB
    #
    # def is_create_claim(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.CREATE_CLAIM
    #
    # def is_assign_doctor(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.ASSIGN_DOCTOR
    #
    # def is_first_visit(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.FIRST_VISIT
    #
    # def is_pass_tests(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.PASS_TESTS
    #
    # def is_attend_procedures(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.ATTEND_PROCEDURES
    #
    # def is_eat_pills(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.EAT_PILLS
    #
    # def is_next_visit(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.NEXT_VISIT
    #
    # def is_lab_test(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.ADD_LAB_TEST
    #
    # def is_pulse(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.ADD_PULSE

    def transaction_type(self):
        return self._transaction.payload_type
