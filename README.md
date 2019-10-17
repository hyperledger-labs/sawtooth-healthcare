# Medical Insurance

# About

This is blockchain project based on Hyperledger Sawtooth. This project focuses on interaction between Insurer, 
Insured Person (Patient), and Medical Facility. It covers data gathering flow and manages data access based on 
client’s role.

# Features

## Functional

- Create main participants (like Patient, Doctor, Clinic Desk, Lab and Insurance)
- Clinic Desk registers/closes claim only if with patient’s consent
- Doctor updates existing claim only if with patient’s consent
- Insurance company creates contract with patient/receive an invoice when the claim resolved
- Patient allows/revokes consent to access his data by Clinic Desk/Doctor
- Patient adds pulse items from hardware (Android smartphone in our case)
- Patient adds lab test items
- Any participant has data access according to granted roles/permissions

## Technical

- Private key to store/read data (every participant uses his own private key to store data, and public key to read data)
- Private data access management (every participant has a role assigned with corresponding permissions)
- Docker compliance (every component of this project has separate docker image and fully isolated)
- Various network representation (blockchain network has few options (1 node/Dev-Mode consensus, 3 nodes/PoET consensus/single VM, 3 nodes/PoET consensus/3 separate VMs)
- IoT (android client to send data to blockchain and manage consent)
- Unit tests (automated regression testing)
- Load tests

# Components

- **Consent/Identity/Authorization Management** smart contract (responsible to operate with identity/permission related data)
- **Data Management** smart contract (responsible to handle EHR patient’s data)
- **Insurance/Contract Management** smart contract (responsible to operate with insurance related data)
- **Finance/Invoice Management** smart contract (responsible to operate with finances/invoices)
- **REST-API service** (provides interface between client and blockchain network)
- **Web client** (web page where a participant can operate as one of predefined roles such as doctor, patient etc)
- **Android client** (application link to Play Market for patient to add pulse items and manage consent for own data)
- **CLI client** (command line service to perform basic operations)

# Architecture

![Infrastructure](https://github.com/hyperledger-labs/sawtooth-healthcare/blob/master/MedicalInsurance.png)

# Technology stack

Python/Hyperledger Sawtooth/Docker/Docker-Composer/Protobuf/Setuptools/Sanic/Shell/JMeter/Webpack

# How to setup and run infrastructure (1 node/Dev-Mode consensus)

- Go to root project’s directory
- Clone this repo (if not cloned yet))
- Ensure all containers stopped: “docker-compose down --remove-orphans”
- Get recent data from the repo: “git pull”
- Start new containers: “docker-compose up”

# Demo

TBD
