# #!/usr/bin/python
# # author luke
# from django.db.models import Q
from django_filters import rest_framework as filters
from .models import *
#

class CourseFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    class Meta:
        model = Course
        fields = ['name', 'org','teacher']

class CategoryFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    class Meta:
        model = CourseCategory
        fields = ['category_type', ]

class CoursewareFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    class Meta:
        model = Courseware
        fields = ['lesson', ]
