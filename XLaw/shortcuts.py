from users import models as UsersModels
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from organizations import models as org_models
from django.contrib.contenttypes.models import ContentType
from subscribes import models as subscribes_models
from django.db.models import Model
from organizations import models as organization_models


def object_is_exist(pk, model, exception="object not found"):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return Response({'message' : f'{exception}'}, status=status.HTTP_404_NOT_FOUND)

def object_is_exist_for_sockets(pk, model: Model, error_method, exception="object not found"):
    try:
        return model.objects.get(pk=pk)
    except:
        error_method(exception)


User = get_user_model()

def emailAlreadyExist(email):
    return User.objects.filter(email=email).exists()

def token_is_exist(token):
    return UsersModels.VerifyToken.objects.filter(token=token).exists()

def check_permission(permission_name, request):
    for group in request.user.groups.all():
        if group.permissions.filter(codename = permission_name):
            return True
    return False

def can_add_organization_objects(content_type_pk, request):
    try:
        org = organization_models.Organization.objects.get(user=request.user.pk)
    except:
        return Response({'message':'You do not have organization yet'}, status.HTTP_404_NOT_FOUND)
    
    contract = org.subscribe_contract
    
    if not contract:
        return Response({'message' : 'you do not have a contract file yet'}, status=status.HTTP_404_NOT_FOUND)

    organization_limits = org.subscribe_contract.subscribe_order.subscribe.limits.all()

    content_types_of_limits = []

    for limit in organization_limits:
        content_types_of_limits.append(limit.content_type.pk)

    organization_ownership_count = organization_models.ObjectOwnership.objects.filter(organization = org, content_type=content_type_pk).count()
    content_type_limit = 0
    
    for i in organization_limits:
        if content_type_pk == i.content_type.pk:
            content_type_limit = i.number_of_object
            break
    
    if (content_type_pk in content_types_of_limits) and (organization_ownership_count < content_type_limit) and (contract.is_active) and(contract.contract_aproval):
        return True
    
    else:
        return False



def get_obj_by_kwargs(model: Model, **kwargs):
    model_ = model.objects.get()
    try:
        model
        for key, val in kwargs.items():
            setattr(model_, key, val)
    except model.DoesNotExist:
        return Response({'message' : '404 not found'}, status=status.HTTP_404_NOT_FOUND)


def isAuth(request):
    try:
        user = request.user
        UsersModels.CustomUser.objects.get(pk = user.id)
        return True
    except User.DoesNotExist:
        return False