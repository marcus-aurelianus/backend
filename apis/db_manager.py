from datetime import datetime

from apis.models import User, EventTab


def check_user_info(user_data):
    check_email = User.objects.filter(email=user_data['email'])
    check_user = User.objects.filter(email=user_data['username'])
    if check_email or check_user:
        return True
    else:
        return False


def create_new_event(event_data, user):
    event_date_str = event_data.get('event_date', '')
    event_time = datetime.strptime(event_date_str, '%Y-%m-%d %H:%M')
    event_data['event_date'] = event_time
    event = EventTab(**event_data)
    event.event_creator = user.pk
    event.save()
    return event
