from rest_framework import serializers

from ..models import Post, UserLikePost
from .image_serializer import ImageSerializer

class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=30)
    facebook = serializers.URLField()
    is_liked = serializers.BooleanField()
    images = ImageSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'

class EditPostSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=30)

    class Meta:
        model = Post
        exclude = ['slug', 'like_number','user']


class CreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        exclude = ['slug','like_number']


class ListPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)


    class Meta:
        model = Post
        fields = ('slug','user','title','price', 'area', 'district', 'province', 'description', 'image','created_at', 'updated_at')


class UserHasPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id','slug','title', 'created_at', 'updated_at']


class LikePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLikePost
        fields = ['user_id','post_id']



