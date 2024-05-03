
from django.urls import path
from .api.views import registration_view, logout_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .api.views import add_device, update_device


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('add_device/', add_device, name='add_device'),
    path('update_device/', update_device, name='update_device')
    ]