from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('send-email-confirmation/', views.CustomUserEmail.as_view()), # for send email confirmation as client or Lawyer
    path('client/confirm-email/<str:token>/', views.ClientRegistration.as_view()),
    path('lawyer/confirm-email/<str:token>/', views.LawyerRegistration.as_view()),
    path('operations/<int:pk>/', views.CustomUserView.as_view()),
    path('operations/', views.CustomUserView.as_view()),
    path('profiles/profile/<int:pk>/', views.LawyerProfileView.as_view()),
    path('profiles/profile/lawyer/<int:user_pk>/', views.LawyerProfileView.as_view()),
    path('profiles/profile/', views.LawyerProfileView.as_view()),
]
