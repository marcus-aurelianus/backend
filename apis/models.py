import uuid

from django.db import models

from apis.constants import EVENT_OPEN, QUOTA_UNLIMITED


class EventTab(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    event_organizer = models.CharField(max_length=48)
    event_title = models.CharField(max_length=48)
    event_desc = models.CharField(max_length=1024)
    event_creator = models.UUIDField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    state = models.IntegerField(default=EVENT_OPEN)
    max_quota = models.IntegerField(default=QUOTA_UNLIMITED)
    num_participants = models.IntegerField(default=0)


class ParticipateTab(models.Model):
    eid = models.UUIDField(db_index=True)
    pid = models.UUIDField(db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)


class LikeTab(models.Model):
    eid = models.UUIDField(db_index=True)
    pid = models.UUIDField(db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)