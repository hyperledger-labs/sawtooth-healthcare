package com.medicalinsurance;

import com.medicalinsurance.protobuf.ConsentPayload;
import com.medicalinsurance.protobuf.Payload;
//import com.google.protobuf.ByteString;
//
//import java.io.ByteArrayOutputStream;
//import java.io.IOException;
//import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.UUID;
import java.util.logging.Logger;

import sawtooth.sdk.protobuf.Batch;
import sawtooth.sdk.protobuf.BatchHeader;
import sawtooth.sdk.protobuf.BatchList;
import sawtooth.sdk.protobuf.Transaction;
import sawtooth.sdk.protobuf.TransactionHeader;
import sawtooth.sdk.signing.PrivateKey;
import sawtooth.sdk.signing.Secp256k1Context;
import sawtooth.sdk.signing.Signer;


class DEHRRequestHandler {

    private Logger log = Logger.getLogger(DEHRRequestHandler.class.getName());
    //    private var service: SawtoothRestApi? = null
    private Signer signer;

    DEHRRequestHandler(PrivateKey privateKey) {
        Secp256k1Context context = new Secp256k1Context();
        this.signer = new Signer(context, privateKey);
    }

    BatchList addPulse(String id, int pulse, long timestamp) {
        String publicKey = signer.getPublicKey().hex();
        Payload.AddPulse pulsePayload = Payload.AddPulse.newBuilder()
                .setId(id)
                .setClientPkey(publicKey)
                .setPulse(String.valueOf(pulse))
                .setTimestamp(String.valueOf(timestamp)).build();

        Payload.TransactionPayload transactionPayload = Payload.TransactionPayload.newBuilder()
                .setPayloadType(Payload.TransactionPayload.PayloadType.ADD_PULSE)
                .setPulse(pulsePayload).build();

        String pulseAddress = Addressing.makePulseAddress(id);
        String pulsePatientRelationAddress = Addressing.makePulsePatientRelationAddress(id, publicKey);
        String patientPulseRelationAddress = Addressing.makePatientPulseRelationAddress(publicKey, id);
        Transaction addPulseTransaction = makeTransaction(
                Arrays.asList(pulseAddress,
                    pulsePatientRelationAddress,
                    patientPulseRelationAddress),
                Arrays.asList(pulseAddress,
                    pulsePatientRelationAddress,
                    patientPulseRelationAddress),
                transactionPayload);
        Batch batch = makeBatch(Collections.singletonList(addPulseTransaction));

        return BatchList.newBuilder()
                .addBatches(batch)
                .build();
    }

    BatchList addPatient(String name, String surname) {
        String publicKey = signer.getPublicKey().hex();

        List<ConsentPayload.Permission> permissions = new ArrayList<>();
        permissions.add(ConsentPayload.Permission.newBuilder().setType(ConsentPayload.Permission.PermissionType.READ_PATIENT).build());
        permissions.add(ConsentPayload.Permission.newBuilder().setType(ConsentPayload.Permission.PermissionType.READ_OWN_PATIENT).build());
        permissions.add(ConsentPayload.Permission.newBuilder().setType(ConsentPayload.Permission.PermissionType.READ_OWN_LAB_TEST).build());
        permissions.add(ConsentPayload.Permission.newBuilder().setType(ConsentPayload.Permission.PermissionType.READ_OWN_PULSE).build());
        permissions.add(ConsentPayload.Permission.newBuilder().setType(ConsentPayload.Permission.PermissionType.READ_OWN_CLAIM).build());
        permissions.add(ConsentPayload.Permission.newBuilder().setType(ConsentPayload.Permission.PermissionType.WRITE_LAB_TEST).build());
        permissions.add(ConsentPayload.Permission.newBuilder().setType(ConsentPayload.Permission.PermissionType.WRITE_PULSE).build());
        permissions.add(ConsentPayload.Permission.newBuilder().setType(ConsentPayload.Permission.PermissionType.WRITE_CLAIM).build());
        permissions.add(ConsentPayload.Permission.newBuilder().setType(ConsentPayload.Permission.PermissionType.REVOKE_ACCESS).build());
        permissions.add(ConsentPayload.Permission.newBuilder().setType(ConsentPayload.Permission.PermissionType.GRANT_ACCESS).build());

        ConsentPayload.Client client = ConsentPayload.Client.newBuilder()
                .addAllPermissions(permissions)
                .setPublicKey(publicKey).build();

        ConsentPayload.ConsentTransactionPayload consentTransactionPayload = ConsentPayload.ConsentTransactionPayload.newBuilder()
                .setPayloadType(ConsentPayload.ConsentTransactionPayload.PayloadType.ADD_CLIENT)
                .setCreateClient(client).build();

        String clientAddress = Addressing.makeClientAddress(publicKey);

        final Transaction addClientTransaction = makeConsentTransaction(
                Collections.singletonList(clientAddress),
                Collections.singletonList(clientAddress),
                consentTransactionPayload);

        Payload.CreatePatient patientPayload = Payload.CreatePatient.newBuilder()
//                .setPublicKey(publicKey)
                .setName(name)
                .setSurname(surname).build();

        Payload.TransactionPayload transactionPayload = Payload.TransactionPayload.newBuilder()
                .setPayloadType(Payload.TransactionPayload.PayloadType.CREATE_PATIENT)
                .setCreatePatient(patientPayload).build();
        log.info("transactionPayload: " + transactionPayload.toString());
        String address = Addressing.makePatientAddress(publicKey);

        final Transaction addPatientTransaction = makeTransaction(
                Collections.singletonList(address),
                Collections.singletonList(address),
                transactionPayload);

        Batch batch = makeBatch(Arrays.asList(addClientTransaction, addPatientTransaction));
//        Batch batch = makeBatch(Collections.singletonList(addClientTransaction)..add(addPatientTransaction));

        return BatchList.newBuilder()
                .addBatches(batch)
                .build();
    }

