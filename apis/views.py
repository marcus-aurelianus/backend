from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apis.authy import authy_create_user, send_sms, verify_token
from apis.constants.error_code import ERROR_INVALID_PASSWORD_USERNAME, ERROR_SERVICE_UNAVAILABLE, \
    ERROR_USER_ALREADY_EXIST, ERROR_UID_NON_EXIST, ERROR_VERIFICATION_FAILED, ERROR_INACTIVATE_ACCOUNT
from apis.constants.util_constants import USER_INACTIVE, USER_ACTIVE
from apis.db_manager import check_user_info, create_new_event, get_filtered_events, build_participate, \
    record_view_history, fetch_user_all_created_events, fetch_user_all_participated_events, fetch_all_participators, get_user
from apis.models import User
from apis.request_decorators import validate_data, json_response, ensure_user_status
from apis.data_schema import login_schema, register_schema, event_schema, filter_schema, participate_schema, \
    record_schema, event_participators_schema, token_schema

from apis.utils import get_error_response_dict

# Remove csrf_exempt decorator when deployed for production.
from backend import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
USER_CREATED_EVENTS_PREFIX = "user_created_events_"
USER_PARTICIPATED_EVENTS_PREFIX = "user_participated_events_"


@csrf_exempt
@validate_data(login_schema)
@json_response
def user_login(request):
    user_data = request.data
    user = authenticate(username=user_data['username'], password=user_data['password'])
    if user is not None:
        if user.state == USER_ACTIVE:
            login(request, user)
            response_data = {
                "status": 'success',
                "username": user.username,
                "email": user.email,
                "uid": user.pk
            }
            return response_data
        else:
            return get_error_response_dict('user account inactivate', error_code=ERROR_INACTIVATE_ACCOUNT)
    else:
        return get_error_response_dict('user name or password incorrect', error_code=ERROR_INVALID_PASSWORD_USERNAME)


@csrf_exempt
@require_http_methods(["GET"])
@ensure_user_status
@json_response
def user_logout(request):
    uid = request.user.pk
    logout(request)
    return {"status": 'success', "uid": uid}


@csrf_exempt
@require_http_methods(["POST"])
@validate_data(register_schema)
@json_response
def user_register_sms(request):
    user_data = request.data
    is_exist = check_user_info(user_data)
    if is_exist:
        return get_error_response_dict('username or email already exists', error_code=ERROR_USER_ALREADY_EXIST)
    else:
        user = User.objects.create_user(**user_data)
        authy_user = authy_create_user(user_data.get("phone_number", ""), user_data.get("email", ""))
        if authy_user:
            user.authy_id = authy_user.id
            user.save()
            sms = send_sms(authy_user.id)
            if sms:
                return {"status": 'success', "desc": "verification code sent through sms", "uid": user.pk}
            else:
                return get_error_response_dict('Service Unavailable', error_code=ERROR_SERVICE_UNAVAILABLE)
        else:
            return get_error_response_dict('Service Unavailable', error_code=ERROR_SERVICE_UNAVAILABLE)


@csrf_exempt
@require_http_methods(["POST"])
@validate_data(token_schema)
@json_response
def user_register_complete(request):
    user_data = request.data
    user = get_user(user_data.get('uid', ''))
    if user:
        if user.state == USER_INACTIVE:
            verify = verify_token(user.authy_id, user_data.get('user_token', ''))
            if verify:
                user.state = USER_ACTIVE
                user.save()
                return {"status": 'success', "uid": user.id}
            else:
                return get_error_response_dict('verification failed', error_code=ERROR_VERIFICATION_FAILED)
        else:
            return get_error_response_dict('user already activated', error_code=ERROR_USER_ALREADY_EXIST)
    else:
        return get_error_response_dict('invalid uid', error_code=ERROR_UID_NON_EXIST)


@require_http_methods(["GET"])
@ensure_user_status
@json_response
def user_events(request):
    cache_result = cache.get(USER_CREATED_EVENTS_PREFIX+str(request.user.pk))
    if cache_result:
        return cache_result
    else:
        events = fetch_user_all_created_events(request.user)
        response = {"status": 'success', "events": events}
        cache.set(USER_CREATED_EVENTS_PREFIX+str(request.user.pk), response, CACHE_TTL)
        return response


@require_http_methods(["GET"])
@ensure_user_status
@json_response
def user_participated_events(request):
    cache_result = cache.get(USER_PARTICIPATED_EVENTS_PREFIX+str(request.user.pk))
    if cache_result:
        return cache_result
    else:
        events = fetch_user_all_participated_events(request.user)
        response = {"status": 'success', "events": events}
        cache.set(USER_PARTICIPATED_EVENTS_PREFIX+str(request.user.pk), response, CACHE_TTL)
        return response


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
        return {"status": 'success', "event_id": event.id, "events_created_today": request.user.events_created_daily}
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
        return {"status": 'success', **data}
    else:
        return {"status": 'failed', **data}


@csrf_exempt
@require_http_methods(["POST"])
@ensure_user_status
@validate_data(record_schema)
@json_response
def record_history_views(request):
    user = request.user
    eid = request.data['eid']
    count = record_view_history(user, eid)
    return {"status": 'success', "views_count": count}


@csrf_exempt
@require_http_methods(["GET"])
@ensure_user_status
@validate_data(event_participators_schema)
@json_response
def event_participators(request):
    user = request.user
    eid = request.data['eid']
    flag, data = fetch_all_participators(eid, user)
    if flag:
        return {"status": 'success', **data}
    else:
        return {"status": 'failed', **data}
