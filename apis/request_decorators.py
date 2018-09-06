from django.http import JsonResponse
from jsonschema import Draft4Validator

error_response_incorrect_format = {"status": 'failed', "desc": "incorrect data format"}
error_response_unexpected_error = {"status": 'failed', "desc": "oops, unexpected error"}


# Data format validator
def validate_data(data_schema):
    def wrapper(func):
        def wrap(request, *args, **kwargs):
            data_validator = Draft4Validator(data_schema)
            if request.method == 'GET':
                data = request.GET
            elif request.method == 'POST':
                data = request.POST
            else:
                return JsonResponse(error_response_incorrect_format)
            data = data.dict()
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
        try:
            response_data = func(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return JsonResponse(error_response_unexpected_error)
        return JsonResponse(response_data)

    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap
