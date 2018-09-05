from django.http import JsonResponse
from jsonschema import Draft4Validator

error_response = {"status": 'failed', "desc": "incorrect data format"}


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
                return JsonResponse(error_response)
            if data_validator.is_valid(data):
                return function(request, *args, **kwargs)
            else:
                return JsonResponse(error_response)

        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
    return wrapper

