# Events Related API documentation

Create a nen event for the authenticated User.

**URL** : `/api/v1/event/create_event/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : None

**Data constraints**

[jsonschema](https://json-schema.org/understanding-json-schema/index.html) is used for post data format validation.

```json
{
    "type": "object",
    "properties": {
        "event_title": {
            "type": "string",
            "maxLength": 48
        },

        "event_desc": {
            "type": "string",
            "maxLength": 1024
        },

        "event_type": {
            "type": "integer",
            "multipleOf": 1.0,
            "enum": "[EVENT_TYPE_DEFAULT, EVENT_FACEBOOK]"
        },

        "max_quota": {
            "type": "integer",
            "multipleOf": 1.0
        },

        "extra_info_dict": {
            "type": "object"
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
```

##Notes:
* Each event must have a start date but not necessary an end date. In that case, specify `is_open_ended=false`.
* Event type code:
    * Default: `0`
    * Facebook event: `1`


### Success Response

**Code** : `200 OK`

**Request data examples**

An authenticated user posting an new event. 

```json
{
	"event_title": "BBQ buffet Dinner @ one north", 
	"event_desc": "This is a free dinner", 
	"max_quota": 50, 
	"event_type": 1,
	"event_start_date": "2019-02-07 11:52",
	"is_open_ended": true
}
```

**Response format examples**

```json
{
    "status": "success",
    "event_id": "1dbbe52b-d65a-4bf8-8ee3-f296fd7aa8d1"
}
```
###Error Response

**Code** : `400 BAD REQUEST`

**Request data examples**

Invalid date format.

```json
{
    "status": "failed",
    "desc": "incorrect format of event start date",
    "error_code": 107
}
```

Non-open-ended events does not specify event end time.

```json
{
    "status": "failed",
    "desc": "non-open-ended event must specify event end time",
    "error_code": 107
}
```


## Notes

* `error_code=107` can be resulted from various reasons, please properly check user input before submitting the data.



