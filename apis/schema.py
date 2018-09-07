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
        }
    },
    "required": ["username", "password"]
}


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
            "multipleOf": 1.0
        },

        "max_quota": {
            "type": "integer",
            "multipleOf": 1.0
        },

        "extra_info_dict": {
            "type": "object",
        },

        "event_date": {
            "type": "string",
            "minLength": 16,
            "maxLength": 16
        }
    },

    "required": ["event_title", "event_desc", "event_type", "max_quota", "event_date"]
}