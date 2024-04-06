from rest_framework import serializers, generics
from vaccinateapp.models import Vaccine, User, UserVaccine
from .serializer import VaccinateSerializer, UserVaccineSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.http import HttpResponseBadRequest

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