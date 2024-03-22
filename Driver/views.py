from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
# Create your views here.
from . import models
from account.models import CustomUser
from .serializers import DriverProfileSerializer
class DriverProfile(APIView):
    def get(self,request,*args,**kwargs):
        username = kwargs.get('username')
        try:    
            user = CustomUser.objects.get(username=username)
            driver_profile = models.Driver.objects.get(user=user)
            serializer = DriverProfileSerializer(driver_profile)
        except CustomUser.DoesNotExist:
            return Response({'error':'Driver not found'},status=status.HTTP_404_NOT_FOUND)
            
        return Response({"msg":"welcome to profile page","user":serializer.data},status=status.HTTP_200_OK)

    def put(self,request,*args,**kwargs):
        username = kwargs.get('username')
        is_update = False
        try:
            user = CustomUser.objects.get(username=username)
            driver_profile = models.Driver.objects.get(user=user)
            serializer = DriverProfileSerializer( driver_profile , data=request.data)
            # print("serializer",serializer)
            if serializer.is_valid():
                serializer.save()
                is_update = True
                return Response({"is_update":is_update,"user_data":serializer.data},status=status.HTTP_200_OK)
            else:
                error_response={
                    "error":"Validation Error",
                    "details":serializer.errors
                }
                return Response(error_response,status=status.HTTP_400_BAD_REQUEST) 
        except CustomUser.DoesNotExist:
            error_response = {'error':'Driver not found'}
            return Response(error_response,status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e :
            error_response = {'error':f'Driver Profile Error: {str(e)}'}
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    