from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from ..serializers import UserProfileSerializer
from ..utils import UserTokenAuthentication
from .api_base import ApiBase

class UserAPI(APIView, ApiBase):
    authentication_classes = (UserTokenAuthentication,)

    def get(self, request, *args, **kwargs):
        user = self.check_anonymous(request)
        serializer = UserProfileSerializer(user)
        return self.as_success(serializer.data)