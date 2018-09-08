import json

from django.http import JsonResponse
from jsonschema import Draft4Validator

from apis.constants.error_code import ERROR_LOGIN_REQUIRED, ERROR_INVALID_DATA_FORMAT, ERROR_UNEXPECTED
from apis.constants.util_constants import USER_ACTIVE

error_response_incorrect_format = {"status": 'failed', "desc": "incorrect data format",
                                   "error_code": ERROR_INVALID_DATA_FORMAT}
error_response_unexpected_error = {"status": 'failed', "desc": "oops, unexpected error", "error_coe": ERROR_UNEXPECTED}
error_response_login_required = {"status": 'failed', "desc": "login required or you haven't activate your account",
                                 "error_code": ERROR_LOGIN_REQUIRED}


# Data format validator
def validate_data(data_schema):
    def wrapper(func):
        def wrap(request, *args, **kwargs):
            data_validator = Draft4Validator(data_schema)
            if request.method == 'GET':
                data = request.GET.dict()
            elif request.method == 'POST':
                # json data
                data = json.loads(request.body)
            else:
                return JsonResponse(error_response_incorrect_format)
            if data_validator.is_valid(data):
                request.data = data
                return func(request, *args, **kwargs)
            else:
                return JsonResponse(error_response_incorrect_format)

        wrap.__doc__ = func.__doc__
        wrap.__name__ = func.__name__
        return wrap

    return wrapper


def json_response(func):
    def wrap(request, *args, **kwargs):
        status_code = 200
        try:
            response_data = func(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return JsonResponse(error_response_unexpected_error)
        if response_data.get('status') == 'failed':
            status_code = 400
        return JsonResponse(response_data, status=status_code)

    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap


def ensure_user_status(func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.user.state == USER_ACTIVE:
                return func(request, *args, **kwargs)
        return JsonResponse(error_response_login_required, status=401)

    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap
