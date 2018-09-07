from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apis.constants.error_code import ERROR_INVALID_PASSWORD_USERNAME
from apis.db_manager import check_user_info, create_new_event, get_filtered_events, build_participate
from apis.models import User
from apis.request_decorators import validate_data, json_response, ensure_user_status
from apis.data_schema import login_schema, register_schema, event_schema, filter_schema, participate_schema


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
        return {"status": 'failed', "desc": 'user name or password incorrect',
                'error_code': ERROR_INVALID_PASSWORD_USERNAME}


@csrf_exempt
@require_http_methods(["GET"])
@ensure_user_status
@json_response
def user_logout(request):
    logout(request)
    return {"status": 'success'}


@csrf_exempt
@require_http_methods(["POST"])
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
@require_http_methods(["POST"])
@ensure_user_status
@validate_data(event_schema)
@json_response
def post_event(request):
    event_data = request.data
    try:
        flag, event = create_new_event(event_data, request.user)
    except:
        return {"status": False, "desc": "oops, unexpected error"}

    if flag:
        return {"status": 'success', "event_id": event.id}
    else:
        return {"status": 'failed', **event}


@require_http_methods(["GET"])
@validate_data(filter_schema)
@json_response
def events_list(request):
    try:
        flag, data = get_filtered_events(request.data)
    except:
        return {"status": False, "desc": "oops, unexpected error"}

    if flag:
        return {"status": 'success', **data}
    else:
        return {"status": 'failed', **data}


@csrf_exempt
@require_http_methods(["POST"])
@ensure_user_status
@validate_data(participate_schema)
@json_response
def participate_event(request):
    user = request.user
    eid = request.data['eid']
    flag, data = build_participate(user, eid, request.data['op_type'])

    if flag:
        return {"status": 'success'}
    else:
        return {"status": 'failed', **data}
