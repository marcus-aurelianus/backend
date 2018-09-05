from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'v1/login/', login),
    url(r'v1/logout/', logout),
]
