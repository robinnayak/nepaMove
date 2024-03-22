from rest_framework import serializers
from . import models

class CustomUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=5,label='confirm_password',write_only=True)
    class Meta:
        model = models.CustomUser
        fields = ['username', 'email','password','password1' ,'phone_number', 'is_driver']
        extra_kwargs = {'password':{'write_only':True}}
        # exclude = ['password1'] #we cannot use exclude and fields at same time 

    def validate(self, data):
        password = data.get('password')
        password1 = data.get('password1')
        
        if password != password1:
            raise serializers.ValidationError({"password":"Password must match!!"})
        return data


    def create(self, validated_data):
        validated_data.pop('password1',None)
        user = models.CustomUser.objects.create_user(**validated_data)
        return user
    
    def to_representation(self, instance):
        # Exclude 'password1' from the serialized data when using the GET method
        request = self.context.get('request')
        method = request.method if request else None

        if method == 'GET':
            self.fields.pop('password1', None)

        return super().to_representation(instance)
    
class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100,label="username")
    password = serializers.CharField(min_length=5,label="password")


        