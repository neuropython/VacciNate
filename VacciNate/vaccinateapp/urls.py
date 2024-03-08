from django.contrib import admin
from django.urls import path, include
from django.urls import include
from .api.views import (VaccinateAll,
                        UserVaccinateAll)

urlpatterns = [
    path('list/', VaccinateAll.as_view(), name='vaccination-list'),
    path('user/', UserVaccinateAll.as_view(), name='user-vaccination-list')
]
