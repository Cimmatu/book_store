import django_filters

from .models import *


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(max_length=40, min_length=1)

    class Meta:
        model = Product
        fields = ['name']