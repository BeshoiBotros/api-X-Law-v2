from rest_framework import serializers
from . import models

class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscribe
        fields = '__all__'

class SubscribeContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubscribeContract
        fields = '__all__'


class SubscribeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubscribeOrder
        fields = '__all__'

class SubscribeContractDetailsSerializer(serializers.Serializer):
    reciept_file = serializers.FileField(required = True)
    nums_of_users = serializers.IntegerField(required = True)

class LimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Limit
        fields = '__all__'
