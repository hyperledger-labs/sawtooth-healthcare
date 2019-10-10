
package com.medicalinsurance;

import com.google.common.io.BaseEncoding;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.Timestamp;
import java.util.Date;

class Addressing{

//    static String DISTRIBUTION_NAME = "sawtooth-healthcare";
//
//    static String DEFAULT_URL = "http://127.0.0.1:8008";

    static String TP_FAMILYNAME = "healthcare";
    static String TP_VERSION = "1.0";
//    static String CLINIC_ENTITY_NAME = "clinic";
//    static String DOCTOR_ENTITY_NAME = "doctor";
//    static String PATIENT_ENTITY_NAME = "patient";
//    static String CLAIM_ENTITY_NAME = "claim";
//    static String EVENT_ENTITY_NAME = "event";
//    static String LAB_TEST_ENTITY_NAME = "lab_test";
//    static String PULSE_ENTITY_NAME = "pulse";

//    static String CLAIM_ENTITY_HEX6 = hash(CLAIM_ENTITY_NAME).substring(0, 6);
//    static String CLINIC_ENTITY_HEX64 = hash(CLINIC_ENTITY_NAME).substring(0, 64);

//    static String CLINIC_ENTITY_CODE = "01";
//    static String DOCTOR_ENTITY_CODE = "02";
    private static String PATIENT_ENTITY_CODE = "03";
//    static String CLAIM_ENTITY_CODE = "04";
//    static String EVENT_ENTITY_CODE = "05";
//    static String LAB_TEST_ENTITY_CODE = "06";
    private static String PULSE_ENTITY_CODE = "07";
//    static String LAB_ENTITY_CODE = "08";

//    static String PATIENT_LAB_TEST__RELATION_CODE = "51";
//    static String LAB_TEST_PATIENT__RELATION_CODE = "52";

    private static String TP_PREFFIX_HEX6 = hash(TP_FAMILYNAME).substring(0, 6);

    static String TP_CONSENT_FAMILYNAME = "consent";
    static String TP_CONSENT_VERSION = "1.0";

    private static String CLIENT_ENTITY_CODE = "02";
    private static String TP_CONSENT_PREFFIX_HEX6 = hash(TP_CONSENT_FAMILYNAME).substring(0, 6);

    private static String hash(String input) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-512");
            md.reset();
            md.update(input.getBytes());
            return BaseEncoding.base16().lowerCase().encode(md.digest());
        }
        catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }

    static String hash(byte[] input) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-512");
            md.reset();
            md.update(input);
            return BaseEncoding.base16().lowerCase().encode(md.digest());
        }
        catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }
//    static String makeLabTestAddress(String clinicPKey, long eventTime){
//        return TP_PREFFIX_HEX6 + LAB_TEST_ENTITY_CODE +
//                hash(LAB_TEST_ENTITY_NAME).substring(0, 6) +
//                hash(clinicPKey).substring(0, 6) +
//                hash(String.valueOf(eventTime)).substring(0, 50);
//    }
//
//    static String makeLabTestListByClinicAddress(String clinicPKey){
//        return TP_PREFFIX_HEX6 + LAB_TEST_ENTITY_CODE +
//                hash(LAB_TEST_ENTITY_NAME).substring(0, 6) +
//                hash(clinicPKey).substring(0, 6);
//    }
//
//    static String makeLabTestListAddress(){
//        return TP_PREFFIX_HEX6 + LAB_TEST_ENTITY_CODE + hash(LAB_TEST_ENTITY_NAME).substring(0, 6);
//    }
//
//    static String makeClinicAddress(String clinicPKey){
//        return TP_PREFFIX_HEX6 + CLINIC_ENTITY_CODE + hash(CLINIC_ENTITY_NAME).substring(0, 6) +
//                hash(clinicPKey).substring(0, 56);
//    }
//
//    static String makeClinicListAddress(){
//        return TP_PREFFIX_HEX6 + CLINIC_ENTITY_CODE + hash(CLINIC_ENTITY_NAME).substring(0, 6);
//    }


//    static String makePulseListAddressForPatient(String publicKey) {
//        return TP_PREFFIX_HEX6 + PULSE_ENTITY_CODE +
//                hash(PULSE_ENTITY_NAME).substring(0, 6) +
//                hash(publicKey).substring(0, 6);
//    }
    static String makePatientAddress(String patientPKey){
        return TP_PREFFIX_HEX6 + PATIENT_ENTITY_CODE +
                hash(patientPKey).substring(0, 62);
    }

    static String makePulseAddress(String pulseId){
        return TP_PREFFIX_HEX6 + PULSE_ENTITY_CODE +
                hash(pulseId).substring(0, 62);
    }

    static String makePulseListAddress(){
        return TP_PREFFIX_HEX6 + PULSE_ENTITY_CODE;
    }

//    Pulse <-> Patient relation
    static String makePulsePatientRelationAddress(String pulseId, String clientPKey){
        String PULSE_PATIENT__RELATION_CODE = "62";
        return TP_PREFFIX_HEX6 + PULSE_PATIENT__RELATION_CODE +
            PULSE_ENTITY_CODE + hash(pulseId).substring(0, 30) +
            PATIENT_ENTITY_CODE + hash(clientPKey).substring(0, 28);
    }

//    static String makePatientListByPulseAddress(String pulseId){
//        return TP_PREFFIX_HEX6 + PULSE_PATIENT__RELATION_CODE +
//                PULSE_ENTITY_CODE + hash(pulseId).substring(0, 30);
//    }

    //    Patient <-> Pulse relation
    static String makePatientPulseRelationAddress(String clientPKey, String pulseId){
        String PATIENT_PULSE__RELATION_CODE = "61";
        return TP_PREFFIX_HEX6 + PATIENT_PULSE__RELATION_CODE +
                PATIENT_ENTITY_CODE + hash(clientPKey).substring(0, 30) +
                PULSE_ENTITY_CODE + hash(pulseId).substring(0, 28);
    }

//    static String makePulseListByPatientAddress(String clientPKey){
//        return TP_PREFFIX_HEX6 + PATIENT_PULSE__RELATION_CODE +
//                PATIENT_ENTITY_CODE + hash(clientPKey).substring(0, 30);
//    }

//    static String makePatientListAddress(){
//        return TP_PREFFIX_HEX6 + PATIENT_ENTITY_CODE + hash(PATIENT_ENTITY_NAME).substring(0, 6);
//    }

    //    Client entity
    static String makeClientAddress(String publicKey){
        return TP_CONSENT_PREFFIX_HEX6 + CLIENT_ENTITY_CODE + hash(publicKey).substring(0, 62);
    }

    static String makeConsentAddress(String destPKey, String srcPKey){
        //    static String CONSENT_ENTITY_NAME = "consent";
        String CONSENT_ENTITY_CODE = "01";
        return TP_CONSENT_PREFFIX_HEX6 + CONSENT_ENTITY_CODE +
                CLIENT_ENTITY_CODE + hash(destPKey).substring(0, 30) +
                CLIENT_ENTITY_CODE + hash(srcPKey).substring(0, 28);
    }

    static long getCurrentTimestamp(){
        Date date= new Date();
        long time = date.getTime();
        final Timestamp ts = new Timestamp(time);
        return ts.getTime();
    }
}
