from rest_framework import serializers
from . import models
from django.apps import apps
from XLaw import constants
from XLaw import shortcuts
from users import serializers as user_serializer
from subscribes import serializers as subscribe_serializer

class OrganizationSerializer(serializers.ModelSerializer):
    
    user_view = serializers.SerializerMethodField(read_only=True)
    subscribe_contract_view = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Organization
        fields = ['id', 'name', 'user', 'subscribe_contract', 'address', 'phone_number', 'url', 'email', 'user_view', 'subscribe_contract_view']
        extra_kwargs = {
            'user' : {'write_only' : True},
            'subscribe_contract' : {'write_only' : True}
        }

    def get_user_view(self, obj):
        serializer = user_serializer.CustomUserSerializer(instance=obj.user)
        return serializer.data

    def get_subscribe_contract_view(self, obj):
        serializer = subscribe_serializer.SubscribeContractSerializer(instance=obj.subscribe_contract)
        return serializer.data
    
class OwnershipSerializer(serializers.ModelSerializer):

    # Read Only Fields
    organization_view = serializers.SerializerMethodField(read_only=True)
    object_view = serializers.SerializerMethodField(read_only=True)
    content_type_view  = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.ObjectOwnership
        fields = ['organization', 'object_id', 'content_type', 'organization_view', 'object_view', 'content_type_view']
        extra_kwargs = {
            'organization': {'write_only': True},
            'object_id': {'write_only': True},
            'content_type': {'write_only': True},
        }
        
    # Getter Methods
    def get_organization_view(self, obj):
        org = models.Organization.objects.get(pk=obj.organization.pk)
        serializer = OrganizationSerializer(instance=org)
        return serializer.data

    def get_object_view(self, obj):
        model_class = apps.get_model(app_label=obj.content_type.app_label, model_name=obj.content_type.model)
        model_serializer = constants.MODEL_TO_SERIALIZER.get(model_class)
        instance = model_class.objects.get(pk=obj.object_id)
        serializer = model_serializer(instance=instance)
        return serializer.data

    def get_content_type_view(self, obj):
        return {'model' : obj.content_type.model}
        

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentMethod
        fields = '__all__'