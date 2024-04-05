from rest_framework import serializers, generics
from vaccinateapp.models import Vaccine, User
from .serializer import VaccinateSerializer, UserVaccineSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


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
