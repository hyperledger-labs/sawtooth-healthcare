# Sawtooth Healthcare

Sawtooth Healthcare is a blockchain application built on Hyperledger Sawtooth, allowing clinics to keep history regarding petients health and claims on the blockchain. The repo is based on two other repos available on the internet:

https://github.com/hyperledger/sawtooth-marketplace 
https://github.com/hyperledger/sawtooth-core/tree/master/sdk/examples/xo_python

Note, this app is under constant development. All items mentioned in this documentation having "To be defined" will be ready later and updated accordingly. However, recent commits to the repo should functioning properly as described in the doc.

# Worklfow Description

This application covers basic workflow when a patient visit clinic with a claim till he fills good:
- Prerequisites: clinic, doctor and patient entity objects registered in blockchain;
- Parient comes to clinic with a claim;
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

Is nothing but blockchain ledger with predefined API that corresponds to the worflow and aimed to store, update and validate data according to the business process.

## Blockchain Client

Client application generates requests to the server basing on data from clinic and interacts with it.

# Technical Structure (Components)

## Common

This is common module, includes business object entities represented in Protobuf format, used in both client and server sides to serialize/deserialize objects.

Also, it has helper class which includes certain constants, methods for internal needs. 

## Smart Contract (Transaction Processor)

Heart of the app - custom module deployed into blcokchain which validates and handles data transfers.

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

# How it works

This example shows how to use CLI client to operate with blockchain:
1. Prerequisite
	-  Application is up and running;
	- Connect to client container from home directory of this repo (you are connected to the client's container) :

	```shell
$ docker exec -it healthcare-client /bin/bash
root@dcc855da11ec:/project/sawtooth_healthcare#
```

	- There are 3 privat key registered in the container: clinicCLI, doctorCLI, patientCLI (for clinic, doctor and patient accordingly). Every command to be invoked on behalf clinic's key.

1. Ensure clinic is registered in blockchain

	- Check clinics list (the list is empty since no clinic registered in blockhain before):

	```shell
root@f1525454c702:/project/sawtooth_healthcare# healthcare-cli-python list_clinics --url http://sawtooth-rest-api:8008
HEX             NAME            PUBLIC_KEY
```
	- Create new clinic by clinicCLI key:

	```shell
root@f1525454c702:/project/sawtooth_healthcare# healthcare-cli-python create_clinic --username clinicCLI --name Clinic22 --url http://sawtooth-rest-api:8008
Response: {
  "link": "http://sawtooth-rest-api:8008/batch_statuses?id=790786556ad147753620a0bf02a7c7f0d22665bc9a21c8f6e801475eeb9a1b0a1bc5d59d7291056cefc7876f3cd322d522ea6a04e44f3d9976e35233cf19b9a6"
}
```

	- Ensure transaction processed successfully:

	```shell
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
```

	- Get clinics list (newly created item appeared in the list):

	```shell
root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python list_clinics --url http://sawtooth-rest-api:8008
HEX             NAME            PUBLIC_KEY     
3d804901bbfeb700e20359b62eb71c236e2f42a77b660f3838cc396b62db634bc23b87 Clinic22        034e1e7c10c7f79a67fa652e5929947186d0cf23df4a67136596f45919413957b6
```

1. Ensure doctor is registered in blockchain

	- Check doctors list (the list is empty since no doctors registered in blockhain before):

	```shell
root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python list_doctors --url http://sawtooth-rest-api:8008
NAME            SURNAME         PUBLIC_KEY 
```

	- Create new doctor by doctorCLI key:
	
	```shell
root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python create_doctor --username doctorCLI --name Doctor22 --surname DoctorSurname22 --url http://sawtooth-rest-api:8008
Response: {
  "link": "http://sawtooth-rest-api:8008/batch_statuses?id=ffee911434ffd36fc98f2f62d608e5acec7c4193fce2e213ac7809b077339e8a35aced8d0b216644a4755dbd7ec1ac28341b7369fdb6067641ebea6b478d7f17"
}
```
	
	- Ensure transaction processed successfully (link is taken from response in previous step)
	
	```shell
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
	
	```shell
root@dcc855da11ec:/project/sawtooth_healthcare# healthcare-cli-python list_doctors --url http://sawtooth-rest-api:8008
NAME            SURNAME         PUBLIC_KEY     
Doctor22        DoctorSurname22 03341e263b90de5ee7962b0dc88543a6f7fa18e8fdb0c01adba7d214a86f8985a2
```


# Scaling

To be defined