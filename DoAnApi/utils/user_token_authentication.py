from rest_framework.authentication import TokenAuthentication, get_authorization_header
from datetime import datetime, timedelta
import pytz
from rest_framework import status

from ..infrastructures import ApiCustomException
from ..constant import ErrorDefine, Constant
from ..models import AuthUser


class UserTokenAuthentication(TokenAuthentication):
    constant = Constant()

    def authenticate_credentials(self, key):
        try:
            auth_user = AuthUser.objects.get(token=key)

        except AuthUser.DoesNotExist:
            raise ApiCustomException(ErrorDefine.INVALID_TOKEN, status.HTTP_401_UNAUTHORIZED)

        if auth_user.user_id.status == 0:
            raise ApiCustomException(ErrorDefine.USER_INACTIVE, status.HTTP_401_UNAUTHORIZED)

        # This is required for the time comparison
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if auth_user.updated_at < utc_now - timedelta(seconds=self.constant.get_token_expired_time()):
            raise ApiCustomException(ErrorDefine.TOKEN_EXPIRED, status.HTTP_401_UNAUTHORIZED)

        return auth_user.user_id, auth_user

    @classmethod
    def get_token(cls, request):
        try:
            authorization = get_authorization_header(request).split()

            token = authorization[1]

            return token
        except Exception:
            raise ApiCustomException(ErrorDefine.MISSING_TOKEN)