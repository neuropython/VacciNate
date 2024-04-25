from rest_framework import serializers, generics
from vaccinateapp.models import Vaccine, User, UserVaccine
from .serializer import VaccinateSerializer, UserVaccineSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class VaccinateAll(generics.ListCreateAPIView):
    """
    This class is used to get all the vaccines and add a new vaccine
    
    get: Get all the vaccines   
    post: Add a new vaccine
    """
    queryset = Vaccine.objects.all()
    serializer_class = VaccinateSerializer

class VaccinateDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    This class is used to get, update and delete a vaccine
    
    get: Get a vaccine
    put: Update a vaccine
    delete: Delete a vaccine
    patch: Partial update of a vaccine
    head: check if a vaccine exists
    options: Get the allowed methods
    """
    queryset = Vaccine.objects.all()
    serializer_class = VaccinateSerializer
    
class UserVaccinateAll(generics.RetrieveUpdateDestroyAPIView):
    """
    This class is used to get all the user vaccines
    
    get: Get all the user vaccines
    put: Update a user vaccine
    delete: Delete a user vaccine
    patch: Partial update of a user vaccine
    options: Get the allowed methods
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserVaccineSerializer

    def get_queryset(self):
        user = self.request.user
        return  UserVaccine.objects.filter(user__username=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        
        serializer.save(user=user)