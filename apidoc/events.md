# Events Related API documentation

#### Create a nen event for the authenticated User.

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

## Notes:
* Each event must have a start date but not necessary an end date. In that case, specify `is_open_ended=false`.
* Event type code:
    * Default: `0`
    * Facebook event: `1`
* Each user can only create up to 20 events per day.


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
    "event_id": "1dbbe52b-d65a-4bf8-8ee3-f296fd7aa8d1",
    "events_created_today": 4
}
```
### Error Response

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

Maximum daily events creation limit exceeded.
```json
{ 
    "status": "failed", 
    "desc": "maximum daily limit exceeded",
    "error_code": 106
}
```

## Notes

* `error_code=107` can be resulted from various reasons, please properly check user input before submitting the data.


#### Participating in an existing open event.

**URL** : `/api/v1/event/participate/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : None

**Data constraints**

[jsonschema](https://json-schema.org/understanding-json-schema/index.html) is used for post data format validation.

```json
{
    "type": "object",
    "properties": {
        "eid": {
            "type": "string"
        },

        "op_type": {
            "type": "integer",
            "enum": "[PARTICIPATE, UNPARTICIPATE]"
        }
    }
}
```

## Notes:
* Upon successful participating in an event, the event remaining quota will be decremented and might subject to
 event status change(`eg. OPEN => QUOTA_FULL`).
* By specifying `op_type`, the operation could be either `participate` or `unparticipate`.
* Note that it is an idempotent operation, such that call participate multiple times will not result in quota inconsistency.


### Success Response

**Code** : `200 OK`

**Request data examples**

An authenticated user is participating an event.

```json
{
	"eid": "b2ad41c2-6a04-4082-be77-496665f6ae77",
	"op_type": 1
}
```

An authenticated user is unparticipating an event.

```json
{
	"eid": "b2ad41c2-6a04-4082-be77-496665f6ae77",
	"op_type": 2
}
```

**Response format examples: successfully participating an event**

```json
{   
    "status": "success", 
    "is_redundant": false, 
    "quota_left": 34, 
    "max_quota": 50
}
```

### Error Response

**Code** : `400 BAD REQUEST`

**Request data examples**

Attempts to participate an non-exist event.

```json
{     "status": "failed", 
      "desc": "event does not exist", 
      "error_code": 105
}
```

Specified operation type is invalid.

```json
{
    "status": "failed",
    "desc": "unknown op type",
    "error_code": 111
}
```


## Notes

* In response body, upon success, `is_redundant=true` indicates the operation is 
redundant(eg. participating an event that you have already participated).




