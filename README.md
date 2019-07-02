# Sawtooth Healthcare

Sawtooth Healthcare is a blockchain application built on Hyperledger Sawtooth, allowing clinics to keep history regarding patients health and claims on the blockchain. The repo is based on two other repos available on the internet:

https://github.com/hyperledger/sawtooth-marketplace 

https://github.com/hyperledger/sawtooth-core/tree/master/sdk/examples/xo_python

Note, this app is under constant development. All items mentioned in this documentation having "To be defined" will be ready later and updated accordingly. However, recent commits to the repo should functioning properly as described in the doc.

# Workflow Description

This application covers basic workflow when a patient visit clinic with a claim till he fills good:
- Prerequisites: clinic, doctor and patient entity objects registered in blockchain;
- Patient comes to clinic with a claim;
- Receptionist creates new claim for patient and assigns the claim to doctor;
- Patient visits the doctor with the claim and as result gets treatment direction (like pass certain tests, eat pills, attend procedures);
- Patient pass tests;
- Patient eats pills;
- Patient attends procedure;
- Patient visits doctor once again and report progress on the claim.

# Business Structure

## Business Objects

Application operates with certain business object entities:
- Clinic (entity on behalf of which claim is registered in blockchain with further update etc);
- Patient (actually user who has a claim). Corresponding account is clinic independent and can be serviced by different clinics;
- Doctor (actually user who investigate symptoms of the claim and provides suggestions). Corresponding account is clinic independent and can work in different clinics;
- Claim (actually claim of the patient). It is clinic dependent since it should be fixed by doctor who works in this clinic)
- Event on claim (anything that relates to the claim). In this particular case it could be like assign to a doctor, first visit to a doctor, eat pills, pass tests etc.

## Blockchain Server

Is nothing but blockchain ledger with predefined API that corresponds to the workflow and aimed to store, update and validate data according to the business process.

## Blockchain Client

Client application generates requests to the server basing on data from clinic and interacts with it.

# Technical Structure (Components)

## Common

This is common module, includes business object entities represented in Protobuf format, used in both client and server sides to serialize/deserialize objects.

Also, it has helper class which includes certain constants, methods for internal needs. 

## Smart Contract (Transaction Processor)

Heart of the app - custom module deployed into blockchain which validates and handles data transfers.

## Command Line Client (CLI)

Thin client presented as service command and requires certain parameters to proceed action.

## Web Client (REST API)

To be defined

## Regression Tests

To be defined

## Load Tests

To be defined

# Network Infrastructure

# Deploy & Setup

# How It Works (Step By Step)

This example shows how to use CLI client to operate with blockchain:

