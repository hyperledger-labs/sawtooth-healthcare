import hashlib
import random
import time

from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader, Batch
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction, TransactionHeader

from . import helper as helper
from .protobuf import consent_payload_pb2


def _make_header_and_batch(payload, inputs, outputs, txn_signer, batch_signer):
    txn_header_bytes, signature = _transaction_header(txn_signer, batch_signer, inputs, outputs, payload)

    txn = Transaction(
        header=txn_header_bytes,
        header_signature=signature,
        payload=payload.SerializeToString()
    )

    transactions = [txn]

    batch_header_bytes, signature = _batch_header(batch_signer, transactions)

    batch = Batch(
        header=batch_header_bytes,
        header_signature=signature,
        transactions=transactions
    )

    # batch_list = BatchList(batches=[batch])
    # batch_id = batch_list.batches[0].header_signature
    # return batch_list, batch_id
    return batch, batch.header_signature


def _transaction_header(txn_signer, batch_signer, inputs, outputs, payload):
    txn_header_bytes = TransactionHeader(
        family_name=helper.TP_FAMILYNAME,
        family_version=helper.TP_VERSION,
        inputs=inputs,
        outputs=outputs,
        signer_public_key=txn_signer.get_public_key().as_hex(),  # signer.get_public_key().as_hex(),
        # In this example, we're signing the batch with the same private key,
        # but the batch can be signed by another party, in which case, the
        # public key will need to be associated with that key.
        batcher_public_key=batch_signer.get_public_key().as_hex(),  # signer.get_public_key().as_hex(),
        # In this example, there are no dependencies.  This list should include
        # an previous transaction header signatures that must be applied for
        # this transaction to successfully commit.
        # For example,
        # dependencies=['540a6803971d1880ec73a96cb97815a95d374cbad5d865925e5aa0432fcf1931539afe10310c122c5eaae15df61236079abbf4f258889359c4d175516934484a'],
        dependencies=[],
        nonce=random.random().hex().encode(),
        payload_sha512=hashlib.sha512(payload.SerializeToString()).hexdigest()
    ).SerializeToString()

    signature = txn_signer.sign(txn_header_bytes)
    return txn_header_bytes, signature


def _batch_header(batch_signer, transactions):
    batch_header_bytes = BatchHeader(
        signer_public_key=batch_signer.get_public_key().as_hex(),
        transaction_ids=[txn.header_signature for txn in transactions],
    ).SerializeToString()

    signature = batch_signer.sign(batch_header_bytes)

    return batch_header_bytes, signature


def grant_access(txn_signer, batch_signer, doctor_pkey):
    patient_pkey = txn_signer.get_public_key().as_hex()
    consent_hex = helper.make_consent_address(doctor_pkey=doctor_pkey, patient_pkey=patient_pkey)

    access = consent_payload_pb2.ActionOnAccess(
        doctor_pkey=doctor_pkey,
        patient_pkey=patient_pkey
    )

    payload = payload_pb2.TransactionPayload(
        payload_type=consent_payload_pb2.TransactionPayload.GRANT_ACCESS,
        grant_access=access)

    return _make_header_and_batch(
        payload=payload,
        inputs=[consent_hex],
        outputs=[consent_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def revoke_access(txn_signer, batch_signer, doctor_pkey):
    patient_pkey = txn_signer.get_public_key().as_hex()
    consent_hex = helper.make_consent_address(doctor_pkey=doctor_pkey, patient_pkey=patient_pkey)

    access = consent_payload_pb2.ActionOnAccess(
        doctor_pkey=doctor_pkey,
        patient_pkey=patient_pkey
    )

    payload = payload_pb2.TransactionPayload(
        payload_type=consent_payload_pb2.TransactionPayload.REVOKE_ACCESS,
        revoke_access=access)

    return _make_header_and_batch(
        payload=payload,
        inputs=[consent_hex],
        outputs=[consent_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)

