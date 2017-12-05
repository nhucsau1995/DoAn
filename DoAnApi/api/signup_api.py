from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from random import randint
from django.conf import settings
import nexmo

from ..utils import UserTokenAuthentication
from .api_base import ApiBase
from ..adapter import SignupAdapter, AuthUserAdapter

class Signup(APIView, ApiBase):
    permission_classes = (AllowAny,)
    authentication_classes = (UserTokenAuthentication,)

    def __init__(self):
        self.signup_adapter = SignupAdapter()
        self.auth_user_adapter = AuthUserAdapter()

    def send_sms(self, to, text):
        client = nexmo.Client(key=settings.NEXMO_API_KEY, secret=settings.NEXMO_API_SECRET)
        client.send_message({
            'from': 'Nexmo',
            'to': to,
            'text':text,
        })

    def signup(self, username, password, confirm_password, email, phone, facebook):
        user = self.signup_adapter.signup(username, password, confirm_password, email, phone, facebook)

        token = self.auth_user_adapter.generate_token()

        auth_user = self.auth_user_adapter.create_or_update(user, token)

        pin = randint(10000, 99999)

        self.signup_adapter.add_pin_to_verify(user, pin)
        to = phone.replace(phone[0], '+84', 1)
        text = "%s la ma xac thuc cua ban tren website myproject.com" % (pin)
        self.send_sms(to, text)

        return auth_user.token

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        confirm_password = request.data['confirm_password']
        email = request.data['email']
        phone = request.data['phone']
        facebook = request.data['facebook']

        token = self.signup(username, password, confirm_password, email, phone, facebook)

        result = {
            'token': token
        }

        return self.as_success(result)


class ActiveUser(APIView, ApiBase):
    authentication_classes = (AllowAny,)

    def __init__(self):
        self.signup_adapter = SignupAdapter()
        self.auth_user_adapter = AuthUserAdapter()

    def post(self, request, *args, **kwargs):
        pin = request.data["pin"]
        token = UserTokenAuthentication.get_token(request)
        auth_user = self.auth_user_adapter.get_by_token(token)
        user = self.signup_adapter.active_user(auth_user.user_id, pin)
        return self.as_success(user)