from django.shortcuts import render
from . import serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import models
from XLaw import shortcuts
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from XLaw import settings
from . import filters
from drf_yasg.utils import swagger_auto_schema


class LimitView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        
        can_view = shortcuts.check_permission(permission_name='view_limit', request=request)

        if not can_view:
            return Response({'message':'you can not perform this action'}, status=status.HTTP_403_FORBIDDEN)

        if pk:
            instance = shortcuts.object_is_exist(pk, models.Limit, 'This limit not found')
            serializer = serializers.LimitSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

        queryset = models.Limit.objects.all()
        filter_set = filters.LimitFilter(request.GET, queryset)

        if filter_set.is_valid():
            queryset = filter_set.qs
        
        serializer = serializers.LimitSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializers.LimitSerializer)
    def post(self, request):

        can_add = shortcuts.check_permission('add_limit', request)

        if not can_add:
            return Response({'message' : 'you can not perform this action'}, status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.LimitSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.LimitSerializer)
    def patch(self, request, pk):

        can_update = shortcuts.check_permission('change_limit', request)

        if not can_update:
            return Response({'message' : 'you can not perform this action'}, status=status.HTTP_403_FORBIDDEN)

        instance = shortcuts.object_is_exist(pk, models.Limit, 'This limit not found')

        serializer = serializers.LimitSerializer(instance=instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):

        can_delete = shortcuts.check_permission('delete_limit', request)

        if not can_delete:
            return Response({'message' : 'you can not perform this action'}, status=status.HTTP_403_FORBIDDEN)

        instance = shortcuts.object_is_exist(pk, models.Limit, 'This limit not found')

        instance.delete()

        return Response({'message' : 'limit deleted successfully'}, status=status.HTTP_200_OK)

