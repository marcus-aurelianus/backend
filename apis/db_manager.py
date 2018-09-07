from datetime import datetime

import pytz
from django.core import serializers
from django.utils.timezone import make_aware

from apis.constants.error_code import ERROR_EVENT_NON_EXIST
from apis.constants.util_constants import EVENT_TYPE_OPTIONS, EVENT_QUOTA_FULL, EVENT_ENDED
from apis.models import User, EventTab, ParticipateTab
from apis.utils import get_response_dict

tz = pytz.timezone('Asia/Singapore')


def check_user_info(user_data):
    check_email = User.objects.filter(email=user_data['email'])
    check_user = User.objects.filter(email=user_data['username'])
    if check_email or check_user:
        return True
    else:
        return False


def create_new_event(event_data, user):
    is_open_ended = event_data.get('is_open_ended', '')
    event_start_date_str = event_data.get('event_start_date', '')
    if not event_start_date_str:
        return False, get_response_dict("incorrect format for event start date")
    try:
        event_start_time = datetime.strptime(event_start_date_str, '%Y-%m-%d %H:%M')
        event_start_time = make_aware(event_start_time, timezone=tz)
    except:
        return False, get_response_dict("invalid date format")

    event_end_date_str = event_data.get('event_end_date', '')
    if not event_end_date_str and is_open_ended:
        # if open ended, make event end time equals event start time
        event_end_time = event_start_time
    elif not event_end_date_str and not is_open_ended:
        return False, get_response_dict("non-open-ended event must specify event end time")
    else:
        try:
            event_end_time = datetime.strptime(event_end_date_str, '%Y-%m-%d %H:%M')
            event_end_time = make_aware(event_end_time, timezone=tz)
        except:
            return False, get_response_dict("invalid date format")

    now = datetime.now(event_start_time.tzinfo)
    if event_start_time < now or event_end_time < now:
        return False, get_response_dict("invalid event start/end time")

    event_data['event_start_date'] = event_start_time
    event_data['event_end_date'] = event_end_time
    event = EventTab(**event_data)
    event.event_creator = user.pk
    event.save()
    return True, event


def get_filtered_events(filter_options):
    # date range check
    date_begin = filter_options.get('date_begin', '')
    date_end = filter_options.get('date_end', '')

    events = EventTab.objects.exclude(state=EVENT_ENDED)
    # If only specify date_begin, will get all events starts after the specified date so far
    if date_begin and not date_end:
        try:
            filter_start_time = datetime.strptime(date_begin, '%Y-%m-%d %H:%M')
        except:
            return False, get_response_dict("invalid date format")
        events = events.filter(event_start_date__gte=filter_start_time)

    elif not date_begin and date_end:
        return False, get_response_dict("unsupported filter option, please specify event start time")

    elif date_begin and date_end:
        try:
            filter_start_time = datetime.strptime(date_begin, '%Y-%m-%d %H:%M')
            filter_end_time = datetime.strptime(date_end, '%Y-%m-%d %H:%M')
        except:
            return False, get_response_dict("invalid date format")
        events = events.filter(event_start_date__gte=filter_start_time).filter(
            event_end_date__lte=filter_end_time)

    # filter by event type
    event_type = filter_options.get('event_type', '')
    if event_type:
        if int(event_type) not in EVENT_TYPE_OPTIONS:
            return False, get_response_dict("unknown event type")
        events = events.filter(event_type=event_type)

    # sorting
    sort_by = filter_options.get("sort_by", '')
    if sort_by:
        if filter_options.get('is_reverse_sort', ''):
            sort_by = "-" + sort_by
        events = events.order_by(sort_by)

    total_pages = 0
    if events.count() > 0:
        # pagination
        page_limit = int(filter_options["page_limit"])
        page_num = int(filter_options["page_num"])

        total_pages = -(-events.count() // 20)
        if total_pages < page_num:
            return False, get_response_dict("max pages exceeded")
        else:
            page_index_begin = page_limit * (page_num - 1)
            page_index_end = min(page_limit * page_num, events.count())
            events = events[page_index_begin:page_index_end]
    return True, {"events": serializers.serialize('json', events), "total_pages": total_pages}


def build_participate(user, eid):
    event = EventTab.objects.filter(id=eid)
    if event:
        event = event.first()
        if event.num_participants < event.max_quota:
            event.num_participants = event.num_participants + 1
            if event.num_participants == event.max_quota:
                event.state = EVENT_QUOTA_FULL
            event.save()
            participate = ParticipateTab(eid=eid, pid=user.pk)
            participate.save()
            return True, participate
        else:
            return False, get_response_dict("event max quota exceed")
    else:
        return False, get_response_dict("event does not exist", error_code=ERROR_EVENT_NON_EXIST)






