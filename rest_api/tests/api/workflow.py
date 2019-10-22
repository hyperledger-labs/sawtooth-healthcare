import logging
import unittest
from uuid import uuid4
import requests
import urllib.parse
from json import JSONDecodeError
import types

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


REST_URL = 'http://localhost:8040'


class WorkflowTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        cls.client.get_and_set_all_clients()

    def test_001_create_clinic(self):
        clinics = Clinics()
        name = 'Clinic_test_001_' + uuid4().hex
        response = clinics.register(name)
        self.assertEqual({'status': 'DONE'}, response.text)
        self.assertEqual(200, response.status_code)

        response = clinics.register(name)
        self.assertEqual("""Error: InvalidTransaction('Invalid action: Clinic already exists: {}',)""".format(name), response.text)
        self.assertEqual(400, response.status_code)

    def test_002_create_patient(self):
        patients = Patients()
        name = 'Patient_name_test_002_' + uuid4().hex
        surname = 'Patient_surname_test_002_' + uuid4().hex
        response = patients.register(name, surname)
        self.assertEqual({'status': 'DONE'}, response.text)
        self.assertEqual(200, response.status_code)

        response = patients.register(name, surname)
        self.assertEqual("""'Error: InvalidTransaction('Invalid action: Patient already exists: {}',)'""".format(name), response.text)
        self.assertEqual(400, response.status_code)

    def test_003_create_doctor(self):
        doctors = Doctors()
        name = 'Doctor_name_test_003_' + uuid4().hex
        surname = 'Doctor_surname_test_003_' + uuid4().hex
        response = doctors.register(name, surname)
        self.assertEqual({'status': 'DONE'}, response.text)
        self.assertEqual(200, response.status_code)

        response = doctors.register(name, surname)
        self.assertEqual("""'Error: InvalidTransaction('Invalid action: Doctor already exists: {}',)'""".format(name), response.text)
        self.assertEqual(400, response.status_code)

    def test_004_patient_grants_clinic_to_access_his_data(self):
        clinic = Clinics()
        response = clinic.get_clinics(client_key=self.client.patient)
        clinic_key = response.get_clinic_public_key()

        patient = Patients()
        response = patient.grant_access(self.client.patient, clinic_key)
        self.assertEqual({'status': 'DONE'}, response.text)
        self.assertEqual(200, response.status_code)

    def test_005_clinic_registers_new_claim(self):
        patient = Patients()
        response = patient.get_patients_list(client_key=self.client.clinic)
        pk = response.get_patient_public_key()

        claim = Claims()
        response = claim.register(self.client.clinic, pk,
                                  description='Claim_description_test_005_' + uuid4().hex,
                                  claim_id='Claim_id_test_005_' + uuid4().hex)

        self.assertEqual({'status': 'DONE'}, response.text)
        self.assertEqual(200, response.status_code)

    def test_006_patient_grants_doctor_to_access_his_data(self):
        doctor = Doctors()
        response = doctor.get_doctors(client_key=self.client.patient)
        pk = response.get_doc_public_key()

        patient = Patients()
        response = patient.grant_access(self.client.patient, pk)
        self.assertEqual({'status': 'DONE'}, response.text)
        self.assertEqual(200, response.status_code)

    def test_007_doctor_search_and_update_claim(self):
        LOGGER.info('Clinic searching for the patient in blockchain and registers new claim')
        patient = Patients()
        response = patient.get_patients_list(client_key=self.client.clinic)
        self.assertEqual(200, response.status_code)
        pk = response.get_patient_public_key()
        self.assertIsNotNone(pk, 'Patient was not found')

        claim = Claims()
        claim_id = 'Claim_id_test_007_' + uuid4().hex
        response = claim.register(self.client.clinic, pk,
                                  description='Claim_description_test_007_' + uuid4().hex,
                                  claim_id=claim_id)
        self.assertEqual({'status': 'DONE'}, response.text)

        LOGGER.info('Search claim {} in the claims list'.format(claim_id))
        response = claim.get_claims_list(self.client.doctor)
        self.assertEqual(200, response.status_code)

        client_public_key = response.get_claim(claim_id)['client_pkey']
        self.assertIsNotNone(client_public_key, 'Claim: {} was not found'.format(claim_id))

        LOGGER.info('Doctor updates the claim')
        provided_service = 'Provided_service_test_007_' + uuid4().hex
        response = claim.update(self.client.doctor, client_public_key, claim_id, provided_service)
        self.assertEqual(200, response.status_code)

        response = claim.get_claims_list(self.client.doctor)
        provided_service_current = response.get_claim(claim_id)['provided_service']
        self.assertEqual(provided_service, provided_service_current)

        LOGGER.info('Clinic closes the claim')
        response = claim.close(self.client.clinic,  client_public_key, claim_id, provided_service)
        self.assertEqual(200, response.status_code)
        self.assertEqual({'status': 'DONE'}, response.text)