class SubscribeView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):

        if pk:
            subscribe_instance = shortcuts.object_is_exist(pk, models.Subscribe, "subscribe not found")
            if subscribe_instance.is_active:
                subscribe_serializer = serializers.SubscribeSerializer(subscribe_instance)
                return Response(subscribe_serializer.data, status=status.HTTP_200_OK)

        subscribe_queryset = models.Subscribe.objects.filter(is_active=True)
        filterset = filters.SubscribeFilter(request.GET, queryset=subscribe_queryset)

        if filterset.is_valid():
            subscribe_queryset = filterset.qs

        subscribe_serializer = serializers.SubscribeSerializer(subscribe_queryset, many=True)
        return Response(subscribe_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializers.SubscribeSerializer)
    def post(self, request):

        is_auth = shortcuts.isAuth(request)

        if not is_auth:
            return Response({'message' : 'Authentication credentials were not provided.'})

        can_add = shortcuts.check_permission('add_subscribe', request)

        if can_add:
            serializer = serializers.SubscribeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message'  : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.SubscribeSerializer)
    def patch(self, request, pk):

        is_auth = shortcuts.isAuth(request)

        if not is_auth:
            return Response({'message' : 'Authentication credentials were not provided.'})

        can_update = shortcuts.check_permission('change_subscribe', request)

        if can_update:
            instance = shortcuts.object_is_exist(pk, models.Subscribe, "Subscribe not found.")
            serializer = serializers.SubscribeSerializer(instance=instance,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message'  : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        is_auth = shortcuts.isAuth(request)

        if not is_auth:
            return Response({'message' : 'Authentication credentials were not provided.'})

        can_delete = shortcuts.check_permission('delete_subscribe', request)

        if can_delete:
            instance = shortcuts.object_is_exist(pk, models.Subscribe, "Subscribe not found.")
            instance.delete()
        else:
            return Response({'message'  : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)


class SubscribeOrderView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):

        can_view = shortcuts.check_permission('view_subscribeorder', request)

        if pk:
            instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeOrder)
            if can_view or (instance.companyuser.pk == request.user.pk):
                serialzier = serializers.SubscribeOrderSerializer(instance)
            else:
                return Response({'message':'you do not have access to perform that action'})
        else:
            if can_view:
                queryset = models.SubscribeOrder.objects.all()
                serialzier = serializers.SubscribeOrderSerializer(queryset, many=True)
            else:
                queryset = models.SubscribeOrder.objects.filter(companyuser = request.user)
                serialzier = serializers.SubscribeOrderSerializer(queryset, many=True)

        return Response(serialzier.data)


    @swagger_auto_schema(request_body=serializers.SubscribeOrderSerializer)
    def post(self, request):

        if request.user.is_lawyer:
            serializer_data = request.data.copy()
            serializer_data['companyuser'] = request.user
            serializer = serializers.SubscribeOrderSerializer(data=serializer_data) # ----------- Handel [Front-End]
            if serializer.is_valid():
                instance = serializer.save()
                send_mail(
                    "subscribe order",
                    "your order is underprocess we will check your data then asking you to complate the contract or cancel it", # ----------- Handel [Front-End]
                    settings.XLAW_EMAIL,
                    [request.user.email],
                    fail_silently=False,
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message' : 'Only lawyers can perform this action.'})

    @swagger_auto_schema(request_body=serializers.SubscribeOrderSerializer)
    def patch(self, request, pk):
        can_update = shortcuts.check_permission('change_subscribeorder', request)
        if can_update:
            instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeOrder)
            serializer = serializers.SubscribeOrderSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                validate_data = serializer.validated_data
                serializer.save()
                if validate_data.get('requestStatus') == "accepted":
                    subscribe_contract_data = {'subscribe_order' : instance.pk}
                    subscribe_contract_serializer = serializers.SubscribeContractSerializer(data=subscribe_contract_data)
                    if subscribe_contract_serializer.is_valid():
                        subscribe_contract_serializer.save()
                        send_mail(
                            "subscribe order",
                            "your subscribe order has been successfully accepted, please come to us to complate the contract",
                            settings.XLAW_EMAIL,
                            [instance.companyuser.email],
                            fail_silently=False,
                        )
                if validate_data.get('requestStatus') == 'rejected' or validate_data.get('requestStatus') == 'other':
                    try:
                        contract_instance = models.SubscribeContract.objects.get(subscribe_order=instance.pk)
                    except models.SubscribeContract.DoesNotExist:
                        pass
                    if contract_instance:
                        contract_instance.delete()
                    send_mail(
                        "subscribe order",
                        "your subscribe order has been rejected, please check the description of subscribe order to know details.",
                        settings.XLAW_EMAIL,
                        [instance.companyuser.email],
                        fail_silently=False,
                    )
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'you do not have access to perform that action'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # to cancel the subscribe order or delete it
        delete_it = request.data.get('delete', None)
        instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeOrder)
        can_delete = shortcuts.check_permission('delete_subscribeorder', request)
        if (instance.companyuser.pk == request.user.pk):
            if (instance.requestStatus != "rejected" and instance.requestStatus != "other" and instance.requestStatus != "canceled"):
                if not delete_it:
                    print(instance.requestStatus != "rejected" or instance.requestStatus != "other" or instance.requestStatus != "canceled")
                    instance.requestStatus = "canceled"
                    instance.save()
                    send_mail(
                        "subscribe order",
                        "your subscribe order has been canceled",
                        settings.XLAW_EMAIL,
                        [instance.companyuser.email],
                        fail_silently=False,
                    )
                    return Response({'message' : 'subscribe order has been canceled successfuly'}, status=status.HTTP_200_OK)
                else:
                    instance.delete()
                    return Response({'message' : 'your order has been deleted successfully.'})
            else:
                return Response({'message' : 'your orderd already canceled.'})
        elif can_delete:
                instance.delete()
                send_mail(
                    "subscribe order",
                    "your subscribe order has been deleted",
                    settings.XLAW_EMAIL,
                    [instance.companyuser.email],
                    fail_silently=False,
                )
                return Response({'message' : 'subscribe order has been deleted successfuly'}, status=status.HTTP_200_OK)
        else:
            return Response({'message' : 'you can only cancel your subscribe orders.'})

