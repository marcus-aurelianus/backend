# status=========
STATUS_OPEN = 1
STATUS_CLOSED = 2
STATUS_QUOTA_FULL = 2
STATUS_ENDED = -1
# =====================


QUOTA_UNLIMITED = -1

# event type ==========
EVENT_TYPE_DEFAULT = 0
EVENT_FACEBOOK = 1

EVENT_TYPE_OPTIONS = [EVENT_TYPE_DEFAULT, EVENT_FACEBOOK]
# =====================

# user type
DEFAULT_USER = 0
FACEBOOK_USER = 1
# =====================

PARTICIPATE = 1
UNPARTICIPATE = 2


# sort options
BEGIN_DATE = 0
END_DATE = 1
MAX_QUOTA = 2
CURRENT_PARTICIPANTS = 3

SORT_OPTIONS = [BEGIN_DATE, END_DATE, MAX_QUOTA, CURRENT_PARTICIPANTS]
SORT_KEYWORD = ['event_start_date', 'event_end_date', 'max_quota', 'num_participants']

EVENT_DAILY_LIMIT = 20
