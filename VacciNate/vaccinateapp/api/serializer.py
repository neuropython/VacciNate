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
        
    def create(self, validated_data):
        user = User.objects.get(username=validated_data.pop('user'))
        vaccine = Vaccine.objects.get(name=validated_data.pop('vaccine'))
        return UserVaccine.objects.create(user=user, vaccine=vaccine, **validated_data)
        