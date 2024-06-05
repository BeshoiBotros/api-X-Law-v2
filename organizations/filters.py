import django_filters
from . import models

class OrganizationFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Organization
        fields = '__all__'

class ObjectOwnershipFilter(django_filters.FilterSet):

    lawyer_username = django_filters.CharFilter(field_name='lawyer__username', lookup_expr='icontains')
    organization_name = django_filters.CharFilter(field_name='organization__name', lookup_expr='icontains')
    
    class Meta:
        model = models.ObjectOwnership
        fields = '__all__'