    BatchList grantAccess(String doctorPKey) {
        String publicKey = signer.getPublicKey().hex();
        ConsentPayload.ActionOnAccess grantAccessPayload = ConsentPayload.ActionOnAccess.newBuilder()
                .setDoctorPkey(doctorPKey)
                .setPatientPkey(publicKey)
                .build();

        ConsentPayload.ConsentTransactionPayload transactionPayload = ConsentPayload.ConsentTransactionPayload.newBuilder()
                .setPayloadType(ConsentPayload.ConsentTransactionPayload.PayloadType.GRANT_ACCESS)
                .setGrantAccess(grantAccessPayload).build();

        String address = Addressing.makeConsentAddress(doctorPKey, signer.getPublicKey().hex());

        Transaction grantAccessTransaction = makeConsentTransaction(
                Collections.singletonList(address),
                Collections.singletonList(address),
                transactionPayload);
        Batch batch = makeBatch(Collections.singletonList(grantAccessTransaction));

        return BatchList.newBuilder()
                .addBatches(batch)
                .build();
    }

    BatchList revokeAccess(String doctorPKey) {
        String publicKey = signer.getPublicKey().hex();
        ConsentPayload.ActionOnAccess revokeAccessPayload = ConsentPayload.ActionOnAccess.newBuilder()
                .setDoctorPkey(doctorPKey)
                .setPatientPkey(publicKey)
                .build();

        ConsentPayload.ConsentTransactionPayload transactionPayload = ConsentPayload.ConsentTransactionPayload.newBuilder()
                .setPayloadType(ConsentPayload.ConsentTransactionPayload.PayloadType.REVOKE_ACCESS)
                .setRevokeAccess(revokeAccessPayload).build();

        String address = Addressing.makeConsentAddress(doctorPKey, signer.getPublicKey().hex());

        Transaction revokeAccessTransaction = makeConsentTransaction(
                Collections.singletonList(address),
                Collections.singletonList(address),
                transactionPayload);
        Batch batch = makeBatch(Collections.singletonList(revokeAccessTransaction));

        return BatchList.newBuilder()
                .addBatches(batch)
                .build();
    }

    private Transaction makeTransaction(List<String> inputs, List <String> outputs, Payload.TransactionPayload transactionPayload) {

//        ByteArrayOutputStream baos = new ByteArrayOutputStream();
//        transactionPayload.writeTo(baos);
//        String serializedPayload = new String(baos.toByteArray(), StandardCharsets.UTF_8);

        TransactionHeader header = TransactionHeader.newBuilder()
                .setSignerPublicKey(signer.getPublicKey().hex())
                .setFamilyName(Addressing.TP_FAMILYNAME)
                .setFamilyVersion(Addressing.TP_VERSION)
                .addAllInputs(inputs)
                .addAllOutputs(outputs)
                .setPayloadSha512(Addressing.hash(transactionPayload.toByteArray()))
                .setBatcherPublicKey(signer.getPublicKey().hex())
                .setNonce(UUID.randomUUID().toString())
                .build();

        String signature = signer.sign(header.toByteArray());

        return Transaction.newBuilder()
                .setHeader(header.toByteString())
                .setPayload(transactionPayload.toByteString())
                .setHeaderSignature(signature)
                .build();
    }

