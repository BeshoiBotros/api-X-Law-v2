from django.urls import path
from . import views
urlpatterns = [

    # -Subscribe urls
    path("subscribe/", views.SubscribeView.as_view()),
    path("subscribe/<int:pk>/", views.SubscribeView.as_view()),
    # -----------------------------

    # -SubscribeOrder urls
    path("subscribe-order/", views.SubscribeOrderView.as_view()),
    path("subscribe-order/<int:pk>/", views.SubscribeOrderView.as_view()),
    #------------------------------

    # -SubscribeConstract urls
    path("subscribe-contract/", views.SubscribeContractView.as_view()),
    path("subscribe-contract/<int:pk>/", views.SubscribeContractView.as_view()),
    #------------------------------
]