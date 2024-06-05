from django.shortcuts import render
from . import models
from . import serializers
from rest_framework.views import APIView
from XLaw import shortcuts
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import filters
from drf_yasg.utils import swagger_auto_schema

class CategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):

        if pk:
            instance = shortcuts.object_is_exist(pk, models.Category, "Category not found")
            serializer = serializers.CategorySerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        queryset = models.Category.objects.all()
        
        filterset = filters.CategoryFilters(request.GET, queryset=queryset)
        
        if filterset.is_valid():
            queryset = filterset.qs
        
        serializer = serializers.CategorySerializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=serializers.CategorySerializer)
    def post(self, request):
        
        can_add_category = shortcuts.check_permission('add_category', request)
        
        if can_add_category:
            serializer = serializers.CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message' : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.CategorySerializer)
    def patch(self, request, pk):
        
        can_update_category = shortcuts.check_permission('change_category', request)
        
        instance = shortcuts.object_is_exist(pk, models.Category, 'Category not found')
        
        if can_update_category:
            serializer = serializers.CategorySerializer(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'message' : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)
            
    def delete(self, request, pk):
        
        can_delete_category = shortcuts.check_permission('delete_category', request)
        
        instance = shortcuts.object_is_exist(pk, models.Category, "Category not found")

        if can_delete_category:    
            instance.delete()
            return Response({'message' : 'the category has been deleted successfully.'}, status=status.HTTP_200_OK)
        
        return Response({'message' : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)

class SubCategoryView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        pass

    def post(self, request):
        pass

    def patch(self, request, pk):
        pass

    def delete(self, request):
        pass



class NewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        
        if pk:
            instance = shortcuts.object_is_exist(pk, models.New, "New not found")
            
            try:
                user_profile = None
            except:
                return Response({'detail':'profile not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = serializers.NewSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        queryset = models.New.objects.all()
        
        filterset = filters.CategoryFilters(request.GET, queryset=queryset)
        
        if filterset.is_valid():
            queryset = filterset.qs

        serializer = serializers.NewSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=serializers.NewSerializer)
    def post(self, request):
        
        can_add_new = shortcuts.check_permission('add_new', request)
        
        if can_add_new:
            serializer_data = request.data.copy()
            serializer_data['user'] = request.user.pk
            serializer = serializers.NewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message' : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.NewSerializer)
    def patch(self, request, pk):
        
        can_update_new = shortcuts.check_permission('change_new', request)
        
        instance = shortcuts.object_is_exist(pk, models.New, 'New not found')
        
        if instance.user.pk != request.user.pk:
            return Response({'message' : 'you can onky update your news'}, status=status.HTTP_400_BAD_REQUEST)
        
        if can_update_new:
            serializer = serializers.NewSerializer(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'message' : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        
        can_delete_new = shortcuts.check_permission('delete_new', request)

        instance = shortcuts.object_is_exist(pk, models.New, "New not found")
        
        if instance.user.pk != request.user.pk:
            return Response({'message' : 'you can only delete your news.'})
        
        if can_delete_new:
            instance.delete()
            return Response({'message' : 'the New has been deleted successfully.'}, status=status.HTTP_200_OK)
        
        return Response({'message' : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)

class SolvedCaseView(APIView):

    def get(self, request, pk=None):
        
        if pk:
            instance = shortcuts.object_is_exist(pk, models.Case, "Case not found")
            serializer = serializers.CaseSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        queryset = models.Case.objects.all()
        
        filterset = filters.CategoryFilters(request.GET, queryset=queryset)
        
        if filterset.is_valid():
            queryset = filterset.qs
            
        serializer = serializers.CaseSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=serializers.CaseSerializer)
    def post(self, request):
        
        is_Auth = shortcuts.isAuth(request)
        if not is_Auth:
            return Response({'message' : 'User not Found'}, status=status.HTTP_404_NOT_FOUND)

        can_add_case = shortcuts.check_permission('add_case', request)
        
        if can_add_case:
            serializer_data = request.data.copy()
            serializer_data['user'] = request.user.pk
            serializer = serializers.CaseSerializer(data=serializer_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'message' : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=serializers.CaseSerializer)
    def patch(self, request, pk):

        is_Auth = shortcuts.isAuth(request)
        if not is_Auth:
            return Response({'message' : 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        can_update_case = shortcuts.check_permission('change_case', request)
        
        instance = shortcuts.object_is_exist(pk, models.Case, 'Case not found')

        if instance.user.pk != request.user.pk:
            return Response({'message' : 'you can only update your cases.'})
        
        if can_update_case:
            serializer = serializers.CaseSerializer(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'message' : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        
        is_Auth = shortcuts.isAuth(request)
        if not is_Auth:
            return Response({'message' : 'User not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        can_delete_case = shortcuts.check_permission('delete_case', request)
        
        if can_delete_case:
            instance = shortcuts.object_is_exist(pk, models.Case, "Case not found")
            if instance.user.pk is not request.user.pk:
                return Response({'message' : 'you can only delete your cases.'})
            instance.delete()
            return Response({'message' : 'the Case has been deleted successfully.'}, status=status.HTTP_200_OK)
        
        return Response({'message' : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)


class CaseView(APIView):

    def get(self, request, pk=None, user_pk=None):
        pass

    def post(self, request):
        pass

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        pass


class CaseInvitation(APIView):

    def get(self, request, pk=None, user_pk=None):
        pass

    def post(self, request):
        pass

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        pass