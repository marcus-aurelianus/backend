import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from apis.constants import EVENT_OPEN, QUOTA_UNLIMITED, EVENT_TYPE_DEFAULT, FACEBOOK_USER


class User(AbstractUser):
    third_party_connection = models.IntegerField(FACEBOOK_USER)


class EventTab(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    event_organizer = models.CharField(max_length=48)
    event_title = models.CharField(max_length=48)
    event_desc = models.CharField(max_length=1024)
    event_creator = models.UUIDField()
    event_type = models.IntegerField(default=EVENT_TYPE_DEFAULT)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    state = models.IntegerField(default=EVENT_OPEN)
    max_quota = models.IntegerField(default=QUOTA_UNLIMITED)
    num_participants = models.IntegerField(default=0)
    extra_info_dict = models.CharField(max_length=1024)

    class Meta:
        db_table = 'event_tab'


class ParticipateTab(models.Model):
    eid = models.UUIDField(db_index=True)
    pid = models.UUIDField(db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'participate_tab'


class LikeTab(models.Model):
    eid = models.UUIDField(db_index=True)
    pid = models.UUIDField(db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'like_tab'
