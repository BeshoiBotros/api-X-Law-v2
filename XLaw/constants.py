from organizations import models as organization_models
from users import models as user_models
from cases import models as case_models
from subscribes import models as subscribe_models

from organizations import serializers as organization_serializers
from users import serializers as user_serializer
from cases import serializers as case_serializers
from subscribes import serializers as subscribe_serializers

MODEL_TO_SERIALIZER = {

    # organization_models.ObjectOwnership : organization_serializers.OwnershipSerializer,
    # organization_models.Organization    : organization_serializers.OrganizationSerializer,
    # organization_models.PaymentMethod   : organization_serializers.PaymentMethodSerializer,

    user_models.Client : user_serializer.ClientSerializer,
    user_models.Lawyer : user_serializer.LawyerSerializer,
    
    case_models.Case : case_serializers.SolvedCaseSerializer,
    case_models.SolvedCase : case_serializers.CaseSerializer,
    

}