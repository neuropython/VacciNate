from datetime import datetime

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from vaccinateapp.models import User, Vaccine, UserVaccine
from .serializer import VaccinateSerializer, UserVaccineSerializer
from rest_framework import generics, serializers, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


class VaccinateAll(generics.ListCreateAPIView):
    queryset = Vaccine.objects.all()
    serializer_class = VaccinateSerializer

class VaccinateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vaccine.objects.all()
    serializer_class = VaccinateSerializer
    
class UserVaccinateAll(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserVaccineSerializer
    lookup_field = None  


    def get_queryset(self):
        user = self.request.user
        return UserVaccine.objects.filter(user__username=user.username) 
       
    def perform_create(self, serializer):
            user = self.request.user
            
            vaccine_id = self.request.data.get('vaccine_id')
            vaccine = Vaccine.objects.filter(id=vaccine_id).first()

            if not vaccine:
                return HttpResponseBadRequest("The specified vaccine does not exist.")

            fist_date = self.request.data.get('fist_date')
            fist_date = datetime.strptime(fist_date, '%Y-%m-%d').date() if fist_date else None
            serializer.save(user=user, vaccine=vaccine, fist_date=fist_date)

class UserVaccineDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = UserVaccineSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return UserVaccine.objects.filter(user=user)

@csrf_exempt
@require_http_methods(["POST"])
@permission_classes([IsAuthenticated])
def cancel(request, id):
    object = UserVaccine.objects.get(id = id)
    print(object.status)
    object.status = "cancelled"
    object.save()
    return HttpResponse("Vaccine cancelled")
    
@csrf_exempt
@require_http_methods(["PATCH"])
@permission_classes([IsAuthenticated])
def update_date (request, id, old_date, new_date):
    object = UserVaccine.objects.get(id = id)
    if old_date not in object.all_dates:
        return HttpResponseBadRequest("The specified date does not exist.")
    if new_date in object.all_dates:
        return HttpResponseBadRequest("The specified date already exists.")
    if new_date < object.fist_date:
        return HttpResponseBadRequest("The specified date is earlier than the first date.")
    if new_date < datetime.now().date():
        return HttpResponseBadRequest("The specified date is earlier than today.")
    object.all_dates[object.all_dates.index(old_date)] = new_date
    object.save()
    return HttpResponse("Date updated")
    