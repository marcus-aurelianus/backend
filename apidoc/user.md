# User Related API documentation

##Register
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


##Login
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

##Logout
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


