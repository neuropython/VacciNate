from django.contrib import admin
from django.urls import path, include
from django.urls import include
from .api.views import (VaccinateAll,
                        UserVaccinateAll,
                        VaccinateDetail,
                        UserVaccineDetail)

urlpatterns = [
    path('list/', VaccinateAll.as_view(), name='vaccination-list'),
    path('detail/<int:pk>/', VaccinateDetail.as_view(), name='vaccination-detail'),
    path('user/', UserVaccinateAll.as_view(), name='user-vaccination-list'),
    path('uservaccine/<int:id>/', UserVaccineDetail.as_view(), name='uservaccine-delete'),
]
 