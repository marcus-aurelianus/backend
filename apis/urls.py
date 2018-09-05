from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'v1/login/', user_login),
    url(r'v1/logout/', user_logout),
]
