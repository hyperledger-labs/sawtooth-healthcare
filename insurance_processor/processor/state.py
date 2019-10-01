from processor.insurance_common import helper
import logging

from processor.insurance_common.protobuf.insurance_payload_pb2 import Insurance, Contract

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class InsuranceState(object):
    TIMEOUT = 3

    def __init__(self, context):
        """Constructor.
        Args:
            context (sawtooth_sdk.processor.context.Context): Access to
                validator state from within the transaction processor.
        """

        self._context = context

    def create_insurance(self, insurance):
        op = self._load_insurance(public_key=insurance.public_key)

        if op is None:
            self._store_insurance(insurance)

    def get_insurance(self, public_key):
        return self._load_insurance(public_key)

    def _load_insurance(self, public_key):
        insurance = None
        insurance_hex = helper.make_insurance_address(public_key)
        state_entries = self._context.get_state(
            [insurance_hex],
            timeout=self.TIMEOUT)
        if state_entries:
            insurance = Insurance()
            insurance.ParseFromString(state_entries[0].data)
        return insurance

    def _store_insurance(self, insurance):
        address = helper.make_insurance_address(insurance.public_key)

        state_data = insurance.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    def add_contract(self, signer, contract):
        con = self._load_contract(contract.id)
        if con is None:
            self._store_contract(signer=signer, contract=contract)

    def get_contract(self, uid):
        return self._load_contract(uid)

    def _load_contract(self, contract_id):
        contract = None
        contract_hex = helper.make_contract_address(contract_id)
        state_entries = self._context.get_state(
            [contract_hex],
            timeout=self.TIMEOUT)
        if state_entries:
            contract = Contract()
            contract.ParseFromString(state_entries[0].data)
        return contract

    def _store_contract(self, signer, contract):
        contract_hex = helper.make_contract_address(contract.id)
        contract_insurance_relation_hex = helper.make_contract_insurance__relation_address(contract.id,
                                                                                           signer)
        insurance_contract_relation_hex = helper.make_insurance_contract__relation_address(signer,
                                                                                           contract.id)

        contract_data = contract.SerializeToString()
        states = {
            contract_hex: contract_data,
            contract_insurance_relation_hex: str.encode(signer),
            insurance_contract_relation_hex: str.encode(contract.id)
        }
        LOGGER.debug("_store_contract: " + str(states))
        self._context.set_state(
            states,
            timeout=self.TIMEOUT)
