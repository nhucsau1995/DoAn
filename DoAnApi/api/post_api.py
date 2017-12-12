from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


from ..utils import UserTokenAuthentication
from .api_base import ApiBase
from ..models import Post, UserLikePost, Image
from ..serializers import PostSerializer, ListPostSerializer, UserHasPostSerializer, EditPostSerializer, \
    CreatePostSerializer
from ..infrastructures import ApiCustomException
from ..constant import ErrorDefine

class PostList(APIView, ApiBase):


    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        for post in posts:
            images = Image.objects.get(post_id=post)
            post.image = images.image

        serializer = ListPostSerializer(posts, many=True)
        return self.as_success(serializer.data)


class PostListWithType(APIView, ApiBase):

    def get_post_with_tpye(self, type):
        try:
            posts = Post.objects.filter(type=type)
            return posts
        except Post.DoesNotExist:
            raise ApiCustomException(ErrorDefine.POST_NOT_FOUND)


    def get(self, request, type, *args, **kwargs):
        types = type.replace('-',' ')
        posts = self.get_post_with_tpye(types)
        for post in posts:
            images = Image.objects.get(post_id=post)
            post.image = images.image
        serializer = ListPostSerializer(posts, many=True)
        return self.as_success(serializer.data)


class PostDetail(APIView, ApiBase):

    def get_object(self, slug):
        try:

            post = Post.objects.get(slug=slug)

            post.is_liked = False
            post.username = post.user.username
            post.email = post.user.email
            post.phone = post.user.phone
            post.facebook = post.user.facebook

            images = Image.objects.filter(post_id = post)
            post.images = images

            return post

        except Post.DoesNotExist:
            raise ApiCustomException(ErrorDefine.POST_NOT_FOUND)

    def get(self, request, slug, *args, **kwargs):
        post = self.get_object(slug)
        serializer = PostSerializer(post)
        return self.as_success(serializer.data)


class PostdetailWithAuth(APIView, ApiBase):
    permission_classes = (AllowAny,)
    authentication_classes = (UserTokenAuthentication,)

    def get_post(self, user, slug):
        try:

            post = Post.objects.get(slug=slug)
            try:
                post.userlikepost_set.get(user_id=user)

                post.is_liked = True
            except:
                post.is_liked = False

            post.username = post.user.username
            post.email = post.user.email
            post.phone = post.user.phone
            post.facebook = post.user.facebook

            images = Image.objects.filter(post_id=post)
            post.images = images

            return post

        except Post.DoesNotExist:
            raise ApiCustomException(ErrorDefine.POST_NOT_FOUND)

    def get(self, request, slug):
        user = self.check_anonymous(request)
        post = self.get_post(user, slug)
        serializer = PostSerializer(post)
        return self.as_success(serializer.data)


class UserHasPostApi(APIView, ApiBase):
    permission_classes = (AllowAny,)
    authentication_classes = (UserTokenAuthentication,)

    def get_user_has_post(self, user):
        try:
            posts = Post.objects.filter(user=user)

            return posts
        except Post.DoesNotExist:
            raise ApiCustomException(ErrorDefine.POST_NOT_FOUND)


    def get(self, request, *args, **kwargs):
        user = self.check_anonymous(request)
        posts = self.get_user_has_post(user)
        serializer = UserHasPostSerializer(posts, many=True)
        return self.as_success(serializer.data)


