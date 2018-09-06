from apis.models import User


def check_user_info(user_data):
    check_email = User.objects.filter(email=user_data['email'])
    check_user = User.objects.filter(email=user_data['username'])
    if check_email or check_user:
        return True
    else:
        return False

