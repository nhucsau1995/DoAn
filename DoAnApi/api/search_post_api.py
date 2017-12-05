from rest_framework import generics
from django_filters import rest_framework as filters

from ..models import Post
from ..serializers import ListPostSerializer
import django_filters


class PostFilter(django_filters.FilterSet):

    class Meta:
        model = Post
        fields = {
            'type': ['exact'],
            'province': ['exact'],
            'district': ['exact'],
            'price':  ['gte', 'lte'],
        }



class SearchPost(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = ListPostSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PostFilter

