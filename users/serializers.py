# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from . import models
from XLaw.shortcuts import emailAlreadyExist, token_is_exist


class CustomUserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    as_lawyer = serializers.BooleanField(required=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        email = data.get('email')  # Using get to avoid KeyError
        
        if emailAlreadyExist(email):
            raise serializers.ValidationError({'error' : 'email already exist'})
        
        return data

    
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_client = serializers.BooleanField(read_only=True)
    is_lawyer = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.CustomUser  
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_client', 'is_lawyer']


class ClientSerializer(CustomUserSerializer):
    class Meta:
        model = models.Client
        fields = CustomUserSerializer.Meta.fields

class LawyerSerializer(CustomUserSerializer):
    class Meta:
        model = models.Lawyer
        fields = CustomUserSerializer.Meta.fields

class VerifyToken(serializers.ModelSerializer):
    token = serializers.CharField(required=True)
    class Meta:
        model = models.VerifyToken
        fields = ['token']
    def validate(self, attrs):
        data = super().validate(attrs)
        token = data.get('token')
        if token_is_exist(token):
            raise serializers.ValidationError({'error':'Can not use expired token!'})
        return data
    
class LawyerProfileSerializer(serializers.ModelSerializer):
    lawyer = LawyerSerializer(read_only=True)
    class Meta:
        model = models.LawyerProfile
        fields = ['id', 'image', 'lawyer']