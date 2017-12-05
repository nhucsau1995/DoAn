from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from ..models import User, AuthUser
from ..infrastructures import ApiCustomException, ApiErrorMessage
from ..constant import ErrorDefine


class SignupAdapter:
    def __init__(self):
        pass

    def check_unique(self, username, phone, email):
        users = User.objects.filter(username=username)

        if users.exists():
            raise ApiCustomException(ErrorDefine.USER_USERNAME_EXIST)

        users = User.objects.filter(phone=phone)

        if users.exists():
            raise ApiCustomException(ErrorDefine.USER_PHONE_EXIST)

        users = User.objects.filter(email=email)

        if users.exists():
            raise ApiCustomException(ErrorDefine.USER_EMAIL_EXIST)

        try:
            validate_email(email)

        except ValidationError as e:
            api_error_message = ApiErrorMessage(e.message, 9999)
            raise ApiCustomException(api_error_message)




    def signup(self, username, password, confirm_password, email, phone, facebook):
        self.check_unique(username, phone, email)

        if password != confirm_password:
            raise ApiCustomException(ErrorDefine.PASSWORD_DO_NOT_MATCH_CONFIRM_PASSWORD)

        status = 0
        # role 2 is normal user, 1 is admin user
        role = 2

        user = User(username=username, password=password, email=email, status=status, role=role, phone = phone, facebook=facebook)

        user.save()

        return user

    def add_pin_to_verify(self, user, pin):
        user.pin = pin
        user.save()


    def active_user(self, user, pin):
        if user.pin == pin:

            if user.status == 1:
                user.pin = None
                user.save()
                raise ApiCustomException(ErrorDefine.USER_ALREADY_ACTIVE)

            user.pin = None
            user.status = 1

            user.save()

            return 'User active successful'

        raise ApiCustomException(ErrorDefine.PIN_INCORRECT)
