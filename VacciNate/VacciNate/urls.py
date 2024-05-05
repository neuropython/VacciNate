from django.contrib import admin
from django.urls import path, include
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vaccinate/', include('vaccinateapp.urls')),
    path('user/', include('userapp.urls')), 
]