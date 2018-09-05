import json

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
