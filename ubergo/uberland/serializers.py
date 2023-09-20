from rest_framework import serializers

from .models import *


#serializer for Ride model
class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
    def to_representation(self,instance):
        representation=super().to_representation(instance)
        #includes driver's first name in the representation
        representation['driver']=instance.driver.user.first_name
        #includes passenger's first name in the representation
        representation['passenger']=instance.passenger.user.first_name

        return representation   

#serializer for Driver model
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
    def to_representation(self,instance):
        representation=super().to_representation(instance)
        #includes user's first name in the representation
        representation['user']=instance.user.first_name
        #includes average rating in the representation
        representation['average_rate']=instance.average_rating()
        #includes ride information in the representation
        representation['rides']=instance.rides()
        return representation   

#serializer for Car model
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('car_model','is_eco')
    def to_representation(self,instance):
        representation=super().to_representation(instance)
        #include class name in the representation
        representation['class']=instance.clas.clas
        return representation   

#serializer for Passenger model
class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__' 
    def to_representation(self,instance):
        representation=super().to_representation(instance)
        #includes user's first name in the representation
        representation['user']=instance.user.first_name
        #includes ride information in the representation
        representation['rides']=instance.rides()   
        return representation 

#serializer for Class model
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
#serializer for Rate model
class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        field = '__all__'
#serializer for DriverLocation model
class DriverLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLocation
        fields = ['latitude', 'longitude']
#serializer for PassengerLocation model
class PassengerLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerLocation
        fields = ['latitude', 'longitude']