from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

#custom manager for CustomUser
class CustomUserManager(BaseUserManager):
	#create a regular user
    def create_user(self, first_name, last_name, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(first_name=first_name, last_name=last_name, phone_number=phone_number, **extra_fields)
        user.save(using=self._db)
        return user 
    #creates a superuser
    def create_superuser(self, first_name, last_name, phone_number,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(first_name=first_name, last_name=last_name, phone_number=phone_number, **extra_fields)

#custom User model
class CustomUser(AbstractBaseUser, PermissionsMixin):
	#user fields
	first_name = models.CharField(max_length=37)
	last_name = models.CharField(max_length=37,null=True)
	phone_number = PhoneNumberField(null=False, blank=False, unique=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	date_joined = models.DateTimeField(default=timezone.now)

	objects = CustomUserManager()

	USERNAME_FIELD = 'first_name'
	REQUIRED_FIELDS = ['phone_number']
	def __str__(self):
		return self.first_name
    


class Class(models.Model):
	clas = models.CharField(max_length=37)
	take_cost = models.IntegerField()
	km_cost = models.IntegerField()
	
class Car(models.Model):
	car_model = models.CharField(max_length=37)
	is_eco = models.BooleanField(default=False)

class Driver(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
	pfp = models.ImageField(upload_to='driver_pfp', default='no_pfp.jpg')

	#calculates average rating of the driver
	def average_rating(self) -> float:
		r = Rate.objects.filter(ride__driver=self).aggregate(Avg("rating"))["rating__avg"] or 0
		return round(r,1)
	#gets rides associated with the driver
	def rides(self):
		return Ride.objects.filter(ride__driver=self).values_list('passenger__user__first_name')

class Passenger(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	#gets rides associated with the passenger
	def rides(self):
		return Ride.objects.filter(passenger=self).values_list('driver__user__first_name','departure_location','destination_location')


class PassengerLocation(models.Model):
    user = models.OneToOneField(Passenger, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

class DriverLocation(models.Model):
    user = models.OneToOneField(Driver, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

class RequestRide(models.Model):
	passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
	departure_location = models.CharField(max_length=37)
	destination_location = models.CharField(max_length=37)
	emission = models.IntegerField(default=0)
	cost = models.FloatField(default=0)
	duration = models.IntegerField(default=0)
	recieved = models.BooleanField(default=False)

class RecieveRide(models.Model):
	driver = models.CharField(max_length=37)
	driver_location = models.CharField(max_length=37)
	passenger_location = models.CharField(max_length=37)
	passenger = models.CharField(max_length=37)
	duration = models.IntegerField(default=0)
	emission = models.IntegerField(default=0)

class Ride(models.Model):
	passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
	driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
	destination_location = models.CharField(max_length=37)
	emission = models.IntegerField(default=0)
	cost = models.IntegerField(default=0)
	duration = models.IntegerField(default=0)

class Rate(models.Model):
	rating = models.IntegerField(default=0)
	passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=True)
	ride = models.ForeignKey(Ride, on_delete=models.CASCADE, null=True)



