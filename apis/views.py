from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from apis.request_decorators import validate_data, json_response
from apis.schema import login_schema, register_schema


@validate_data(login_schema)
@json_response
def user_login(request):
    user_data = request.data
    user = authenticate(username=user_data['username'], password=user_data['password'])
    if user is not None:
        login(request, user)
        response_data = {
            "status": 'success',
            "username": user.username,
            "email": user.email,
            "uid": user.pk
        }
        return response_data
    else:
        return {"status": 'failed', "desc": 'user does not exist'}


@login_required()
@json_response
def user_logout(request):
    logout(request)
    return {"status": 'success'}


@validate_data(register_schema)
@json_response
def user_register(request):
    return HttpResponse("Logout")
