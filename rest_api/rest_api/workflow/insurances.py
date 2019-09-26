from sanic import Blueprint
from sanic import response

from rest_api.insurance_common import transaction as insurance_transaction
from rest_api.consent_common import transaction as consent_transaction
from rest_api.workflow import general, security_messaging
from rest_api.workflow.errors import ApiInternalError, ApiBadRequest

INSURANCES_BP = Blueprint('insurances')


@INSURANCES_BP.get('insurances')
async def get_all_insurances(request):
    """Fetches complete details of all Accounts in state"""
    client_key = general.get_request_key_header(request)
    insurances = await security_messaging.get_insurances(request.app.config.VAL_CONN, client_key)
    insurances_json = []
    for address, ins in insurances.items():
        insurances_json.append({'name': ins.name, 'public_key': ins.public_key})

    return response.json(body={'data': insurances_json},
                         headers=general.get_response_headers())


@INSURANCES_BP.post('insurances')
async def register_new_insurance(request):
    """Updates auth information for the authorized account"""
    # keyfile = common.get_keyfile(request.json.get['signer'])
    required_fields = ['name']
    general.validate_fields(required_fields, request.json)

    name = request.json.get('name')

    insurance_signer = request.app.config.SIGNER_INSURANCE

    client_txn = consent_transaction.create_insurance_client(
        txn_signer=insurance_signer,
        batch_signer=insurance_signer
    )

    insurance_txn = insurance_transaction.create_insurance(
        txn_signer=insurance_signer,
        batch_signer=insurance_signer,
        name=name)

    batch, batch_id = insurance_transaction.make_batch_and_id([client_txn, insurance_txn], insurance_signer)

    await security_messaging.add_insurance(
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
