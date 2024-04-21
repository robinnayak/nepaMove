from rest_framework import serializers
from . import models
from account.serializers import CustomUserSerializer
from passenger.serializers import PassengerProfileSerializer
from passenger.models import Passenger
class DriverProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = models.Driver
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

class VehicleSerializer(serializers.ModelSerializer):
    driver = DriverProfileSerializer(read_only=True)
    class Meta:
        model = models.Vehicle
        fields = [
            'driver',
            'registration_number',
            'vehicle_type',
            'company_made',
            'model',
            'age',
            'color',
            'seating_capacity',
            'license_plate_number',
            'insurance_expiry_date',
            'fitness_certificate_expiry_date',
            'image',
            'available_seat',
            ]
    # need to add the save method for the vehicle model tomorrow
    
    def create(self, validated_data):
        driver_context = self.context
        print("driver username",driver_context)
        driver_username = driver_context.get('username')
        user = models.CustomUser.objects.get(username=driver_username) 
        driver = models.Driver.objects.get(user=user)
        validated_data['driver'] = driver
        vehicle = models.Vehicle.objects.create(**validated_data)
        # driver_data = validated_data.pop('driver')
        # print("driver data",driver_data)    
        return vehicle
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trip
        fields = ['trip_id','from_location','to_location','start_datetime','end_datetime']

class TripPriceSerializer(serializers.ModelSerializer):
    
    vehicle = VehicleSerializer(read_only=True)
    trip = TripSerializer(read_only=True)
    class Meta:
        model = models.TripPrice
        fields = ['trip_price_id','trip','vehicle','price']
        # exclude= ['vehicle_registration','trip_id']
        
    
    def create(Self, validated_data):
        # vehicle_registration = validated_data['vehicle_registration']
        # trip_id = validated_data['trip_id']
        license_plate_number = Self.context.get('vehicle_registration')
        trip_id = Self.context.get('trip_id')
        print("trip-id serializer",trip_id)
        print("vehicle_registration serializer",license_plate_number)
        vehicle = models.Vehicle.objects.get(license_plate_number=license_plate_number)
        trip = models.Trip.objects.get(trip_id=trip_id)
        # print ("vehicle serializer :",vehicle)
        # print ("trip serializer :",trip )
        trip_price = models.TripPrice.objects.create(
            vehicle=vehicle,
            trip = trip,
            **validated_data
        )
        return trip_price
    
    def update(self, instance, validated_data):
        vehicle_registration = self.context.get('vehicle_registration')
        trip_id = self.context.get('trip_id')
        # print("trip-id serializer",trip_id)
        # print("vehicle_registration serializer",vehicle_registration)
        instance.price = validated_data['price']
        # print("validated price : ",validated_data['price'])
        # print("instance vehicle registration", instance.trip)
        if vehicle_registration != instance.vehicle.registration_number:
            vehicle = models.Vehicle.objects.get(registration_number=vehicle_registration)
            instance.vehicle = vehicle
            # print ("instance vehicle", instance.vehicle)
        if trip_id != instance.trip.trip_id:
            trip = models.Trip.objects.get(trip_id=trip_id)
            instance.trip = trip
        
        instance.save()
        return instance
        
class BookingSerializer(serializers.ModelSerializer):
    tripprice = TripPriceSerializer(read_only=True) 
    passenger = PassengerProfileSerializer(read_only=True)
    class Meta:
        model = models.Booking
        fields = ['booking_id','passenger','tripprice','num_passengers','price']
        
    def create(self, validated_data):
        trip_price_id = self.context.get('trip_price_id')
        passenger_username = self.context.get('passenger')
        passenger = Passenger.objects.get(user=passenger_username)
        trip_price = models.TripPrice.objects.get(trip_price_id=trip_price_id)
        
        booking = models.Booking.objects.create(
            passenger = passenger,
            tripprice = trip_price,
            **validated_data,
        )   
        
        return booking 
   
    def update(self, instance, validated_data):
        trip_price_id = self.context.get('trip_price_id')
        
        if trip_price_id!=instance.tripprice.trip_price_id:
            trip_price = models.TripPrice.objects.get(trip_price_id=trip_price_id)
            instance.tripprice = trip_price
        
        if instance.num_passengers != validated_data['num_passengers']:
            instance.num_passengers = validated_data['num_passengers']
        instance.save()
        return instance    
        

class TicketSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    class Meta:
        model = models.Ticket
        fields = ['booking','ticket_file']
        
        
#================================optional========================================

# class TripPriceLocationFilterSerializer(serializers.Serializer):
#     from_location = serializers.CharField()
#     to_location = serializers.CharField()   
#     tripPrice = TripPriceSerializer(read_only=True)
#     def create(self, validated_data):
#         pass