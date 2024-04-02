from rest_framework import serializers
from vaccinateapp.models import Vaccine, User, UserVaccine

class VaccinateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vaccine
        fields = '__all__'
    
class UserVaccineSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    vaccine = serializers.StringRelatedField()
    
    class Meta:
        model = UserVaccine
        fields = '__all__'
        