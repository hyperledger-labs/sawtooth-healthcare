from sanic import Blueprint
from sanic import response

# from rest_api.common.protobuf import payload_pb2
from rest_api.common import transaction
from rest_api.consent_common import transaction as consent_transaction
from rest_api.workflow import general, security_messaging
from rest_api.workflow.errors import ApiInternalError, ApiBadRequest


PATIENTS_BP = Blueprint('patients')


# @CLINICS_BP.post('accounts')
# async def create_account(request):
#     """Creates a new Account and corresponding authorization token"""
#     required_fields = ['email', 'password']
#     common.validate_fields(required_fields, request.json)
#
#     private_key = request.app.config.CONTEXT.new_random_private_key()
#     signer = CryptoFactory(request.app.config.CONTEXT).new_signer(private_key)
#     public_key = signer.get_public_key().as_hex()
#
#     auth_entry = _create_auth_dict(
#         request, public_key, pr ivate_key.as_hex())
#     await auth_query.create_auth_entry(request.app.config.DB_CONN, auth_entry)
#
#     account = _create_account_dict(request.json, public_key)
#
#     batches, batch_id = transaction_creation.create_account(
#         txn_key=signer,
#         batch_key=request.app.config.SIGNER,
#         label=account.get('label'),
#         description=account.get('description'))
#
#     await messaging.send(
#         request.app.config.VAL_CONN,
#         request.app.config.TIMEOUT,
#         batches)
#
#     try:
#         await messaging.check_batch_status(
#             request.app.config.VAL_CONN, batch_id)
#     except (ApiBadRequest, ApiInternalError) as err:
#         await auth_query.remove_auth_entry(
#             request.app.config.DB_CONN, request.json.get('email'))
#         raise err
#
#     token = common.generate_auth_token(
#         request.app.config.SECRET_KEY,
#         account.get('email'),
#         public_key)
#
#     return response.json(
#         {
#             'authorization': token,
#             'account': account
#         })


# @PATIENTS_BP.get('patients')
# async def get_all_patients(request):
#     """Fetches complete details of all Accounts in state"""
#     client_key = general.get_request_key_header(request)
#     patient_resources = await security_messaging.get_patients(request.app.config.VAL_CONN, client_key)
#     patients = []
#     for entity in patient_resources.entries:
#         pat = payload_pb2.CreatePatient()
#         pat.ParseFromString(entity.data)
#         # permissions = []
#         # for perm in pat.permissions:
#         #     permissions.append(perm)
#         # patients.append({'name': pat.name, 'surname': pat.surname, 'permissions': str(permissions)})
#         patients.append({'name': pat.name, 'surname': pat.surname})
#
#     return response.json(body={'data': patients},
#                          headers=general.get_response_headers())


@PATIENTS_BP.get('patients')
async def get_all_patients(request):
    """Fetches complete details of all Accounts in state"""
    client_key = general.get_request_key_header(request)
    patient_list = await security_messaging.get_patients(request.app.config.VAL_CONN, client_key)
    patient_list_json = []
    for address, pat in patient_list.items():
        patient_list_json.append({
            'public_key': pat.public_key,
            'name': pat.name,
            'surname': pat.surname
        })

    return response.json(body={'data': patient_list_json},
                         headers=general.get_response_headers())


@PATIENTS_BP.post('patients')
async def register_new_patient(request):
    """Updates auth information for the authorized account"""
    # keyfile = common.get_keyfile(request.json.get['signer'])
    required_fields = ['name', 'surname']
    general.validate_fields(required_fields, request.json)

    name = request.json.get('name')
    surname = request.json.get('surname')

    # private_key = common.get_signer_from_file(keyfile)
    # signer = CryptoFactory(request.app.config.CONTEXT).new_signer(private_key)
    patient_signer = request.app.config.SIGNER_PATIENT  # .get_public_key().as_hex()

    client_txn = consent_transaction.create_patient_client(
        txn_signer=patient_signer,
        batch_signer=patient_signer
    )

    patient_txn = transaction.create_patient(
        txn_signer=patient_signer,
        batch_signer=patient_signer,
        name=name,
        surname=surname)

    batch, batch_id = transaction.make_batch_and_id([client_txn, patient_txn], patient_signer)

    await security_messaging.add_patient(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch])

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())


