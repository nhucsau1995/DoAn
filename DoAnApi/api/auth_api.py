from rest_framework.views import APIView
from django.db.models import Q

from rest_framework.permissions import AllowAny

from ..models import User
from ..utils import UserTokenAuthentication
from ..infrastructures import ApiCustomException
from ..constant import ErrorDefine
from .api_base import ApiBase
from ..adapter import AuthUserAdapter

class Login(APIView, ApiBase):
    permission_classes = (AllowAny,)
    authentication_classes = (UserTokenAuthentication,)

    def __init__(self):
        self.auth_user_adapter = AuthUserAdapter()

    def login(self, username, password):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))

            if user.password != password:
                raise ApiCustomException(ErrorDefine.LOGIN_FAIL)

            if user.status == 0:
                raise ApiCustomException(ErrorDefine.USER_INACTIVE)

            return user
        except User.DoesNotExist:
            raise ApiCustomException(ErrorDefine.LOGIN_FAIL)


    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        user = self.login(username=username, password=password)

        token = self.auth_user_adapter.generate_token()

        auth_user = self.auth_user_adapter.create_or_update(user=user, token=token)

        result = {
            'token': auth_user.token
        }

        return self.as_success(result)



class Logout(APIView, ApiBase):
    permission_classes = (AllowAny,)
    authentication_classes = (UserTokenAuthentication,)

    def __init__(self):
        self.auth_user_adapter = AuthUserAdapter()

    def get(self, request):
        user = self.check_anonymous(request)
        result = self.auth_user_adapter.delete_by_user(user)

        return self.as_success(result)


