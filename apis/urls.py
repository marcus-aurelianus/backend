from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'v1/login/', user_login),
    url(r'v1/logout/', user_logout),
    url(r'v1/register/', user_register),
    url(r'v1/create_event/', post_event),
]
