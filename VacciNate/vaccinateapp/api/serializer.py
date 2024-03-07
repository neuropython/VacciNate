from rest_framework import serializers
from vaccinateapp.models import Vaccine, User 

class VaccinateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vaccine
        fields = '__all__'