@PATIENTS_BP.get('patients/revoke/<doctor_pkey>')
async def revoke_access(request, doctor_pkey):
    """Updates auth information for the authorized account"""
    client_key = general.get_request_key_header(request)
    client_signer = general.get_signer(request, client_key)
    revoke_access_txn = consent_transaction.revoke_access(
        txn_signer=client_signer,
        batch_signer=client_signer,
        doctor_pkey=doctor_pkey)

    batch, batch_id = transaction.make_batch_and_id([revoke_access_txn], client_signer)

    await security_messaging.revoke_access(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], client_key)

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())


@PATIENTS_BP.get('patients/grant/<doctor_pkey>')
async def grant_access(request, doctor_pkey):
    """Updates auth information for the authorized account"""
    client_key = general.get_request_key_header(request)
    client_signer = general.get_signer(request, client_key)
    grant_access_txn = consent_transaction.grant_access(
        txn_signer=client_signer,
        batch_signer=client_signer,
        doctor_pkey=doctor_pkey)

    batch, batch_id = transaction.make_batch_and_id([grant_access_txn], client_signer)

    await security_messaging.grant_access(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], client_key)

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())

# @ACCOUNTS_BP.get('accounts/<key>')
# async def get_account(request, key):
#     """Fetches the details of particular Account in state"""
#     try:
#         auth_key = common.deserialize_auth_token(
#             request.app.config.SECRET_KEY,
#             request.token).get('public_key')
#     except (BadSignature, TypeError):
#         auth_key = None
#     account_resource = await accounts_query.fetch_account_resource(
#         request.app.config.DB_CONN, key, auth_key)
#     return response.json(account_resource)
#

# @ACCOUNTS_BP.patch('accounts')
# @authorized()
# async def update_account_info(request):
#     """Updates auth information for the authorized account"""
#     token = common.deserialize_auth_token(
#         request.app.config.SECRET_KEY, request.token)
#
#     update = {}
#     if request.json.get('password'):
#         update['hashed_password'] = bcrypt.hashpw(
#             bytes(request.json.get('password'), 'utf-8'), bcrypt.gensalt())
#     if request.json.get('email'):
#         update['email'] = request.json.get('email')
#
#     if update:
#         updated_auth_info = await auth_query.update_auth_info(
#             request.app.config.DB_CONN,
#             token.get('email'),
#             token.get('public_key'),
#             update)
#         new_token = common.generate_auth_token(
#             request.app.config.SECRET_KEY,
#             updated_auth_info.get('email'),
#             updated_auth_info.get('publicKey'))
#     else:
#         updated_auth_info = await accounts_query.fetch_account_resource(
#             request.app.config.DB_CONN,
#             token.get('public_key'),
#             token.get('public_key'))
#         new_token = request.token
#
#     return response.json(
#         {
#             'authorization': new_token,
#             'account': updated_auth_info
#         })

#
# def _create_account_dict(body, public_key):
#     keys = ['label', 'description', 'email']
#
#     account = {k: body[k] for k in keys if body.get(k) is not None}
#
#     account['publicKey'] = public_key
#     account['holdings'] = []
#
#     return account


# def _create_auth_dict(request, public_key, private_key):
#     auth_entry = {
#         'public_key': public_key,
#         'email': request.json['email']
#     }
#
#     auth_entry['encrypted_private_key'] = common.encrypt_private_key(
#         request.app.config.AES_KEY, public_key, private_key)
#     auth_entry['hashed_password'] = bcrypt.hashpw(
#         bytes(request.json.get('password'), 'utf-8'), bcrypt.gensalt())
#
# return auth_entry
