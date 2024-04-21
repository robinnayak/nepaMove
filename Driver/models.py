from django.db import models
from account.models import CustomUser
from passenger.models import Passenger
from rest_framework import serializers
from django.utils import timezone
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# Create your models here.

# class VehicleAdmin(models.Model):
#     count = 1
#     REGISTRATION_CHOICES = (
#         ('car', 'Car'),
#         ('van', 'Van'),
#         ('motorcycle', 'Motorcycle'),
#         # Add more vehicle types as needed
#     )

#     driver = models.ForeignKey(Driver, on_delete=models.CASCADE)  # Link to driver
#     registration_number = models.CharField(max_length=20, unique=True)
#     vehicle_type = models.CharField(max_length=10, choices=REGISTRATION_CHOICES)
#     company_made = models.CharField(max_length=50)
#     model = models.CharField(max_length=50)
#     age = models.IntegerField()
#     color = models.CharField(max_length=30)
#     seating_capacity = models.PositiveIntegerField(default=0)
#     license_plate_number = models.CharField(max_length=10, unique=True)
#     insurance_expiry_date = models.DateField()  # Ensure insurance validity
#     fitness_certificate_expiry_date = models.DateField()  # Track vehicle fitness
#     image = models.ImageField(upload_to='vehicle_images', blank=True)  # Optional image
#     available_seat = models.PositiveIntegerField(default=0)

#     def save(self,*args,**kwargs):
#         if self.available_seat ==0:
#             if self.count==1:
#                 self.available_seat = self.seating_capacity
#                 self.count = self.count + 1
#         elif self.available_seat <= 0:
#             # Raise a ValidationError for not enough available seats
#             raise serializers.ValidationError("Not enough available seats!!")
#         super().save(*args,**kwargs)
            
#     def __str__(self):
#         return f"{self.registration_number} - {self.company_made} {self.model}"


class Driver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=20,blank=True)
    phone_number = models.CharField(max_length=15,blank=True)
    address = models.CharField(max_length=255,blank=True)
    date_of_birth = models.DateField(blank=True,null=True)
    driving_experience = models.IntegerField(default=1)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    total_rides = models.PositiveIntegerField(default=0)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    availability_status = models.BooleanField(default=True)
    
    # Additional fields for tracking
    # current_location = models.PointField(null=True)  # Using GeoDjango for location tracking
    last_updated_location = models.DateTimeField(auto_now=True)
    

    def __str__(self) -> str:
        return self.user.username
    
class Trip(models.Model):
    trip_id = models.CharField(max_length = 100,unique=True,default="JNKKTM")
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
        
    def save(self,*args,**kwargs):
        prefix = f"{self.from_location[:3]}{self.to_location[:3]}"
        self.trip_id = prefix.upper()
        super().save(*args,**kwargs)
    
    
    def __str__(self):
        return f"{self.trip_id} - {self.start_datetime}"

class Vehicle(models.Model):
    count = 1
    REGISTRATION_CHOICES = (
        ('car', 'Car'),
        ('van', 'Van'),
        ('motorcycle', 'Motorcycle'),
        # Add more vehicle types as needed
    )

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)  # Link to driver
    registration_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=REGISTRATION_CHOICES)
    company_made = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    age = models.IntegerField()
    color = models.CharField(max_length=30)
    seating_capacity = models.PositiveIntegerField(default=0)
    license_plate_number = models.CharField(max_length=10, unique=True)
    insurance_expiry_date = models.DateField(auto_now_add=True)  # Ensure insurance validity
    fitness_certificate_expiry_date = models.DateField(auto_now_add=True)  # Track vehicle fitness
    image = models.ImageField(upload_to='vehicle_images', blank=True)  # Optional image
    available_seat = models.PositiveIntegerField(default=0)

    def save(self,*args,**kwargs):
        if self.available_seat ==0:
            if self.count==1:
                self.available_seat = self.seating_capacity
                self.count = self.count + 1
        elif self.available_seat <= 0:
            # Raise a ValidationError for not enough available seats
            raise serializers.ValidationError("Not enough available seats!!")
        super().save(*args,**kwargs)
            
            
            
    def get_booked_seats_by_passennger(self,passenger):
        bookings = Booking.objects.filter(Vehicle=self,user=passenger)
        total_passenger_booked_seats = sum(booking.num_passenger for booking in bookings)
        return total_passenger_booked_seats
    
    # def update_available_seat(self,num_passengers):
    #     if self.available_seat - num_passengers >0:
    #         self.available_seat = self.available_seat - num_passengers
    #         self.save()
    #     else:
    #         raise ValueError("Not enough available seats in the vehicle")
    
    def __str__(self):
        return f"{self.registration_number} - {self.company_made} {self.model}"

