from django.shortcuts import render,HttpResponse
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from django.views.generic import View
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
# from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
# Create your views here.
from . import serializers
from Driver.models import Driver
from passenger.models import Passenger
from . import models


def index(request):
    return HttpResponse("hello world!!")

class HomeView(APIView):
    def get(self,request,*args,**kwargs):
        return Response({"msg":"home page!!"}, status=status.HTTP_200_OK)


@csrf_exempt
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken':request.META['CSRF_COOKIE'],'csrfToken1':token})

# class UserView(APIView):
#     def get(self,request,*args,**kwargs):
#         user = models.CustomUser.objects.all()
#         return Response({ "user":user},status=status.HTTP_200_OK)

class RegistrationView(APIView):
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    Licence_no = '123456789'
    phone_number = '12345608'
    address = "Jankapur, Nepal"
    date_of_birth = timezone.now()

    def get(self,request,*args,**kwargs):
        users = models.CustomUser.objects.all()
        serializer = serializers.CustomUserSerializer(users,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request,*args,**kwargs):
        serializer = serializers.CustomUserSerializer(data=request.data)
        print("is_driver",request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                print(user.is_driver)
                if user.is_driver:
                    driver_group = Group.objects.get(name='driver')
                    print("group_driver",driver_group)
                    user.groups.add(driver_group)
                    driver =  Driver.objects.create(
                        user = user,
                        )
                    print("driver",driver)
                else:
                    passenger_group = Group.objects.get(name="passenger")
                    print("passenger group", passenger_group)
                    user.groups.add(passenger_group)
                    passenger = Passenger.objects.create(
                        user = user,
                    )
                    print("passenger: ",passenger)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"err":serializer.errors,"msg":"register as a driver"},status=status.HTTP_400_BAD_REQUEST)
        except Group.DoesNotExist:
            return Response({"error": "Driver group does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error",e)
            return Response({"error":"Register page error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          

class CustomLoginView(APIView):
    def get(self,request,*args,**kwargs):
        return Response("welcome to login page",status=status.HTTP_200_OK)
    def post(self,request,*args,**kwargs):
        serializer = serializers.CustomLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                print("login successful!!!",user)
            # print("data",serializer.data)
            # print("username data",serializer.data['username'])
            return Response({'msg':"login successful",'data':serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CustomLogoutView(APIView):
    is_logout = False
    def get(self,request,*args,**kwargs):
        try:
            # print("request user",request.user)
            if request.user:
                # print("request user",request.user)
                user = logout(request)
                self.is_logout = True
                print("user",user)
                return Response({"message":"Logout Successful","is_logout":self.is_logout},status=status.HTTP_200_OK)
            else:
                return Response({"message":"user is not authenticated"},status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError):
            return Response ({"message": "User is not authenticated"},status=status.HTTP_401_UNAUTHORIZED)
            