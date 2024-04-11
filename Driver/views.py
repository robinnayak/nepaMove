from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
# Create your views here.
from . import models
from account.models import CustomUser
from . import serializers
from passenger.models import Passenger
class DriverProfile(APIView):
    def get(self,request,*args,**kwargs):
        username = kwargs.get('username')
        try:    
            user = CustomUser.objects.get(username=username)
            driver_profile = models.Driver.objects.get(user=user)
            serializer = serializers.DriverProfileSerializer(driver_profile)
        except CustomUser.DoesNotExist:
            return Response({'error':'Driver not found'},status=status.HTTP_404_NOT_FOUND)
            
        return Response({"msg":"welcome to profile page","user":serializer.data},status=status.HTTP_200_OK)

    def put(self,request,*args,**kwargs):
        username = kwargs.get('username')
        is_update = False
        try:
            user = CustomUser.objects.get(username=username)
            driver_profile = models.Driver.objects.get(user=user)
            serializer = serializers.DriverProfileSerializer( driver_profile , data=request.data)
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
    

class VehicleView(APIView):
    def get(self, request, format=None):
        try:
            vehicles = models.Vehicle.objects.all()  # Use plural for clarity
            serializer = serializers.VehicleSerializer(vehicles, many=True)
            # print("vehicle data",vehicles)
            # print("serializer data",serializer.data)
            
            return Response({"msg": "Vehicle list retrieved", "data": serializer.data}, status=status.HTTP_200_OK)
        except models.Vehicle.DoesNotExist:
            return Response({"error": "No vehicles found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        serializer = serializers.VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Vehicle created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class Test(APIView):
#     def get(self,request,*args,**kwargs):
#         return Response({"msg":"test page"},status=status.HTTP_200_OK)
    

   
class VehicleDetailView(APIView):
    def get(self,request,*args,**kwargs):
        license_plate_number = kwargs.get("licence_plate_number")        
        return Response({"msg":"vehicle detail view","data":license_plate_number})
    
    def put(self,request,*args,**kwargs):
        license_plate_number = kwargs.get("licence_plate_number")
        try:
            vehicles = models.Vehicle.objects.get(license_plate_number=license_plate_number)
            serializer = serializers.VehicleSerializer(vehicles,data=request.data)
            if serializer.is_valid():
                serializer.save()
            
            return Response ({"msg":"updated","data":serializer.data},status=status.HTTP_200_OK)
            
        except models.Vehicle.DoesNotExist:
            return Response({"error":"vehicle not found !!"},status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e :
            error_response = {'error':f'Driver Profile Error: {str(e)}'}
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self,request,*args,**kwargs):
        license_plate_number = kwargs.get("licence_plate_number")        
        # print("args",args)
        try:
            vehicle = models.Vehicle.objects.get(license_plate_number=license_plate_number)
            
        except models.Vehicle.DoesNotExist:
            return Response({"error":"Vehicle not found"},status=status.HTTP_404_NOT_FOUND)
        
        vehicle.delete()
        return Response({"message":"Vehicle deleted successfully"},status=status.HTTP_204_NO_CONTENT)     
            
class TripView(APIView):
    def get(self, request, *args, **kwargs):
        trips = models.Trip.objects.all()
        serializer = serializers.TripSerializer(trips, many=True)  # Serialize all trips

        # Handle successful retrieval
        try:
            return Response({"msg": "Trip API ((janakpur) -> (Kathmandu))", "data": serializer.data}, status=status.HTTP_200_OK)
        # Handle case where no trips found
        except models.Trip.DoesNotExist as e:
            return Response({f"msg": "No trips found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as err:
            error_response = {'err':err, 'serialier_error':serializer.errors}
            return Response(error_response,status=status.HTTP_400_BAD_REQUEST)
        
    def post(self,request,*args,**kwargs):
        serializer = serializers.TripSerializer(data=request.data)    
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"New Trip created successfuly!", 'data':serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TripDetail(APIView):
    def get(self,request,*args,**kwargs):
        tripid = kwargs.get('tripid')
        
        if not tripid :
            return Response({"error":"Missing 'from ' or 'to' location in request"}, status=status.HTTP_400_BAD_REQUEST)
        
        trips = get_object_or_404(models.Trip ,trip_id=tripid)
        # trips = models.Trip.objects.get(trip_id=tripid)
        print("trips : ",trips)
        try:
            # if not trips:
            #     return Response({"msg":f"No trips found from {trip_from} to {trip_to}"},status=status.HTTP_404_NOT_FOUND)
            serializer = serializers.TripSerializer(trips)
            return Response({"msg":f"Trip Api ({tripid}) ","data":serializer.data},status=status.HTTP_200_OK)
        except models.Trip.DoesNotExist:
            return Response({"err":f"Trip Doesnot exist {tripid}"})
        
        except Exception as e:
            error_response = {"error": f'Trip Profile Error {e}'}
            return Response(error_response,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,*args,**kwargs):
        trip_id = kwargs.get('tripid')
        if not trip_id:
            return Response({"error":"Missing 'from' or 'to' location in request"},status=status.HTTP_400_BAD_REQUEST)
        
        trips = get_object_or_404(models.Trip,trip_id=trip_id)
        try:
            serializer = serializers.TripSerializer(trips,data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response({"msg":f"Trip Api for {trip_id} is updated successfully","data": serializer.data},status=status.HTTP_200_OK)
        
        except Exception as e:
            error_response = {"err": str(e), "serializer_error":serializer.errors}    
            return Response(error_response,status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self,*args,**kwargs):
        trip_id = kwargs.get("tripid")
        try:
            trip = get_object_or_404(models.Trip, trip_id=trip_id)
            trip.delete()
            return Response({"msg":f"trip with this id {trip_id} id deleted successfully!!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_response = {"err": str(e)}    
            return Response(error_response,status=status.HTTP_400_BAD_REQUEST)
            

class TripPriceView(APIView):
    def get(self,request,*args,**kwargs):
        trip_price = models.TripPrice.objects.all()
        serializer = serializers.TripPriceSerializer(trip_price,many=True)
        if not serializer.data:
            return Response({"error":"No trip price found"},status=status.HTTP_404_NOT_FOUND)
        
        try:
            msg = {"msg":"Trip Price Api ", "data":serializer.data}
            return Response(msg,status=status.HTTP_200_OK)
        except models.TripPrice.DoesNotExist:
            return Response({"err":"Trip price Does Not Exist"})
        except Exception as err:
            error_response = {"error":err, "serializer_error":serializer.errors}
            return Response(error_response,status=status.HTTP_400_BAD_REQUEST)
        
    def post(self,request,*args,**kwargs):
        vehicle_registration= request.data.get('vehicle_registration')
        trip_id = request.data.get('trip_id')
        serializer = serializers.TripPriceSerializer(data=request.data,context={
            "vehicle_registration":vehicle_registration,
            "trip_id" : trip_id
            })
        if serializer.is_valid():
            try:
                serializer.save()
                message= {"msg":"Trip Price successfully created!" ,"data":serializer.data}
                return Response(message,status=status.HTTP_201_CREATED)
            
            except Exception as err:
                return Response({"err":str(err)},status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class TripPriceDetailView(APIView):
    def get(self,request,*args,**kwargs):
        trip_price_id = kwargs.get('trip_price_id')
        trip_price = get_object_or_404(models.TripPrice,trip_price_id=trip_price_id)
        serializer = serializers.TripPriceSerializer(trip_price)
        if not serializer.data:
            return Response({"error":f"No Trip Price related to this id : {trip_price_id}"})
        try:
            msg = {"msg":f"Trip Price API for this id : {trip_price_id}","data":serializer.data}
            return Response(msg,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e),"serializer_error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,*args,**kwargs):
        trip_price_id = kwargs.get('trip_price_id')
        vehicle_registration = request.data.get('vehicle_registration')
        trip_id = request.data.get('trip_id')
        trip_price = get_object_or_404(models.TripPrice,trip_price_id=trip_price_id)
        
        serializer = serializers.TripPriceSerializer(trip_price,data=request.data,context={
                "vehicle_registration":vehicle_registration,
                "trip_id" : trip_id
            })
        if serializer.is_valid():
            try:
                serializer.save()
                message = {"msg": f"Trip Price successfully created for this id {trip_price_id}!","data":serializer.data}
                return Response(message,status=status.HTTP_201_CREATED)        
            except Exception as e:
                return Response({"err":str(e)},status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,*args,**kwargs):
        trip_price_id = kwargs.get('trip_price_id')
        if not trip_price_id:
            return Response({"msg":"you must give a trip price id (JANKATXYZ1234) "})
        trip_price = get_object_or_404(models.TripPrice,trip_price_id=trip_price_id)
        try:
            trip_price.delete()
            return Response({"msg":f"trip price with this id {trip_price_id} is deleted successfully!!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"err":str(e)},status=status.HTTP_400_BAD_REQUEST)

class BookingView(APIView):
    def get(self,request,*args,**kwargs):
        passenger = request.user
        print("passenger",passenger)
        passenger_data = Passenger.objects.get(user =passenger)
        print("passenger data" ,passenger_data.phone_number)
        booking = models.Booking.objects.all()
        serializer =serializers.BookingSerializer(booking,many=True)
        if not serializer.data:
            return Response({"msg":"No booking data found"})
        try:
            msg = {"msg":"Booking Profile APi ","data":serializer.data}
            return Response(msg,status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"err":str(err)},status=status.HTTP_400_BAD_REQUEST)
        
    def post(self,request,*args,**kwargs):
        passenger = request.user
        trip_price_id = request.data.get('trip_price_id')
        serializer = serializers.BookingSerializer(data=request.data, context={
            "passenger" : passenger,
            "trip_price_id" : trip_price_id
        })
        if serializer.is_valid():
            try:
                ticket = serializer.save()
                # ticket_serializer = serializers.TicketSerializer()
                print("ticket",ticket)
                msg = {"msg": "Booking is successfully created!!","data":serializer.data}
                return Response(msg,status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"err":str(e)},status=status.HTTP_400_BAD_REQUEST)
        return Response({"err":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    
class BookingDetail(APIView):
    def get(self,request,*args,**kwargs):
        booking_id = kwargs.get('booking_id')
        booking = get_object_or_404(models.Booking,booking_id=booking_id)
        serializer = serializers.BookingSerializer(booking)
        if not serializer.data:
            return Response({"error":f"No Booking Found With this id {booking_id}"})
        try: 
            msg = {"msg":f"Booking Api for this id {booking_id} ", "data":serializer.data}
            return Response(msg,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"err":str(e),"serializer_error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,*args,**kwargs):
        booking_id = kwargs.get('booking_id')
        passenger = request.user
        trip_price_id = request.data.get('trip_price_id')
        booking = get_object_or_404(models.Booking,booking_id=booking_id)
        trip_from = booking.tripprice.trip.from_location
        trip_to = booking.tripprice.trip.to_location
        serializer = serializers.BookingSerializer(booking,data=request.data,context={
            "trip_price_id" : trip_price_id
        })
        if serializer.is_valid():
            try:
                ticket = serializer.save()
                print("updated ticket: ", ticket)
                msg= {"msg":f"Trip from {trip_from} to {trip_to} successfully created!! ","data":serializer.data,"updated_ticket":ticket}
                return Response(msg,status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error":str(e)},status= status.HTTP_400_BAD_REQUEST)
        return Response({"err":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,*args,**kwargs):
        booking_id = kwargs.get('booking_id')
        if not booking_id:
            return Response({"msg":f"you must need to give a booking id (PASSENGER2JANKATXYZ1234)"})
        
        booking = get_object_or_404(models.Booking, booking_id=booking_id)
        try:
            booking.delete()
            return Response({"msg":f"booking for this id {booking_id} id deleted successfully!! "})
        
        except Exception as e:
            return Response({"err":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        