1. Prerequisite
    - Application is up and running;
    - Connect to client container from home directory of this repo (you are connected to the client's container) :

    ```bash
    $ docker exec -it healthcare-client /bin/bash
    root@dcc855da11ec:/project/sawtooth_healthcare#
    ```
    
    - There are 3 private key registered in the container: clinicCLI, doctorCLI, patientCLI (for clinic, doctor and patient accordingly). Every command to be invoked on behalf clinic's key.

1. Ensure clinic is registered in blockchain

	- Check clinics list (the list is empty since no clinic registered in blockchain before):

    ```bash
    root@f1525454c702:/project/sawtooth_healthcare# healthcare-cli-python list_clinics --url http://sawtooth-rest-api:8008
    HEX             NAME            PUBLIC_KEY
    ```
	
	- Create new clinic by clinicCLI key:
	
    ```bash
    root@f1525454c702:/project/sawtooth_healthcare# healthcare-cli-python create_clinic --username clinicCLI --name Clinic22 --url http://sawtooth-rest-api:8008
    Response: {
        "link": "http://sawtooth-rest-api:8008/batch_statuses?id=790786556ad147753620a0bf02a7c7f0d22665bc9a21c8f6e801475eeb9a1b0a1bc5d59d7291056cefc7876f3cd322d522ea6a04e44f3d9976e35233cf19b9a6"
    }
    ```

	- Ensure transaction processed successfully:
	
	```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# curl http://sawtooth-rest-api:8008/batch_statuses?id=9b02f64a8d38f2c849f50dbf916b3ce861b439234f434b0abcf4339e28c340eb09819a791813b4522e5d60cca1bc00e8be37e04b7df03f457a5c26c72fc5d73
    {
         "data": [
             {
                 "id": "9b02f64a8d38f2c849f50dbf916b3ce861b439234f434b0abcf4339e28c340eb09819a791813b4522e5d60cca1bc00e8be375e04b7df03f457a5c26c72fc5d73",
                 "invalid_transactions": [],
                 "status": "COMMITTED"
             }
         ],
         "link": "http://sawtooth-rest-api:8008/batch_statuses?id=9b02f64a8d38f2c849f50dbf916b3ce861b439234f434b0abcf4339e28c340eb09819a791813b4522e5d60cca1bc00e8be375e04b7df03f457a5c26c72fc5d73"
    }
    ```

	- Get clinics list (newly created item appeared in the list):

	```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python list_clinics --url http://sawtooth-rest-api:8008
    HEX             NAME            PUBLIC_KEY     
    3d804901bbfeb700e20359b62eb71c236e2f42a77b660f3838cc396b62db634bc23b87 Clinic22        034e1e7c10c7f79a67fa652e5929947186d0cf23df4a67136596f45919413957b6
    ```

1. Ensure doctor is registered in blockchain

	- Check doctors list (the list is empty since no doctors registered in blockhain before):

	```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python list_doctors --url http://sawtooth-rest-api:8008
    NAME            SURNAME         PUBLIC_KEY 
    ```

	- Create new doctor by doctorCLI key:
	
	```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python create_doctor --username doctorCLI --name Doctor22 --surname DoctorSurname22 --url http://sawtooth-rest-api:8008
    Response: {
         "link": "http://sawtooth-rest-api:8008/batch_statuses?id=ffee911434ffd36fc98f2f62d608e5acec7c4193fce2e213ac7809b077339e8a35aced8d0b216644a4755dbd7ec1ac28341b7369fdb6067641ebea6b478d7f17"
    }
    ```
	
	- Ensure transaction processed successfully (link is taken from response in previous step)
	
	```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# curl http://sawtooth-rest-api:8008/batch_statuses?id=ffee911434ffd36fc98f2f62d608e5acec7c4193fce2e213ac7809b077339e8a35aced8d0b216644a4755dbd7ec1ac28341b7369fdb6067641ebea6b478d7f17
    {
          "data": [
                {
                      "id": "ffee911434ffd36fc98f2f62d608e5acec7c4193fce2e213ac7809b077339e8a35aced8d0b216644a4755dbd7ec1ac28341b7369fdb6067641ebea6b478d7f17",
                      "invalid_transactions": [],
                      "status": "COMMITTED"
                }
          ],
          "link": "http://sawtooth-rest-api:8008/batch_statuses?id=ffee911434ffd36fc98f2f62d608e5acec7c4193fce2e213ac7809b077339e8a35aced8d0b216644a4755dbd7ec1ac28341b7369fdb6067641ebea6b478d7f17"
    }
    ```
	
	- Check doctors list again (newly created item appeared in the list):
	
	```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python list_doctors --url http://sawtooth-rest-api:8008
    NAME            SURNAME         PUBLIC_KEY     
    Doctor22        DoctorSurname22 03341e263b90de5ee7962b0dc88543a6f7fa18e8fdb0c01adba7d214a86f8985a2
    ```

1. Ensure patient is registered in blockchain

    - Check patients list (the list is empty):
    
    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python list_patients --url http://sawtooth-rest-api:8008
    PATIENT HEX     NAME            SURNAME         PUBLIC_KEY    
    ```

    - Create new patient by patientCLI key:

    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python create_patient --username patientCLI --name Patient22 --surname PatientSurname22 --url http://sawtooth-rest-api:8008
    Response: {
       "link": "http://sawtooth-rest-api:8008/batch_statuses?id=f66cbab8dc6af995f0d3282cd9b2e656891582962b3a67c9ea9960c1ae78c4797fc51418743b06a211e7e89fd0f9c7138a357a4b2b6ac7e34e167914dde82249"
    }
    ``` 
    
    - Ensure transaction processed successfully:

    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# curl http://sawtooth-rest-api:8008/batch_statuses?id=f66cbab8dc6af995f0d3282cd9b2e656891582962b3a67c9ea9960c1ae78c4797fc51418743b06a211e7e89fd0f9c7138a357a4b2b6ac7e34e167914dde82249
    {
       "data": [
           {
               "id": "f66cbab8dc6af995f0d3282cd9b2e656891582962b3a67c9ea9960c1ae78c4797fc51418743b06a211e7e89fd0f9c7138a357a4b2b6ac7e34e167914dde82249",
               "invalid_transactions": [],
               "status": "COMMITTED"
              }
       ],
       "link": "http://sawtooth-rest-api:8008/batch_statuses?id=f66cbab8dc6af995f0d3282cd9b2e656891582962b3a67c9ea9960c1ae78c4797fc51418743b06a211e7e89fd0f9c7138a357a4b2b6ac7e34e167914dde82249"
    }
    ```

    - Check patient list (newly created item appeared in the list):
    
    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python list_patients --url http://sawtooth-rest-api:8008PATIENT HEX     NAME            SURNAME         PUBLIC_KEY     
    3d8049032295ffaa8a3b9f7f9d28a9abbba2109fcb454fadfbd057560d9ec467cc8e77 Patient22       PatientSurname22 03e4273903a23cabeca68527035d22b7f997932ec1eb0a146ee346ed7374abe307
    ```

1. Receptionist registers new claim in blockchain:

    - Check claims list (the list is empty):
    
    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python list_claims --url http://sawtooth-rest-api:8008
    CLAIM HEX       CLAIM ID        CLINIC PKEY     PATIENT PKEY
    ```
    
    - Create new claim by clinicCLI key (new claim linked to patient using his public key from response above):
    
    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python create_claim --username clinicCLI --claim_id 23 --patient_pkey 03e4273903a23cabeca68527035d22b7f997932ec1eb0a146ee346ed7374abe307 --url http://sawtooth-rest-api:8008
    Response: {
       "link": "http://sawtooth-rest-api:8008/batch_statuses?id=1e583ffbc341146bdb589059f22fc3602e5c9104d060622dad51215e6bcda32c6aa8a37cf49cba8398c5d94c7e7f131adc9117f8898eaade132ac67a1f7eef54"
    }
    ```
    
    - Ensure transaction processed successfully:

    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# curl http://sawtooth-rest-api:8008/batch_statuses?id=1e583ffbc341146bdb589059f22fc3602e5c9104d060622dad51215e6bcda32c6aa8a37cf49cba8398c5d94c7e7f131adc9117f8898eaade132ac67a1f7eef54
    {
       "data": [
           {
               "id": "1e583ffbc341146bdb589059f22fc3602e5c9104d060622dad51215e6bcda32c6aa8a37cf49cba8398c5d94c7e7f131adc9117f8898eaade132ac67a1f7eef54",
               "invalid_transactions": [],
               "status": "COMMITTED"
           }
       ],
       "link": "http://sawtooth-rest-api:8008/batch_statuses?id=1e583ffbc341146bdb589059f22fc3602e5c9104d060622dad51215e6bcda32c6aa8a37cf49cba8398c5d94c7e7f131adc9117f8898eaade132ac67a1f7eef54"
    }
    ```
    
    - Check claim list (newly created item appeared in the list):

    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python list_claims --url http://sawtooth-rest-api:8008
    CLAIM HEX       CLAIM ID        CLINIC PKEY     PATIENT PKEY   
    3d804904dd1b3c535fa3bbfeb700e20359b62eb71c236e2f42a77b660f3838cc396b62 23              034e1e7c10c7f79a67fa652e5929947186d0cf23df4a67136596f45919413957b6 03e4273903a23cabeca68527035d22b7f997932ec1eb0a146ee346ed7374abe307
    ```

1. Check claim details (details are empty for now since no activities performed yet with the claim):
    
    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python list_claim_details --claim_id 23 --clinic_pkey 034e1e7c10c7f79a67fa652e5929947186d0cf23df4a67136596f45919413957b6 --url http://sawtooth-rest-api:8008
    EVENT HEX       CLAIM ID        CLINIC PKEY     EVENT           DESCRIPTION     EVENT TIME     
    ```
    
    NOTE: get claim details requires 2 parameters to identify exact claim: public key of the clinic and internal id of the claim in the clinic

1. Receptionist assigns claim to a doctor:

    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python assign_doctor --username clinicCLI --claim_id 23 --doctor_pkey 03341e263b90de5ee7962b0dc88543a6f7fa18e8fdb0c01adba7d214a86f8985a2 --url http://sawtooth-rest-api:8008
    Response: {
       "link": "http://sawtooth-rest-api:8008/batch_statuses?id=d3ddede3b71ca855cf39bb99f44e6e22027421f55595d65f64ec70b37f1e3db43b476e8ec93ab0ac34effdc7baecf48f118735193e3c90a4adbe780ded289dae"
    }
    ```
    
1. Check same claim details again (details contains note about claim assigned to doctor):

    ```bash
    root@dcc855da11ec:/project/awtooth_healthcare# healthcare-cli-python list_claim_details --claim_id 23 --clinic_pkey 034e1e7c10c7f79a67fa652e5929947186d0cf23df4a67136596f45919413957b6 --url http://sawtooth-rest-api:8008
    EVENT HEX       CLAIM ID        CLINIC PKEY     EVENT           DESCRIPTION     EVENT TIME     
    3d804905dd1b3c535fa3bbfeb700e203ba085b08a1b17a282f1cb2ed5484c3845cc4d3 23              034e1e7c10c7f79a67fa652e5929947186d0cf23df4a67136596f45919413957b6 0               Doctor pkey: 03341e263b90de5ee7962b0dc88543a6f7fa18e8fdb0c01adba7d214a86f8985a2, assigned to claim: 3d804904dd1b3c535fa3bbfeb700e20359b62eb71c236e2f42a77b660f3838cc396b62 1541509428.2187653
    ```
       
1. Perform first visit to a doctor:

    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python first_visit --username clinicCLI --claim_id 23 --doctor_pkey 03341e263b90de5ee7962b0dc88543a6f7fa18e8fdb0c01adba7d214a86f8985a2 --description first-visit --url http://sawtooth-rest-api:8008
       Response: {
           "link": "http://sawtooth-rest-api:8008/batch_statuses?id=b3b376986b4b4481c2a75f821fbf81a9a59f6cf73a6db649ee25282d4f9f2b7f431192d2eaf5cb1789cea4b4a6de8344777987af4427d234acb0931ba7fb9ffa"
    }
    ```
 
1. Pass tests in scope of this claim:

    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python pass_tests --username clinicCLI --claim_id 23 --description passtests1 --url http://sawtooth-rest-api:8008
       Response: {
           "link": "http://sawtooth-rest-api:8008/batch_statuses?id=31014921dbbec97417611a7153dd2d5cbb11bf715e132585135292b55c77e14e095e050aed51df0cf90e90706dcff5c87348f01ace136cdec0210194916fc9d7"
    }
    ```

1. Eat pills in scope of this claim:

    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python eat_pills --username clinicCLI --claim_id 23 --description eat-pills --url http://sawtooth-rest-api:8008
       Response: {
           "link": "http://sawtooth-rest-api:8008/batch_statuses?id=2d7ed250f925a4aae55ab8b026ff818f184e7feb5e847a1ac626e2ea7e9ca51b43834cd63955fe824d31a1cc4b4b15c7f20a48c3055045c85c0cc6c6ec7257b2"
    }
    ```

1. Attend procedures in scope of this claim:

    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python attend_procedures --username clinicCLI --claim_id 23 --description attend-procedures --url http://sawtooth-rest-api:8008
       Response: {
           "link": "http://sawtooth-rest-api:8008/batch_statuses?id=97ce6bb0c508c007f991b9e0b91c7f434ee5bb0d300ca3f392e42265a8ef63353f9539151c7d2cb65787fc9b838bdb5aa2a5adb13e5dee1fa9f986bb5f483d86"
    }
    ```

1. Visit doctor once again:
    
    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python next_visit --username clinicCLI --claim_id 23 --doctor_pkey 0376c6baf12dd35240203b457ed7c5256716faa13ae93bbbe13aadc3284863e6db --description next-visit --url http://sawtooth-rest-api:8008
       Response: {
           "link": "http://sawtooth-rest-api:8008/batch_statuses?id=16adc516bbab7419d76574df1489a9c71c42b2f881651a5047c73438830de31b742634dbe2e64e2e6a94f4333923d80c694f9ade7b4c66338a572f7b74f7ac44"
    }
    ```

1. Check claim details again:
    
    ```bash
    root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python list_claim_details --claim_id 23 --clinic_pkey 034e1e7c10c7f79a67fa652e5929947186d0cf23df4a67136596f45919413957b6 --url http://sawtooth-rest-api:8008
    EVENT HEX       CLAIM ID        CLINIC PKEY     EVENT           DESCRIPTION     EVENT TIME     
    3d804905dd1b3c535fa3bbfeb700e20354030aea0ed54f82ab9b779cbcb7560a858ebe 23              034e1e7c10c7f79a67fa652e5929947186d0cf23df4a67136596f45919413957b6 1               Doctor pkey: 03341e263b90de5ee7962b0dc88543a6f7fa18e8fdb0c01adba7d214a86f8985a2, claim hex: 3d804904dd1b3c535fa3bbfeb700e20359b62eb71c236e2f42a77b660f3838cc396b62, description: first-visit 1541504687.8921192
    3d804905dd1b3c535fa3bbfeb700e203ba085b08a1b17a282f1cb2ed5484c3845cc4d3 23              034e1e7c10c7f79a67fa652e5929947186d0cf23df4a67136596f45919413957b6 0               Doctor pkey: 03341e263b90de5ee7962b0dc88543a6f7fa18e8fdb0c01adba7d214a86f8985a2, assigned to claim: 3d804904dd1b3c535fa3bbfeb700e20359b62eb71c236e2f42a77b660f3838cc396b62 1541509428.2187653
    3d804905dd1b3c535fa3bbfeb700e203b23085a0e68cb1f86076db6f6bc90bde881bb2 23              034e1e7c10c7f79a67fa652e5929947186d0cf23df4a67136596f45919413957b6 3               attend-procedures 1541505164.3952157
    3d804905dd1b3c535fa3bbfeb700e20378144e442c568e9ac5bad20b049e8bbb393170 23              034e1e7c10c7f79a67fa652e5929947186d0cf23df4a67136596f45919413957b6 5               Doctor pkey: 0376c6baf12dd35240203b457ed7c5256716faa13ae93bbbe13aadc3284863e6db, claim hex: 3d804904dd1b3c535fa3bbfeb700e20359b62eb71c236e2f42a77b660f3838cc396b62, description: next-visit 1541509924.4827342
    3d804905dd1b3c535fa3bbfeb700e203b3aa45d6f46de6d84bd31ef0e6036e535eca95 23              034e1e7c10c7f79a67fa652e5929947186d0cf23df4a67136596f45919413957b6 2               passtests1      1541504968.6052659
    3d804905dd1b3c535fa3bbfeb700e20398d7788559d7a65d23917cddfbe928b7bbbd9d 23              034e1e7c10c7f79a67fa652e5929947186d0cf23df4a67136596f45919413957b6 4               eat-pills       1541505068.717659
    ```
    
Finally, you may see event actions performed for this claim stored into blockchain and displayed by the command

# Scaling

To be defined
