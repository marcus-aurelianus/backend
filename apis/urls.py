from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'v1/user/login/', user_login),
    url(r'v1/user/logout/', user_logout),
    url(r'v1/user/register-request/', user_register_sms),
    url(r'v1/user/register-verify/', user_register_complete),

    url(r'v1/user/events_created/', user_events),
    url(r'v1/user/events_participated/', user_participated_events),

    url(r'v1/event/create_event/', post_event),
    url(r'v1/event/list/', events_list),
    url(r'v1/event/participate/', participate_event),

    # undocumented
    url(r'v1/event/participators/', event_participators),
    url(r'v2/event/history_record/', record_history_views),
]
