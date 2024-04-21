from rest_framework import serializers
from . import models 

from account.serializers import CustomUserSerializer

class PassengerProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = models.Passenger
        fields = ['user','phone_number','address','emergency_contact_name',
                  'emergency_contact_number','date_of_birth','preferred_language'
                  ]
        
    