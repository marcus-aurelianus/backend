from apis.constants.util_constants import EVENT_TYPE_OPTIONS, PARTICIPATE, UNPARTICIPATE, SORT_OPTIONS

login_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "minLength": 6,
            "maxLength": 18,
        },

        "password": {
            "type": "string",
            "minLength": 6,
            "maxLength": 18,
        },
    },
    "required": ["username", "password"]
}

register_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "minLength": 6,
            "maxLength": 18,
        },

        "password": {
            "type": "string",
            "minLength": 6,
            "maxLength": 18,
        },

        "email": {
            "type": "string",
            "format": "email"
        },

        "phone_number": {
            "type": "string",
            "minLength": 8,
            "maxLength": 8
        }
    },
    "required": ["username", "password", "email", "phone_number"]
}

token_schema = {
    "type": "object",
    "properties": {
        "user_token": {
            "type": "string"
        },

        "uid": {
            "type": "string"
        }
    }
}


# user could only specify event start date if the event is open-ended. In that case, specify event_end_date with
# same value as event_start_date

event_schema = {
    "type": "object",
    "properties": {
        "event_title": {
            "type": "string",
            "maxLength": 48,
        },

        "event_desc": {
            "type": "string",
            "maxLength": 1024,
        },

        "event_type": {
            "type": "integer",
            "multipleOf": 1.0,
            "enum": EVENT_TYPE_OPTIONS
        },

        "max_quota": {
            "type": "integer",
            "multipleOf": 1.0
        },

        "extra_info_dict": {
            "type": "object",
        },

        "event_start_date": {
            "type": "string",
            "minLength": 16,
            "maxLength": 16
        },

        "event_end_date": {
            "type": "string",
            "minLength": 16,
            "maxLength": 16
        },

        "is_open_ended": {
            "type": "boolean"
        }
    },

    "required": ["event_title", "event_desc", "event_type", "max_quota", "event_start_date",
                 "is_open_ended"]
}

filter_schema = {
    "type": "object",
    "properties": {
        "date_begin": {
            "type": "string",
            "minLength": 16,
            "maxLength": 16
        },

        "date_end": {
            "type": "string",
            "minLength": 16,
            "maxLength": 16
        },

        "event_type": {
            "type": "string",
        },

        "page_limit": {
            "type": "string",
        },

        "page_num": {
            "type": "string",
        },

        "sort_by": {
          "type": "string",
          "enum": SORT_OPTIONS
        },

        "is_reverse_sort": {
            "type": "boolean",
        },

        "keywords": {
            "type": "string"
        }

    },

    "required": ["page_limit", "page_num"]
}


participate_schema = {
    "type": "object",
    "properties": {
        "eid": {
            "type": "string"
        },

        "op_type": {
            "type": "integer",
            "enum": [PARTICIPATE, UNPARTICIPATE]
        }
    }
}

record_schema = {
    "type": "object",
    "properties": {
        "eid": {
            "type": "string"
        },
    }
}

event_participators_schema = {
    "type": "object",
    "properties": {
        "eid": {
            "type": "string"
        },
    }
}