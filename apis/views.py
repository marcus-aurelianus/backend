from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from apis.request_decorators import validate_data
from apis.schema import login_schema, register_schema


@validate_data(login_schema)
def login(request):
    return HttpResponse("Hey, login?")


@login_required()
def logout(request):
    return HttpResponse("Hey, logout?")


@validate_data(register_schema)
def register(request):
    return HttpResponse("Logout")
