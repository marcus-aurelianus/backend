# User Related API documentation

## Register
Register new account with email, username and password.

**URL** : `/api/v1/user/register/`

**Method** : `POST`

**Auth required** : No

**Permissions required** : None

### Success Response

**Code** : `200 OK`

**Request data examples**

For a User with username `test1234`, password `12345678`, and email `test1234@abc.com`

```json
{
    "username": "test1234",
    "password": "12345678",
    "email": "test1234@abc.com"
}
```

**Response format examples**

```json
{
    "status": "success", 
    "user_id": 65213
}
```

## Notes

* `username` and `password` have to be a minimum length of 8 and maximum of 16 characters.


## Login
Login with username and password.

**URL** : `/api/v1/user/login/`

**Method** : `POST`

**Auth required** : No

**Permissions required** : None

### Success Response

**Code** : `200 OK`

**Request data examples**

For a User with username `test1234`, password `12345678`.

```json
{
    "username": "test1234",
    "password": "12345678"
}
```

**Successful Response format examples**

```json
{
    "status": "success",
    "username": "test1234",
    "email": "test1234@abc.com",
    "uid": "65213"
}
```
### Error Response

**Code** : `200 OK`

**Failed Response format examples**

```json
{   
    "status": "failed", 
    "desc": "user name or password incorrect",
    "error_code": 102
}    
```

## Logout
Login with username and password.

**URL** : `/api/v1/user/logout/`

**Method** : `POST`

**Auth required**: Yes

**Permissions required** : None

### Success Response

**Code** : `200 OK`

**Request data examples**

* No request data required.

**Successful Response format examples**

```json
{    
    "status": "success",
    "uid": 85807
}
```

### Error Response

**Code** : `401 Unauthorized`

**Failed Response format examples**

```json
{    
    "status": "failed", 
    "desc": "login required", 
    "error_code": 101
}
```

## Notes
* A full list of `error code` can be found [here](error_code.md)
* Upon successful login, `sessionid` is set on cookie to indicate login status.


## Fetch user related events.
Fetch all events that user participated in.

**URL** : `/api/v1/user/events_participated/`

**Method** : `GET`

**Auth required** : Yes

**Permissions required** : None

### Success Response

**Code** : `200 OK`

**Request data examples**

* No request data required.


**Response format examples**

```json
{
    "status": "success", 
    "events": [ 
        { 
            "pk": "b2ad41c2-6a04-4082-be77-496665f6ae77", 
            "fields": {   
                  "event_title": "BBQ buffet Dinner @ one north", 
                  "event_desc": "This is a free dinner", 
                  "event_creator": 1, 
                  "event_type": 1, 
                  "create_time": "2018-09-08T06:22:41.486Z", 
                  "update_time": "2018-09-08T06:29:14.502Z", 
                  "state": 1, 
                  "max_quota": 50, 
                  "num_participants": 1, 
                  "extra_info_dict": "", 
                  "event_start_date": 
                  "2019-02-07T03:52:00Z", 
                  "event_end_date": 
                  "2019-02-07T03:52:00Z", 
                  "is_open_ended": 1}
        },
         
        { 
            "pk": "b2ad41c2-6a04-4082-be77-496665f6ae77", 
            "fields": {   
                  "event_title": "BBQ buffet Dinner @ one north", 
                  "event_desc": "This is a free dinner", 
                  "event_creator": 1, 
                  "event_type": 1, 
                  "create_time": "2018-09-08T06:22:41.486Z", 
                  "update_time": "2018-09-08T06:29:14.502Z", 
                  "state": 1, 
                  "max_quota": 50, 
                  "num_participants": 1, 
                  "extra_info_dict": "", 
                  "event_start_date": 
                  "2019-02-07T03:52:00Z", 
                  "event_end_date": 
                  "2019-02-07T03:52:00Z", 
                  "is_open_ended": 1
            }
        }
    ]
}
```

## Fetch user created events.
Fetch all events that user created.

**URL** : `/api/v1/user/events_created/`

**Method** : `GET`

**Auth required** : Yes

**Permissions required** : None

### Success Response

**Code** : `200 OK`

**Request data examples**

* No request data required.


**Response format examples**

```json
{
    "status": "success", 
    "events": [ 
        { 
            "pk": "b2ad41c2-6a04-4082-be77-496665f6ae77", 
            "fields": {   
                  "event_title": "BBQ buffet Dinner @ one north", 
                  "event_desc": "This is a free dinner", 
                  "event_creator": 1, 
                  "event_type": 1, 
                  "create_time": "2018-09-08T06:22:41.486Z", 
                  "update_time": "2018-09-08T06:29:14.502Z", 
                  "state": 1, 
                  "max_quota": 50, 
                  "num_participants": 1, 
                  "extra_info_dict": "", 
                  "event_start_date": 
                  "2019-02-07T03:52:00Z", 
                  "event_end_date": 
                  "2019-02-07T03:52:00Z", 
                  "is_open_ended": 1}
        },
         
        { 
            "pk": "b2ad41c2-6a04-4082-be77-496665f6ae77", 
            "fields": {   
                  "event_title": "BBQ buffet Dinner @ one north", 
                  "event_desc": "This is a free dinner", 
                  "event_creator": 1, 
                  "event_type": 1, 
                  "create_time": "2018-09-08T06:22:41.486Z", 
                  "update_time": "2018-09-08T06:29:14.502Z", 
                  "state": 1, 
                  "max_quota": 50, 
                  "num_participants": 1, 
                  "extra_info_dict": "", 
                  "event_start_date": 
                  "2019-02-07T03:52:00Z", 
                  "event_end_date": 
                  "2019-02-07T03:52:00Z", 
                  "is_open_ended": 1
            }
        }
    ]
}
```

