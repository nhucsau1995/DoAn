from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from ..utils import UserTokenAuthentication
from ..serializers import BaseCommentSerializer, ListCommentSerializer
from .api_base import ApiBase
from ..models import Comment, Post
from ..infrastructures import ApiCustomException
from ..constant import ErrorDefine

class ListComment(APIView, ApiBase):
    permission_classes = (AllowAny,)


    def get(self, request, *args, **kwargs):
        comments = Comment.objects.all()
        for comment in comments:
            comment.username = comment.user_id.username

        serializer = ListCommentSerializer(comments, many=True)
        return self.as_success(serializer.data)


class SaveComment(APIView, ApiBase):
    authentication_classes = (UserTokenAuthentication,)
    permission_classes = (AllowAny,)

    def save_comment(self, content, user, post_id):
        try:
            post = Post.objects.get(id=post_id)

            comment = Comment(user_id=user, content=content, post_id=post)
            comment.save()

            return comment
        except Post.DoesNotExist:
            raise ApiCustomException(ErrorDefine.POST_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        user = self.check_anonymous(request)
        content = request.data['content']
        post_id = request.data['post']
        comment = self.save_comment(user, content, post_id)
        serializer = BaseCommentSerializer(comment, many=False)
        return self.as_success(serializer.data)