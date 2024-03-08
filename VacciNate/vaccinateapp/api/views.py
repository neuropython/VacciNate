from rest_framework import serializers, generics
from vaccinateapp.models import Vaccine, User
from .serializer import VaccinateSerializer, UserVaccineSerializer

class VaccinateAll(generics.ListCreateAPIView):
    queryset = Vaccine.objects.all()
    serializer_class = VaccinateSerializer

class UserVaccinateAll(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserVaccineSerializer