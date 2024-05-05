from django.contrib import admin
from django.urls import path, include
from django.urls import include
from .api.views import (VaccinateAll,
                        UserVaccinateAll,
                        VaccinateDetail,
                        UserVaccineDetail, 
                        cancel,
                        update_date,
                        update_dose,
                        notify_user_test)

urlpatterns = [
    path('list/', VaccinateAll.as_view(), name='vaccination-list'),
    path('detail/<int:pk>/', VaccinateDetail.as_view(), name='vaccination-detail'),
    path('user/', UserVaccinateAll.as_view(), name='user-vaccination-list'),
    path('uservaccine/<int:id>/', UserVaccineDetail.as_view(), name='uservaccine-delete'),
    path('uservaccine/cancel/<int:id>/', cancel , name='uservaccine-cancel'),
    path('uservaccine/update_date/<int:id>/<str:old_date>/<str:new_date>/', update_date, name='uservaccine-update'),
    path("uservaccine/update_dose/<int:id>", update_dose, name="uservaccine-update-dose"),
    path("notify/", notify_user_test, name="notify")
    ]
 