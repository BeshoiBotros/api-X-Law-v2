import django_filters
from . import models

class SubscribeFilter(django_filters.FilterSet):
    class Meta:
        model = models.Subscribe
        fields = '__all__'


class LimitFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    class Meta:
        model = models.Limit
        fields = '__all__'