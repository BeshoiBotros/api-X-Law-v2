from rest_framework.views import APIView
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from XLaw import shortcuts
from rest_framework.response import Response
from . import filters
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.apps import apps
from XLaw import constants
from django.shortcuts import get_object_or_404

class OrganizationView(APIView):
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(methods=['get'])
    def get(self, request, pk=None):

        if pk:
            instance = get_object_or_404( models.Organization, id=pk)
            serializer = serializers.OrganizationSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        queryset = models.Organization.objects.filter(subscribe_contract__is_active=True)
        
        filter = filters.OrganizationFilter(request.GET, queryset=queryset)
        
        if filter.is_valid():
            queryset = filter.qs
        
        serializer = serializers.OrganizationSerializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializers.OrganizationSerializer)
    def post(self, request):
        can_add = shortcuts.check_permission('add_organization',request)
        if can_add:
            serializer = serializers.OrganizationSerializer(request.data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message' : 'You can not perform this action'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.OrganizationSerializer)
    def patch(self, request, pk):
        can_add = shortcuts.check_permission('change_organization',request)
        instance = get_object_or_404( models.Organization, id=pk)
        if can_add:
            serializer = serializers.OrganizationSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.user.pk == instance.user.pk:
            serializer = serializers.OrganizationSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.validated_data.pop('subscribe_contract', None)
                serializer.validated_data.pop('user', None)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message' : 'You can not perform this action'})

    @swagger_auto_schema(methods=['delete'])
    def delete(self, request, pk):
        can_add = shortcuts.check_permission('delete_organization',request)
        instance = get_object_or_404( models.Organization, id=pk)
        if can_add:
            instance.delete()
            return Response({'message':'Organization has been deleted successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message' : 'You can not perform this action'}, status=status.HTTP_400_BAD_REQUEST)


class ObjectOwnershipView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(method='get')
    def get(self, request, pk=None, organization_pk=None):
        
        if organization_pk:
            organization = ContentType(models.Organization, id=organization_pk)
            queryset = models.ObjectOwnership.objects.filter(organization=organization)
            serializer = serializers.OwnershipSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if pk:
            instance = shortcuts.object_is_exist(pk, models.ObjectOwnership, 'organization not found')
            serializer = serializers.OwnershipSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = models.ObjectOwnership.objects.all()
        
        filter = filters.ObjectOwnershipFilter(request.GET, queryset=queryset)
        
        if filter.is_valid():
            queryset = filter.qs
        
        serializer = serializers.OwnershipSerializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT))
    def post(self, request, content_type_pk):
        
        can_add_object = shortcuts.can_add_organization_objects(content_type_pk, request)
        content_type_instance = get_object_or_404(ContentType, id=content_type_pk )
        
        org = models.Organization.objects.get(user=request.user.pk)

        if not can_add_object:
            return Response({'message' : f'you reach your limit to add {content_type_instance.model}'}, status=status.HTTP_403_FORBIDDEN)
        
        model = apps.get_model(app_label=content_type_instance.app_label, model_name=content_type_instance.model)

        serializer_class = constants.MODEL_TO_SERIALIZER.get(model)
        object_serializer = serializer_class(data=request.data)

        if object_serializer.is_valid():
            
            obj_instance = object_serializer.save()
            
            data = {
                'organization' : org.pk,
                'object_id' : obj_instance.pk,
                'content_type' : content_type_instance.pk,
            }
            
            ownership_serializer = serializers.OwnershipSerializer(data=data)
            
            if ownership_serializer.is_valid():
                ownership_serializer.save()
                return Response(ownership_serializer.data, status=status.HTTP_200_OK)
            else:
                obj_instance.delete()
                return Response(ownership_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(object_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT))
    def patch(self, request, pk):

        ownership_object = get_object_or_404(models.ObjectOwnership, id=pk)

        try:
            org = models.Organization.objects.get(user=request.user.pk)
        except models.Organization.DoesNotExist:
            return Response({'message' : 'Organization Not foundes'}, status=status.HTTP_404_NOT_FOUND)

        if ownership_object.organization.pk is not org.pk:
            return Response({'message' : 'you can only update your ownership'}, status=status.HTTP_403_FORBIDDEN)

        model_class = ownership_object.content_object.__class__
        model_serializer = constants.MODEL_TO_SERIALIZER.get(model_class)

        if not model_serializer:
            return Response({'message' : 'Not Found 404'}, status=status.HTTP_404_NOT_FOUND)

        object_serializer = model_serializer(instance=ownership_object.content_object, data=request.data, partial=True)

        if object_serializer.is_valid():
            instance = object_serializer.save()
            ownership_serializer = serializers.OwnershipSerializer(instance=ownership_object)
            return Response(ownership_serializer.data)
        
        return Response(object_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(method='delete')
    def delete(self, request, pk):

        ownership_object = get_object_or_404(models.ObjectOwnership, id=pk)

        try:
            org = models.Organization.objects.get(user=request.user.pk)
        except models.Organization.DoesNotExist:
            return Response({'message' : 'Organization Not foundes'}, status=status.HTTP_404_NOT_FOUND)

        if ownership_object.organization.pk is not org.pk:
            return Response({'message' : 'you can only delete your ownership'}, status=status.HTTP_403_FORBIDDEN)

        ownership_object.content_object.delete()
        ownership_object.delete()

        return Response({'message' : 'Ownership deleted successfully'}, status=status.HTTP_200_OK)


class PaymentMethodView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, organization_pk=None):
        pass

    def post(self, request):
        pass

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        pass