class TripPrice(models.Model):
    trip_price_id = models.CharField(max_length=100,unique=True,default="POKKATABC123")
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    
    def save(self,*args,**kwargs):
        prefix = f"{self.trip.trip_id}{self.vehicle.registration_number}"
        self.trip_price_id = prefix.upper()
        super().save(*args,**kwargs)
        
    def __str__(self):
        return f"Location for Trip: {self.trip.from_location} to {self.trip.to_location} - Price Id: {self.trip_price_id} - Price: {self.price}"

def generate_ticket_content(booking):
    ticket_content = f"""
        -------------------------------------
        Booking ID: {booking.booking_id}
        Passenger: {booking.passenger.user.username}
        Trip: {booking.tripprice.trip.from_location} to {booking.tripprice.trip.to_location}
        No. of Passengers: {booking.num_passengers}
        Price per Person: {booking.tripprice.price}
        Total Price: {booking.price}
        Trip Date: {booking.tripprice.trip.start_datetime.strftime("%Y-%m-%d %H:%M:%S")}
        Ticket Booked Time: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}
        -------------------------------------
    """
    return ticket_content

class Booking(models.Model):
    booking_id = models.CharField(max_length=200,unique=True,default="passenger2JANKATXYZ1234")
    passenger = models.ForeignKey(Passenger,on_delete=models.CASCADE)
    tripprice = models.ForeignKey(TripPrice,on_delete = models.CASCADE)
    num_passengers = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    
    def clean(self):
        """Custom validation to check available seats before booking."""
        if self.num_passengers > self.tripprice.vehicle.seating_capacity:
            raise ValueError("Not enough seats in this vehicle ")
         
    def save(self,*args,**kwargs):
        self.clean()
        self.price = self.tripprice.price * self.num_passengers
        self.tripprice.vehicle.available_seat -= self.num_passengers
        self.tripprice.vehicle.save()
        
        
        prefix = f"{self.passenger.user.username}_{self.num_passengers}_{self.tripprice.trip_price_id}"
        timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
        self.booking_id = f"{prefix}_{timestamp}".upper()
        super().save(*args,**kwargs)
        
        ticket_content = generate_ticket_content(self)
        filename = f"{self.booking_id}.txt"
        try: 
            ticket_file_path = os.path.join(settings.MEDIA_ROOT,'tickets',filename)
            print("ticket file path",ticket_file_path)
            with open(ticket_file_path,'w') as ticket_file:
                ticket_file.write(ticket_content)
        except Exception as e:
            raise serializers.ValidationError(f"Error creating ticket file: {str(e)}")
        ticket = Ticket.objects.create(booking=self, ticket_file=ticket_file_path)
        ticket.save()

        return ticket
        

    def __str__(self):
        return f"Booking for {self.passenger.user.username} on {self.tripprice.vehicle.registration_number} - {self.tripprice.trip.from_location} to {self.tripprice.trip.to_location}"

class Ticket(models.Model):
    booking = models.OneToOneField(Booking,on_delete=models.CASCADE)
    ticket_file = models.FileField()
    def __str__(self):
        return f"Ticket for {self.booking.tripprice.vehicle.registration_number} - {self.booking.tripprice.trip.from_location} to {self.booking.tripprice.trip.to_location}"


    