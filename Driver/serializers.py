from rest_framework import serializers
from .models import Driver
from account.serializers import CustomUserSerializer

class DriverProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Driver
        fields = ['user', 'license_number', 'phone_number', 'address',
                  'date_of_birth', 'driving_experience', 'rating', 'total_rides',
                  'earnings', 'availability_status', 'last_updated_location']
        # exclude = ['password']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        
        print("user: ", validated_data.get('user'))
        print("user_data: ", user_data)
        print("instance ", instance)

        if user_data:
            user_serializer = CustomUserSerializer(instance.user, data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()

        instance.license_number = validated_data.get('license_number', instance.license_number)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.driving_experience = validated_data.get('driving_experience', instance.driving_experience)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.total_rides = validated_data.get('total_rides', instance.total_rides)
        instance.earnings = validated_data.get('earnings', instance.earnings)
        instance.availability_status = validated_data.get('availability_status', instance.availability_status)
        # print("exprerience instace ",instance.driving_experience)
        instance.save()
        return instance 

#alternate 

# def update(self, instance, validated_data):
#     user_data = validated_data.pop('user', None)

#     if user_data:
#         user_serializer = CustomUserSerializer(instance.user, data=user_data)
#         if user_serializer.is_valid():
#             user_serializer.save()

#     fields_to_update = ['license_number', 'phone_number', 'address', 'date_of_birth',
#                         'driving_experience', 'rating', 'total_rides', 'earnings',
#                         'availability_status']

#     for field in fields_to_update:
#         setattr(instance, field, validated_data.get(field, getattr(instance, field)))

#     return instance
