
from django.urls import path
from .api.views import registration_view, logout_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]