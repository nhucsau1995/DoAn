from rest_framework import serializers
from ..models import User

class SignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')


class AcitveUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pin']