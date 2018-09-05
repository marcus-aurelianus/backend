import json

from django.http import JsonResponse
from jsonschema import Draft4Validator

error_response_incorrect_format = {"status": 'failed', "desc": "incorrect data format"}
error_response_unexpected_error = {"status": 'failed', "desc": "oops, unexpected error"}


# Data format validator
def validate_data(data_schema):
    def wrapper(function):
        def wrap(request, *args, **kwargs):
            data_validator = Draft4Validator(data_schema)
            if request.method == 'get':
                data = request.GET
            elif request.method == 'post':
                data = request.POST
            else:
                return JsonResponse(error_response_incorrect_format)
            if data_validator.is_valid(data):
                request.data = data
                return function(request, *args, **kwargs)
            else:
                return JsonResponse(error_response_incorrect_format)

        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
    return wrapper


def json_response(function):
    def wrap(request, *args, **kwargs):
        try:
            response_data = function(request, *args, **kwargs)
        except:
            return JsonResponse(error_response_unexpected_error)
        return JsonResponse(json.dumps(response_data))

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
