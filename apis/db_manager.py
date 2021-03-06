from datetime import datetime

import pytz
from django.core import serializers
from django.db import transaction
from django.utils.timezone import make_aware

from apis.constants.error_code import ERROR_EVENT_NON_EXIST, ERROR_DATE_INVALID, \
    ERROR_UNKNOWN_EVENT_TYPE, ERROR_EVENT_UNAVAILABLE, ERROR_PAGE_EXCEEDED, ERROR_UNKNOWN_OP_TYPE, \
    ERROR_DAILY_EVENT_LIMITS_EXCEEDED, ERROR_UNAUTHORIZED_OPERATION
from apis.constants.util_constants import EVENT_TYPE_OPTIONS, STATUS_QUOTA_FULL, STATUS_ENDED, PARTICIPATE, \
    UNPARTICIPATE, \
    STATUS_CLOSED, STATUS_OPEN, SORT_KEYWORD, EVENT_DAILY_LIMIT
from apis.models import User, EventTab, ParticipateTab, ViewHistoryTab
from apis.utils import get_error_response_dict

tz = pytz.timezone('Asia/Singapore')


def get_user(uid):
    user = User.objects.filter(pk=uid)
    if user:
        return user.first()
    else:
        return None


def check_user_info(user_data):
    check_email = User.objects.filter(email=user_data['email'])
    check_user = User.objects.filter(email=user_data['username'])
    if check_email or check_user:
        return True
    else:
        return False


def create_new_event(event_data, user):
    if user.events_created_daily >= EVENT_DAILY_LIMIT:
        return False, get_error_response_dict("maximum daily limit exceeded",
                                              error_code=ERROR_DAILY_EVENT_LIMITS_EXCEEDED)

    is_open_ended = event_data.get('is_open_ended', '')
    event_start_date_str = event_data.get('event_start_date', '')
    if not event_start_date_str:
        return False, get_error_response_dict("incorrect format of event start date", error_code=ERROR_DATE_INVALID)
    try:
        event_start_time = datetime.strptime(event_start_date_str, '%Y-%m-%d %H:%M')
        event_start_time = make_aware(event_start_time, timezone=tz)
    except:
        return False, get_error_response_dict("invalid date format", error_code=ERROR_DATE_INVALID)

    event_end_date_str = event_data.get('event_end_date', '')
    if not event_end_date_str and is_open_ended:
        # if open ended, make event end time equals event start time
        event_end_time = event_start_time
    elif not event_end_date_str and not is_open_ended:
        return False, get_error_response_dict("non-open-ended event must specify event end time",
                                              error_code=ERROR_DATE_INVALID)
    else:
        try:
            event_end_time = datetime.strptime(event_end_date_str, '%Y-%m-%d %H:%M')
            event_end_time = make_aware(event_end_time, timezone=tz)
        except:
            return False, get_error_response_dict("invalid date format", error_code=ERROR_DATE_INVALID)

    now = datetime.now(event_start_time.tzinfo)
    if event_start_time < now or event_end_time < now:
        return False, get_error_response_dict("invalid event start/end time", error_code=ERROR_DATE_INVALID)

    event_data['event_start_date'] = event_start_time
    event_data['event_end_date'] = event_end_time
    event = EventTab(**event_data)
    event.event_creator = user.pk
    event.save()
    user.events_created_daily = user.events_created_daily + 1
    user.save()
    return True, event


