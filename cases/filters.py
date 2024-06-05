import django_filters
from . import models

class NewFilters(django_filters.FilterSet):
    class Meta:
        model = models.New
        fields = ['title', 'user', 'category', 'subject']

class CaseFilters(django_filters.FilterSet):
    class Meta:
        model = models.SolvedCase
        fields = ['title', 'user', 'category', 'subject']

class CategoryFilters(django_filters.FilterSet):
    class Meta:
        model = models.Category
        fields = ['name']