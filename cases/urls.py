from django.urls import path
from . import views

urlpatterns = [
    # category URLs
    path('category/', views.CategoryView.as_view()),
    path('category/<int:pk>/', views.CategoryView.as_view()),

    #sub category URLs

    # news URLs
    path('new/', views.NewView.as_view()),
    path('new/<int:pk>/', views.NewView.as_view()),
    
    # Cases URLs
    path('case/', views.SolvedCaseView.as_view()),
    path('case/<int:pk>', views.SolvedCaseView.as_view()),
]
