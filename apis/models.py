import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from apis.constants.util_constants import QUOTA_UNLIMITED, EVENT_TYPE_DEFAULT, DEFAULT_USER, STATUS_OPEN, USER_INACTIVE


class User(AbstractUser):
    events_created_daily = models.IntegerField(default=0)
    third_party_connection = models.IntegerField(default=DEFAULT_USER)
    phone_number = models.CharField(max_length=24)
    authy_id = models.CharField(max_length=24)
    state = models.IntegerField(default=USER_INACTIVE)


class EventTab(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    event_organizer = models.CharField(max_length=48)
    event_title = models.CharField(max_length=48)
    event_desc = models.CharField(max_length=1024)
    event_creator = models.IntegerField(db_index=True, null=False)
    event_type = models.IntegerField(default=EVENT_TYPE_DEFAULT)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    state = models.IntegerField(default=STATUS_OPEN)
    max_quota = models.IntegerField(default=QUOTA_UNLIMITED)
    num_participants = models.IntegerField(default=0)
    extra_info_dict = models.CharField(max_length=1024)
    event_start_date = models.DateTimeField(null=False)
    event_end_date = models.DateTimeField(null=False)
    is_open_ended = models.IntegerField()

    class Meta:
        db_table = 'event_tab'


class ParticipateTab(models.Model):
    eid = models.UUIDField(db_index=True)
    pid = models.IntegerField(db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=STATUS_OPEN)

    class Meta:
        db_table = 'participate_tab'


class ViewHistoryTab(models.Model):
    eid = models.UUIDField(db_index=True)
    pid = models.IntegerField(db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=1)

    class Meta:
        db_table = 'history_view_tab'


class LikeTab(models.Model):
    eid = models.UUIDField(db_index=True)
    pid = models.IntegerField(db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=STATUS_OPEN)

    class Meta:
        db_table = 'like_tab'