class UserPostDetail(APIView, ApiBase):
    permission_classes = (AllowAny,)
    authentication_classes = (UserTokenAuthentication,)

    def get_user_post_detail(self, user, slug):
        try:
            post = Post.objects.get(slug=slug, user=user)
            post.phone = post.user.phone

            images = Image.objects.filter(post_id=post)
            post.images = images
            return post

        except Post.DoesNotExist:
            raise ApiCustomException(ErrorDefine.POST_NOT_FOUND)

    def get_post(self, user, post):
        try:
            try:
                post.userlikepost_set.get(user_id=user)

                post.is_liked = True
            except:
                post.is_liked = False

            post.username = post.user.username
            post.email = post.user.email
            post.phone = post.user.phone
            post.facebook = post.user.facebook

            images = Image.objects.filter(post_id=post)
            post.images = images

            return post

        except Post.DoesNotExist:
            raise ApiCustomException(ErrorDefine.POST_NOT_FOUND)

    def update_post(self,slug,user,phone,type,title,video,customer,price,area, province,district, address, description):
        post = Post.objects.get(slug=slug, user=user)
        post.phone = phone
        post.type = type
        post.title = title
        post.customer = customer
        post.price = price
        post.area = area
        post.province = province
        post.district = district
        post.address = address
        post.description = description
        if post.video != video:
            post.video.delete()
            post.video = video
        post.save()
        return post

    def delete_image(self, id):
        image = Image.objects.get(id=id)
        image.image.delete()
        image.delete()

    def add_image(self, image, post):
        images = Image(post_id=post, image=image)
        images.save()
        return images


    def get(self, request, slug, *args, **kwargs):
        user = self.check_anonymous(request)
        post = self.get_user_post_detail(user, slug)
        serializer = PostSerializer(post)
        return self.as_success(serializer.data)

    def put(self, request, slug,*args, **kwargs):
        user = self.check_anonymous(request)
        phone = request.data['phone']
        type = request.data['type']
        title = request.data['title']
        video = request.data['video']
        customer = request.data['customer']
        price = request.data['price']
        area = request.data['area']
        province = request.data['province']
        district = request.data['district']
        address = request.data['address']
        description = request.data['description']
        post = self.update_post(slug,user,phone,type,title,video,customer,price,area, province,district, address, description)
        for id in request.data['delete']:
            self.delete_image(id)
        for image in request.data.getlist('images'):
            self.create_image(image, post)
        post = self.get_post(user, post)
        serializer = PostSerializer(post)
        return self.as_success(serializer.data)

    def delete(self, request, slug ,format=None,*args, **kwargs):
        user = self.check_anonymous(request)
        post = self.get_user_post_detail(user, slug)
        images = Image.objects.filter(post_id=post)
        for image in images:
            image.image.delete()
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCreatePost(APIView, ApiBase):
    permission_classes = (AllowAny,)
    authentication_classes = (UserTokenAuthentication,)

    def get_post(self, user, post):
        try:
            try:
                post.userlikepost_set.get(user_id=user)

                post.is_liked = True
            except:
                post.is_liked = False

            post.username = post.user.username
            post.email = post.user.email
            post.phone = post.user.phone
            post.facebook = post.user.facebook

            images = Image.objects.filter(post_id=post)
            post.images = images

            return post

        except Post.DoesNotExist:
            raise ApiCustomException(ErrorDefine.POST_NOT_FOUND)

    def create_post(self,user,phone,type,title,video,customer,price,area, province,district, address, description):
        post = Post(user=user,phone=phone, type=type, title=title,video=video, customer=customer,
               price=price, area = area, province=province,district=district, address=address, description=description)
        post.save()
        return post


    def create_image(self,image, post):
        images = Image(post_id = post, image=image)
        images.save()
        return images


    def post(self, request, *args, **kwargs):
        user = self.check_anonymous(request)
        phone = user.phone
        type = request.data['type']
        title = request.data['title']
        video = request.data['video']
        customer = request.data['customer']
        price = request.data['price']
        area = request.data['area']
        province = request.data['province']
        district = request.data['district']
        address = request.data['address']
        description = request.data['description']
        post = self.create_post(user,phone,type,title,video,customer,price,area, province,district, address, description)
        for image in request.data.getlist('images'):
            self.create_image(image, post)
        post = self.get_post(user, post)
        serializer = PostSerializer(post)
        return self.as_success(serializer.data)



class LikePost(APIView, ApiBase):
    permission_classes = (AllowAny,)
    authentication_classes = (UserTokenAuthentication,)

    def like(self, user, post_id):
        try:
            post = Post.objects.get(id=post_id)

            user_like_post = UserLikePost.objects.filter(user_id=user,post_id=post)

            if user_like_post.exists():
                user_like_post.first().delete()
                return 'You unlike success'

            user_like_post = UserLikePost(user_id=user, post_id=post)
            user_like_post.save()

            return 'You like comment success'

        except Post.DoesNotExist:
            raise ApiCustomException(ErrorDefine.POST_NOT_FOUND)


    def post(self, request,*args, **kwargs):
        user = self.check_anonymous(request)

        post_id = request.data['post_id']

        result = self.like(user, post_id)

        return self.as_success(result)