class SubscribeContractView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        can_view = shortcuts.check_permission('view_subscribecontract', request)
        if pk:
            instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeContract)
            if can_view or (instance.subscribe_order.companyuser.pk == request.user.pk):
                serialzier = serializers.SubscribeContractSerializer(instance)
            else:
                return Response({'message': 'you do not have access to perform that action'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            if can_view:
                queryset = models.SubscribeContract.objects.all()
                serialzier = serializers.SubscribeContractSerializer(queryset, many=True)
                return Response(serialzier.data, status=status.HTTP_200_OK)
            else:
                queryset = models.SubscribeContract.objects.filter(subscribe_order__companyuser=request.user.pk)
                print(queryset)
                serializer = serializers.SubscribeContractSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializers.SubscribeContractSerializer)
    def post(self, request):
        can_add = shortcuts.check_permission('add_subscribecontract', request)
        if can_add:
            serializer = serializers.SubscribeContractSerializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                company_user_email = instance.subscribe_order.companyuser.email
                # need to complate ----------------------------------------------------------------
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'you do not have access to perform that action'})

    @swagger_auto_schema(request_body=serializers.SubscribeContractSerializer)
    def patch(self, request, pk):
        can_update = shortcuts.check_permission('change_subscribecontract', request)
        instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeContract)
        if can_update:
            serializer = serializers.SubscribeContractSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if (instance.subscribe_contract_status == "paied") and (instance.is_active == True):
                    send_mail(
                        "subscribe contract",
                        "your subscribe order has been successfully accepted, please check the description of subscribe contract to know details.",
                        settings.XLAW_EMAIL,
                        [instance.subscribe_order.companyuser.email],
                        fail_silently=False,
                    )
                if instance.subscribe_contract_status == "rejected" or instance.subscribe_contract_status == "other":
                    send_mail(
                        "subscribe contract",
                        "your subscribe contract has been rejected, please check the description  of subscribe contract to know details.",
                        settings.XLAW_EMAIL,
                        [instance.subscribe_order.companyuser.email],
                        fail_silently=False,
                    )
                if instance.subscribe_contract_status == "unpaied":
                    send_mail(
                        "subscribe contract",
                        "your subscribe contract is unpaid, please make sure to paid then upload the reciept file to activate your Organization.",
                        settings.XLAW_EMAIL,
                        [instance.subscribe_order.companyuser.email],
                        fail_silently=False,
                    )
                if instance.subscribe_contract_status == "underProcess":
                    send_mail(
                        "subscribe contract",
                        "your contract is underprocess we will check your data then asking you to complate the contract or cancel it",
                        settings.XLAW_EMAIL,
                        [instance.subscribe_order.companyuser.email],
                        fail_silently=False,
                    )
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            if instance.subscribe_order.companyuser.pk == request.user.pk:
                serializer = serializers.SubscribeContractDetailsSerializer(request.data)
                if serializer.is_valid():
                    reciept_file = serializer.validated_data['reciept_file']
                    nums_of_users = serializer.validated_data['nums_of_users']
                    instance.reciept_file = reciept_file
                    instance.nums_of_users = nums_of_users
                    instance.save()
                    instance.subscribe_contract_status = 'underProcess'
                    return Response(serializers.SubscribeContractSerializer(instance).data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'you do not have access to perform that action'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeContract)
        can_delete = shortcuts.check_permission('delete_subscribecontract', request)
        if (instance.subscribe_order.companyuser.pk == request.user.pk):
            instance.subscribe_contract_status = 'canceled'
            instance.save()
            send_mail(
                "subscribe contract",
                "your subscribe contract has been canceled",
                settings.XLAW_EMAIL,
                [instance.subscribe_order.companyuser.email],
                fail_silently=False,
            )
            return Response({'message': 'subscribe contract has been canceled successfully.'}, status=status.HTTP_200_OK)
        elif can_delete :
            instance.delete()
            return Response({'message': 'instance has been deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message' : 'only admins and owners can perform this request.'})