    private Transaction makeConsentTransaction(List<String> inputs, List<String> outputs, ConsentPayload.ConsentTransactionPayload transactionPayload) {

//        ByteArrayOutputStream baos = new ByteArrayOutputStream();
//        transactionPayload.writeTo(baos);
//        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
//        String serializedPayload = new String(baos.toByteArray(), StandardCharsets.UTF_8);
//        String serializedPayload = Base64.getEncoder().encodeToString(transactionPayload.toByteArray());
//        String serializedPayload = transactionPayload.toByteString().toString();
//        log.info("consentTransactionPayload before serialization: " + transactionPayload.toString());
//        String encodedString = Base64.getEncoder().encodeToString(transactionPayload.toByteArray());
//        log.info("encodedString: " + encodedString);
//        byte[] decodedBytes = Base64.getDecoder().decode(encodedString);
//        String decodedString = new String(decodedBytes);
//        log.info("decodedString: " + decodedString);
//        ConsentPayload.ConsentTransactionPayload deserializePayload = ConsentPayload.ConsentTransactionPayload.parseFrom(decodedBytes);
//        log.info("consentTransactionPayload after de-serialization: " + deserializePayload.toString());

//        log.info("consentTransactionPayload after serialization: " + serializedPayload);
//        try {
//            String serializedPayloadHash = Addressing.hash2(serializedPayload);
//            log.info("serializedPayloadHash: " + serializedPayloadHash);
//            byte[] decodedData = Base64.getDecoder().decode(serializedPayloadHash);
//            String decodedString = new String(decodedData);
//            log.info("decodedString: " + decodedString);
////            ConsentPayload.ConsentTransactionPayload deserializePayloadHash = ConsentPayload.ConsentTransactionPayload.parseFrom(ByteString.copyFrom(serializedPayloadHash, StandardCharsets.UTF_8));
//            ConsentPayload.ConsentTransactionPayload deserializePayloadHash = ConsentPayload.ConsentTransactionPayload.parseFrom(decodedData);
//            log.info("deserializePayloadHash: " + deserializePayloadHash.toString());
//        } catch (NoSuchAlgorithmException e) {
//            e.printStackTrace();
//        }
//        ConsentPayload.ConsentTransactionPayload deserializePayloadString = ConsentPayload.ConsentTransactionPayload.parseFrom(ByteString.copyFrom(serializedPayload, StandardCharsets.UTF_8));
//        log.info("consentTransactionPayload after de-serialization string: " + deserializePayloadString.toString());
//        ConsentPayload.ConsentTransactionPayload deserializePayload = ConsentPayload.ConsentTransactionPayload.parseFrom(bais);
//        log.info("consentTransactionPayload after de-serialization byte: " + deserializePayload.toString());

        TransactionHeader header = TransactionHeader.newBuilder()
                .setSignerPublicKey(signer.getPublicKey().hex())
                .setFamilyName(Addressing.TP_CONSENT_FAMILYNAME)
                .setFamilyVersion(Addressing.TP_CONSENT_VERSION)
                .addAllInputs(inputs)
                .addAllOutputs(outputs)
//                .setPayloadSha512(Addressing.hash(serializedPayload))
                .setPayloadSha512(Addressing.hash(transactionPayload.toByteArray()))
                .setBatcherPublicKey(signer.getPublicKey().hex())
                .setNonce(UUID.randomUUID().toString())
                .build();

        String signature = signer.sign(header.toByteArray());

        return Transaction.newBuilder()
                .setHeader(header.toByteString())
                .setPayload(transactionPayload.toByteString())
//                .setPayload(ByteString.copyFrom(serializedPayload, "UTF-8"))
                .setHeaderSignature(signature)
                .build();
    }

    private Batch makeBatch(List<Transaction> transactions) {
        List<String> transactionIds = new ArrayList<>();
        for(Transaction transact: transactions){
            transactionIds.add(transact.getHeaderSignature());
        }
        BatchHeader batchHeader = BatchHeader.newBuilder()
                .setSignerPublicKey(signer.getPublicKey().hex())
                .addAllTransactionIds(transactionIds)
                .build();

        String batchSignature = signer.sign(batchHeader.toByteArray());

        return Batch.newBuilder()
                .setHeader(batchHeader.toByteString())
                .addAllTransactions(transactions)
                .setHeaderSignature(batchSignature)
                .build();
    }
}
