from django.db import models
from account.models import CustomUser
from passenger.models import Passenger
# Create your models here.

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
    
class Vehicle(models.Model):
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
    year = models.IntegerField()
    color = models.CharField(max_length=30)
    seating_capacity = models.PositiveIntegerField(default=0)
    license_plate_number = models.CharField(max_length=10, unique=True)
    insurance_expiry_date = models.DateField()  # Ensure insurance validity
    fitness_certificate_expiry_date = models.DateField()  # Track vehicle fitness
    image = models.ImageField(upload_to='vehicle_images', blank=True)  # Optional image
    available_seat = models.PositiveIntegerField(default=0)
    
    
    def get_booked_seats_by_passennger(self,passenger):
        bookings = Booking.objects.filter(Vehicle=self,user=passenger)
        total_passenger_booked_seats = sum(booking.num_passenger for booking in bookings)
        return total_passenger_booked_seats
    
    
    def __str__(self):
        return f"{self.registration_number} - {self.make} {self.model}"
    


class Trip(models.Model):
    driver = models.ForeignKey(Driver,on_delete=models.CASCADE, related_name = "driver_trips")
    vehicle = models.ForeignKey(Vehicle,on_delete = models.CASCADE, related_name = "vehicle_trips")
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    end_location = models.CharField(max_length=255)
    passenger = models.ManyToManyField(Passenger,related_name='passenger_trips',blank=True)
    
    def __str__(self):
        return f"{self.driver.user.username}'s Trip - {self.start_datetime}"
    

    def save(self,*args,**kwargs):
        booked_seat = Booking.objects.filter(Vehicle=self).count()
        self.vehicle.available_seat = self.vehicle.seating_capacity - booked_seat
        super().save(*args,**kwargs)

class Booking(models.Model):
    user = models.ForeignKey(Passenger,on_delete = models.CASCADE)
    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    num_passenger = models.PositiveBigIntegerField(default=1)
    is_paid = models.BooleanField(default=False)
    booking_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.vehicle.company_made}{self.vehicle.model} - {self.booking_date}  "

class Ticket(models.Model):
    passenger = models.OneToOneField(Passenger,on_delete=models.CASCADE)
    booking = models.OneToOneField(Booking,on_delete = models.CASCADE)
    ticket_file = models.FileField(upload_to='tickets/')
    num_passenger = models.PositiveIntegerField(default=0)
    
    def total_passenger_with_one_ticket(self):
        booked_seat_passenger = self.booking.vehicle.get_booked_seats_by_passennger(self.passenger)
        self.num_passenger = booked_seat_passenger
        self.save()
        