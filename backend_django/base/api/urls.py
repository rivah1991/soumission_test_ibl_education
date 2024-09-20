# créer par Rivah
from django.urls import path
from . import views
from .views import MyTokenObtainPairView, langflow_endpoint

#ajouter par Rivah
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),

    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('langflow/endpoint/', langflow_endpoint, name='langflow-endpoint'),
]