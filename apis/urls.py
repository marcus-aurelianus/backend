from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'v1/user/login/', user_login),
    url(r'v1/user/logout/', user_logout),
    url(r'v1/user/register/', user_register),

    url(r'v1/user/events_created/', user_events),
    url(r'v1/user/events_participated/', user_participated_events),

    url(r'v1/event/create_event/', post_event),
    url(r'v1/event/list/', events_list),

    url(r'v1/action/participate/', participate_event),


    url(r'v2/action/history_record/', record_history_views),
]
