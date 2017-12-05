from django.http import Http404
from random import randint
import datetime, time

from ..utils import hash_sha256
from ..infrastructures import ApiCustomException
from ..constant import ErrorDefine
from ..models import AuthUser

class AuthUserAdapter:
    def __init__(self):
        pass

    def create_or_update(self, user, token):
        try:
            auth_user = AuthUser.objects.get(user_id=user)

            auth_user.token = token
            auth_user.save()

            return auth_user
        except AuthUser.DoesNotExist:
            auth_user = AuthUser(user_id=user, token=token)

            auth_user.save()

            return auth_user

    def delete_by_user(self, user):
        try:
            auth_user = AuthUser.objects.get(user_id=user)

            auth_user.delete()

            return 'You has logout complele'
        except AuthUser.DoesNotExist:
            raise ApiCustomException(ErrorDefine.USER_NOT_FOUND)

    def get_by_token(self, token):
        try:
            auth_user = AuthUser.objects.get(token=token)

            return auth_user
        except AuthUser.DoesNotExist:
            raise ApiCustomException(ErrorDefine.INVALID_TOKEN)


    def get_by_token(self, token):
        try:
            auth_user = AuthUser.objects.get(token=token)

            return auth_user
        except AuthUser.DoesNotExist:
            raise Http404

    def generate_token(self):
        ts = time.gmtime()

        base_token = '{}{}{}'.format('PROJECT-', str(ts), str(randint(1000, 9999)))
        token = hash_sha256(base_token)

        return token