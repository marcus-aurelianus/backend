from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from apis.db_manager import check_user_info, create_new_event
from apis.models import User
from apis.request_decorators import validate_data, json_response
from apis.schema import login_schema, register_schema, event_schema


# Remove csrf_exempt decorator when deployed for production.

@csrf_exempt
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


@csrf_exempt
@login_required
@json_response
def user_logout(request):
    logout(request)
    return {"status": 'success'}


@csrf_exempt
@validate_data(register_schema)
@json_response
def user_register(request):
    user_data = request.data
    is_exist = check_user_info(user_data)
    if is_exist:
        return {"status": 'failed', "desc": 'username or email already exists'}
    else:
        user = User.objects.create_user(**user_data)
        user.save()
        return {"status": 'success', "user_id": user.pk}


@csrf_exempt
@login_required
@validate_data(event_schema)
@json_response
def post_event(request):
    event_data = request.data
    event = create_new_event(event_data, request.user)
    return {"status": 'success', "event_id": event.id}
