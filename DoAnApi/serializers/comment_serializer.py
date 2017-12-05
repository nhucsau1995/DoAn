from rest_framework import serializers

from ..models import Comment

class BaseCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class ListCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=254)

    class Meta:
        model = Comment
        fields = '__all__'