def get_filtered_events(filter_options):
    # date range check
    date_begin = filter_options.get('date_begin', '')
    date_end = filter_options.get('date_end', '')

    events = EventTab.objects.exclude(state=STATUS_ENDED)
    # If only specify date_begin, will get all events starts after the specified date so far
    if date_begin and not date_end:
        try:
            filter_start_time = datetime.strptime(date_begin, '%Y-%m-%d %H:%M')
        except:
            return False, get_error_response_dict("invalid date format", error_code=ERROR_DATE_INVALID)
        events = events.filter(event_start_date__gte=filter_start_time)

    elif not date_begin and date_end:
        return False, get_error_response_dict("unsupported filter option, please specify event start time",
                                              error_code=ERROR_DATE_INVALID)

    elif date_begin and date_end:
        try:
            filter_start_time = datetime.strptime(date_begin, '%Y-%m-%d %H:%M')
            filter_end_time = datetime.strptime(date_end, '%Y-%m-%d %H:%M')
        except:
            return False, get_error_response_dict("invalid date format", error_code=ERROR_DATE_INVALID)
        events = events.filter(event_start_date__gte=filter_start_time).filter(
            event_end_date__lte=filter_end_time)

    # filter by event type
    event_type = filter_options.get('event_type', None)
    if event_type:
        if int(event_type) not in EVENT_TYPE_OPTIONS:
            return False, get_error_response_dict("unknown event type", error_code=ERROR_UNKNOWN_EVENT_TYPE)
        events = events.filter(event_type=event_type)

    # keyword matching
    keyword = filter_options.get('keyword', None)
    if keyword:
        events = events.filter(name__contains=keyword)

    # sorting
    sort_by = filter_options.get("sort_by", None)
    if sort_by:
        sort_keyword = SORT_KEYWORD[sort_by]
        if filter_options.get('is_reverse_sort', None):
            sort_keyword = "-" + sort_keyword
        events = events.order_by(sort_keyword)

    total_pages = 0
    if events.count() > 0:
        # pagination
        page_limit = int(filter_options["page_limit"])
        page_num = int(filter_options["page_num"])

        total_pages = -(-events.count() // 20)
        if total_pages < page_num:
            return False, get_error_response_dict("max pages exceeded", error_code=ERROR_PAGE_EXCEEDED)
        else:
            page_index_begin = page_limit * (page_num - 1)
            page_index_end = min(page_limit * page_num, events.count())
            events = events[page_index_begin:page_index_end]
    return True, {"events": serializers.serialize('json', events), "total_pages": total_pages}


@transaction.atomic
def build_participate(user, eid, op_type):
    event = EventTab.objects.select_for_update().filter(id=eid)
    participate = ParticipateTab.objects.select_for_update().filter(eid=eid, pid=user.pk)
    if participate:
        participate = participate.first()
    if event:
        if op_type == PARTICIPATE:
            event = event.first()
            if (participate and participate.state == STATUS_CLOSED) or not participate:
                if event.state == STATUS_OPEN and event.num_participants < event.max_quota:
                    event.num_participants = event.num_participants + 1
                    if event.num_participants == event.max_quota:
                        event.state = STATUS_QUOTA_FULL
                    event.save()

                    if participate:
                        participate.state = STATUS_OPEN
                        participate.save()
                    else:
                        participate = ParticipateTab(eid=eid, pid=user.pk, state=STATUS_OPEN)
                        participate.save()
                    return True, {"is_redundant": False, "quota_left": event.max_quota - event.num_participants,
                                  "max_quota": event.max_quota}
                else:
                    return False, get_error_response_dict("event quota full", error_code=ERROR_EVENT_UNAVAILABLE)
            else:
                # already has participate record of status open, don't care.
                return True, {"is_redundant": True, "quota_left": event.max_quota - event.num_participants,
                              "max_quota": event.max_quota}
        elif op_type == UNPARTICIPATE:
            event = event.first()
            if participate and participate.state == STATUS_OPEN:
                if event.num_participants == event.max_quota:
                    event.state = STATUS_OPEN
                event.num_participants = event.num_participants - 1
                event.save()

                participate.state = STATUS_CLOSED
                participate.save()
                return True, {"is_redundant": False, "quota_left": event.max_quota - event.num_participants,
                              "max_quota": event.max_quota}
            else:
                if not participate:
                    participate = ParticipateTab(eid=eid, pid=user.pk, state=STATUS_CLOSED)
                    participate.save()
                return True, {"is_redundant": True, "quota_left": event.max_quota - event.num_participants,
                              "max_quota": event.max_quota}
        else:
            return False, get_error_response_dict("unknown op type", error_code=ERROR_UNKNOWN_OP_TYPE)
    else:
        return False, get_error_response_dict("event does not exist", error_code=ERROR_EVENT_NON_EXIST)


@transaction.atomic
def record_view_history(user, eid):
    record = ViewHistoryTab.objects.select_for_update().filter(pid=user.pk, eid=eid)
    if record:
        record = record.first()
        record.count = record.count + 1
        record.save()
    else:
        record = ViewHistoryTab(pid=user.pk, eid=eid)
        record.save()
    return record.count


def fetch_user_all_created_events(user):
    events = EventTab.objects.filter(event_creator=user.pk)
    events = serializers.serialize('json', events)
    return events


def fetch_user_all_participated_events(user):
    participates = ParticipateTab.objects.filter(pid=user.pk)
    event_ids = []
    for participate in participates:
        event_ids.append(participate.eid)
    events = EventTab.objects.filter(id__in=event_ids)
    events = serializers.serialize('json', events)
    return events


def fetch_all_participators(eid, user):
    # only event owner can see the list of participators.
    event = EventTab.objects.filter(id=eid)
    if event:
        event = event.first()
        if event.event_creator != user.pk:
            return False, get_error_response_dict("unauthorized operation", error_code=ERROR_UNAUTHORIZED_OPERATION)
        participates = list(ParticipateTab.objects.filter(eid=eid).values_list('pid', flat=True))
        users = User.objects.filter(pk__in=participates)
        return True, {"participators": serializers.serialize('json', users, fields=('pk', 'username', 'email'))}
    else:
        return False, get_error_response_dict("event does not exist", error_code=ERROR_EVENT_NON_EXIST)


