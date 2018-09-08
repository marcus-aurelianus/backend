def get_error_response_dict(desc, status=None, error_code=None):
    response_dict = {
        "desc": desc
    }

    if status:
        response_dict = {
            **response_dict,
            "status": status,
        }

    if error_code:
        response_dict = {
            **response_dict,
            "error_code": error_code
        }
    return response_dict
