from rest_framework import generics
from django_filters import rest_framework as filters

from ..models import Post, Image
from ..serializers import ListPostSerializer
import django_filters
from ..infrastructures import ApiCustomException
from ..constant import ErrorDefine
from .api_base import ApiBase


class PostFilter(django_filters.FilterSet):

    class Meta:
        model = Post
        fields = {
            'type': ['exact'],
            'province': ['exact'],
            'district': ['exact'],
            'price':  ['gte', 'lte'],
        }



class SearchPost(generics.ListAPIView, ApiBase):
    queryset = Post.objects.all()
    serializer_class = ListPostSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    def get_post(self, type, province, district, price__lte, price__gte):
        try:
            if price__lte != "" and price__gte != "" and type != "" and province != "" and district != "":
                queryset = Post.objects.filter(type=type, province=province, district=district,
                                               price__lte=price__lte, price__gte=price__gte)

            elif price__lte == "" and price__gte == "" and type == "" and province == "" and district == "":
                queryset = Post.objects.all()

            elif price__lte == "" and price__gte == "" and province == "" and district == "":
                queryset = Post.objects.filter(type=type)

            elif price__lte == "" and price__gte == "" and type == "" and district == "":
                queryset = Post.objects.filter(province=province)

            elif price__gte == "" and type == "" and province == "" and district == "":
                queryset = Post.objects.filter(price__lte=price__lte)

            elif price__lte == "" and type == "" and province == "" and district == "":
                queryset = Post.objects.filter(price__gte=price__gte)

            elif type == "" and province == "" and district == "":
                queryset = Post.objects.filter(price__lte=price__lte,price__gte=price__gte)

            elif price__lte == "" and province == "" and district == "":
                queryset = Post.objects.filter(type=type, price__gte=price__gte)

            elif price__lte == "" and price__gte == "" and district == "":
                queryset = Post.objects.filter(type=type, province=province)

            elif price__lte == "" and district == "" and type =="":
                queryset = Post.objects.filter(province=province, price__gte=price__gte)

            elif district == "" and province =="":
                queryset = Post.objects.filter(type=type, price__gte=price__gte,price__lte=price__lte)

            elif price__lte == "" and district =="":
                queryset = Post.objects.filter(type=type, price__gte=price__gte,province=province)

            elif price__lte == "" and price__gte =="":
                queryset = Post.objects.filter(type=type, district=district,province=province)

            elif price__lte == "" and type=="":
                queryset = Post.objects.filter(price__gte=price__gte, district=district,province=province)

            elif type == "" and district =="":
                queryset = Post.objects.filter(price__lte=price__lte, price__gte=price__gte,province=province)

            elif type =="":
                queryset = Post.objects.filter(price__lte=price__lte, price__gte=price__gte, province=province, district=district)

            elif district=="":
                queryset = Post.objects.filter(price__lte=price__lte, price__gte=price__gte, province=province, type=type)

            elif price__lte=="":
                queryset = Post.objects.filter(district=district, price__gte=price__gte, province=province, type=type)


            return queryset
        except Post.DoesNotExist:
            raise ApiCustomException(ErrorDefine.POST_NOT_FOUND)


    def get_queryset(self):
        type = self.request.query_params.get('type', None)
        province = self.request.query_params.get('province', None)
        district = self.request.query_params.get('district', None)
        price__gte = self.request.query_params.get('price__gte', None)
        price__lte = self.request.query_params.get('price__lte', None)


        queryset = self.get_post(type, province, district, price__lte, price__gte)


        for post in queryset:
            image = Image.objects.get(post_id=post)
            post.image = image.image
        return queryset