class RequestBase(object):

    def get(self, path, params=None, headers=None):
        url = urllib.parse.urljoin(REST_URL, path)
        LOGGER.info('Request: GET. URL: {}, PARAMS: {}, HEADERS: {}'.format(url, params, headers))
        r = requests.get(url=url, params=params, headers=headers)
        return self.format_response(r)

    def post(self, api_point, json_data, headers=None):
        url = urllib.parse.urljoin(REST_URL, api_point)
        LOGGER.info('Request: POST. URL: {}, PAYLOAD: {}, HEADERS: {}'.format(url, json_data, headers))
        r = requests.post(url=url, json=json_data, headers=headers)
        return self.format_response(r)

    def format_response(self, response):
        j_obj = JsonResponse()
        try:
            j_obj.status_code = response.status_code
            LOGGER.info('Response: Code {}'.format(j_obj.status_code))
            j_obj.text = response.json()
            LOGGER.info('Response: Text {}'.format(j_obj.text))
        except JSONDecodeError:
            j_obj.text = response.text
        return j_obj


class JsonResponse(object):
    def __init__(self):
        self.status_code = None
        self.text = None


class Client(RequestBase):
    def __init__(self):
        self.clinic = None
        self.doctor = None
        self.insurance = None
        self.lab = None
        self.patient = None

    def get_and_set_all_clients(self):
        response = self.get('/clients/')
        r_data = response.text['data']
        self.clinic, self.doctor, self.insurance, self.lab, self.patient = r_data['clinic'], r_data['doctor'], r_data['insurance'], r_data['lab'], r_data['patient']
        return response.status_code, response


class Clinics(RequestBase):
    def __init__(self):
        self.path = '/clinics/'

    def register(self, name):
        return self.post(self.path, {'name': name})

    def get_clinics(self, client_key):
        response = self.get(self.path, headers={'ClientKey': client_key})
        response.get_clinic_public_key = types.MethodType(self._get_clinic_public_key, response)
        return response

    @staticmethod
    def _get_clinic_public_key(obj):
        return obj.text['data'][0]['public_key']


class Patients(RequestBase):
    def __init__(self):
        self.path = '/patients/'
        self.path_grant = self.path + 'grant/'

    def register(self, name, surname):
        return self.post(self.path, {'name': name, 'surname': surname})

    def grant_access(self, client_key, doc_public_key):
        return self.get('{}{}'.format(self.path_grant, doc_public_key), headers={'ClientKey': client_key})

    def get_patients_list(self, client_key):
        response = self.get(path=self.path, headers={'ClientKey': client_key})
        response.get_patient_public_key = types.MethodType(self._get_patient_public_key, response)
        return response

    @staticmethod
    def _get_patient_public_key(obj):
        return obj.text['data'][0]['public_key']


class Doctors(RequestBase):
    def __init__(self):
        self.path = '/doctors/'

    def register(self, name, surname):
        return self.post(self.path, {'name': name, 'surname': surname})

    def get_doctors(self, client_key):
        response = self.get(self.path, headers={'ClientKey': client_key})
        response.get_doc_public_key = types.MethodType(self._get_doc_public_key, response)
        return response

    @staticmethod
    def _get_doc_public_key(obj):
        return obj.text['data'][0]['public_key']


class Claims(RequestBase):
    def __init__(self):
        self.path = 'claims'
        self.path_update = self.path + '/update/'
        self.path_close = self.path + '/close/'

    def register(self, client_key, public_key, description, claim_id, contract_id=''):
        response = self.post(self.path, json_data={'claim_id': claim_id,
                                                   'contract_id': contract_id,
                                                   'description': description,
                                                   'patient_pkey': public_key},
                             headers={'ClientKey': client_key})
        return response

    def get_claims_list(self, client_key):
        response = self.get(self.path, headers={'ClientKey': client_key})
        response.get_claim = types.MethodType(self._get_claim, response)
        return response

    def update(self, client_key, client_public_key, claim_id, provided_service, contract_id=''):
        response = self.post(self.path_update, json_data={'claim_id': claim_id,
                                                          'client_pkey': client_public_key,
                                                          'contract_id': contract_id,
                                                          'provided_service': provided_service},
                             headers={'ClientKey': client_key})
        return response

    def close(self, client_key, client_public_key, claim_id, provided_service, contract_id=''):
        response = self.post(self.path_close, json_data={'claim_id': claim_id,
                                                         'client_pkey': client_public_key,
                                                         'contract_id': contract_id,
                                                         'provided_service': provided_service},
                             headers={'ClientKey': client_key})
        return response

    @staticmethod
    def _get_claim(obj, claim_id):
        data = obj.text['data']
        for elem in data:
            if elem['id'] == claim_id:
                return elem
        else:
            return None

