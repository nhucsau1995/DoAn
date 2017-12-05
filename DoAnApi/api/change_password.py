from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from random import randint
from django.conf import settings
import nexmo

from ..utils import UserTokenAuthentication
from .api_base import ApiBase
from ..models import User
from ..infrastructures import ApiCustomException
from ..constant import ErrorDefine


class ChangePassword(APIView, ApiBase):
    permission_classes = (AllowAny,)
    authentication_classes = (UserTokenAuthentication,)

    def change_password(self, user, old_password, new_password, comfirm_password):
        try:
            if old_password == user.password:
                if new_password == comfirm_password:
                    user.password = new_password
                    user.save()
                    return "You changed password successfully"
                else:
                    raise ApiCustomException(ErrorDefine.NEW_PASSWORD_DO_NOT_MATCH_CONFIRM_PASSWORD)
            raise ApiCustomException(ErrorDefine.YOUR_PASSWORD_WRONG)
        except User.DoesNotExist:
            raise ApiCustomException(ErrorDefine.USER_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        user = self.check_anonymous(request)
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        comfim_password = request.data['comfirm_password']
        user = self.change_password(user, old_password, new_password, comfim_password)
        return self.as_success(user)



class ForgetPassword(APIView, ApiBase):

    def send_sms(self, to, text):
        client = nexmo.Client(key=settings.NEXMO_API_KEY, secret=settings.NEXMO_API_SECRET)
        client.send_message({
            'from': 'Nexmo',
            'to': to,
            'text':text,
        })

    def get_user(self, phone):
        try:
            user = User.objects.get(phone=phone)
            user.pin = randint(10000, 99999)
            user.save()
            to = phone.replace(phone[0], '+84', 1)
            text = "%s la ma xac thuc cua ban tren website myproject.com" % (user.pin)
            self.send_sms(to, text)
            return "Ma xac nhan da duoc gui den %s. Vui long nhap ma vao ben duoi de tiep tuc." % (phone)

        except User.DoesNotExist:
            raise ApiCustomException(ErrorDefine.USER_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        phone = request.data['phone']
        result = self.get_user(phone)
        return self.as_success(result)


class InputpPin(APIView, ApiBase):

    def input_pin(self, phone, pin):
        try:
            user = User.objects.get(phone=phone)
            if user.pin == pin:
                user.pin = None
                user.save()
                return "Correct"
            raise ApiCustomException(ErrorDefine.PIN_INCORRECT)

        except User.DoesNotExist:
            raise ApiCustomException(ErrorDefine.USER_NOT_FOUND)

    def post(self,request, *args, **kwargs):
        phone = request.data['phone']
        pin = request.data['pin']
        result = self.input_pin(phone, pin)
        return self.as_success(result)


class ResetPassword(APIView, ApiBase):

    def reset_password(self, phone, new_password, comfirm_password):
        try:
            user = User.objects.get(phone=phone)
            if new_password == comfirm_password:
                user.password = new_password
                user.save()
                return "Ban da doi mat khau thanh cong"
            raise ApiCustomException(ErrorDefine.NEW_PASSWORD_DO_NOT_MATCH_CONFIRM_PASSWORD)

        except User.DoesNotExist:
            raise ApiCustomException(ErrorDefine.USER_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        phone = request.data['phone']
        new_password = request.data['new_password']
        comfirm_password = request.data['comfirm_password']
        result = self.reset_password(phone, new_password, comfirm_password)
        return self.as_success(result)
