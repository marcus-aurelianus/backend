from authy.api import AuthyApiClient

from backend.settings import AUTHY_API_KEY

authy_api = AuthyApiClient(AUTHY_API_KEY)

COUNTRY_CODE_SINGAPORE = 65


def authy_create_user(phone_number, email):
    user = authy_api.users.create(email, phone_number, COUNTRY_CODE_SINGAPORE)
    if user.ok():
        return user
    else:
        return None


def send_sms(authy_id):
    sms = authy_api.users.request_sms(authy_id)
    if sms.ok():
        return sms
    else:
        return None


def verify_token(authy_id, user_token):
    verification = authy_api.tokens.verify(authy_id, user_token, {"force": True})
    return verification.ok()

