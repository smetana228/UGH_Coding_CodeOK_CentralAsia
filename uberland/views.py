from .models import *
from .serializers import *

from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from validate_email import validate_email
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.decorators.clickjacking import xframe_options_exempt

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from templates.route_calculator import *
from services.promo_code import daily_promo_code
import random
import string
import datetime

import openrouteservice
from openrouteservice import convert
import folium
from geopy.geocoders import Nominatim

# Initialize geolocator
geolocator = Nominatim(user_agent="aa")

# Initialize the OpenRouteService client with your API key
client = openrouteservice.Client(key='5b3ce3597851110001cf6248959428a4c3da48e38933f1fd8fd5a38f')


def login_view(request):
    error_message=''
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            user_type = request.POST.get('user_type')
            
            if user_type == 'driver':
                is_driver = True
                is_passenger = False
            else:
                is_driver = False
                is_passenger = True

            if phone_number and first_name and last_name:
                if not CustomUser.objects.filter(phone_number=phone_number).exists():
                    user = CustomUser(phone_number=phone_number, first_name=first_name, last_name=last_name)
                    user.save()
                    login(request, user)
                    if is_driver:
                        driver = Driver(user=user)
                        driver.save()
                        return redirect('http://127.0.0.1:8000/car_mod/')
                    else:
                        passenger = Passenger(user=user)
                        passenger.save()
                        return redirect('http://127.0.0.1:8000/request_order/')
                        

                          # Redirect to the rideshare page or another page as needed
                else:
                    error_message = 'User with this phone number already exists'
        except Exception as e:
            error_message = f'Error: {str(e)}'
    
    return render(request, 'register.html', {'error_message': error_message})

def car(request):
    if request.method == 'POST':
        car_model = request.POST.get('car_model')
        is_eco = request.POST.get('eco')
        car = Car(car_model=car_model)
        car.save()
        if is_eco == 'eco':
            car.is_eco=True
        car.save()
        driver=Driver.objects.filter(user=request.user)
        driver.update(car=car)
        return redirect('http://127.0.0.1:8000/recieve_order/')
    return render(request, 'car.html')
@login_required
def logout_view(request):
    user=request.user
    user.delete()
    logout(request)
    return JsonResponse({'success': 'Вы успешно вышли из системы.'})
    
class DriverViewSet(viewsets.ModelViewSet):
    queryset=Driver.objects.all()
    serializer_class=DriverSerializer
class PassengerViewSet(viewsets.ModelViewSet):
    queryset=Passenger.objects.all()
    serializer_class=PassengerSerializer
class CarViewSet(viewsets.ModelViewSet):
    queryset=Car.objects.all()
    serializer_class=CarSerializer
class ClassViewSet(viewsets.ModelViewSet):
    queryset=Class.objects.all()
    serializer_class=ClassSerializer
class RideViewSet(viewsets.ModelViewSet):
    queryset=Ride.objects.all()
    serializer_class=RideSerializer
class RecieveRideViewSet(viewsets.ModelViewSet):
    queryset=RecieveRide.objects.all()
    serializer_class=RecieveRideSerializer
class RequestRideViewSet(viewsets.ModelViewSet):
    queryset=RequestRide.objects.all()
    serializer_class=RequestRideSerializer
class RateViewSet(viewsets.ModelViewSet):
    queryset=Rate.objects.all()
    serializer_class = RateSerializer
class DriverLocationViewSet(viewsets.ModelViewSet):
    queryset = DriverLocation.objects.all()
    serializer_class = DriverLocationSerializer
class PassengerLocationViewSet(viewsets.ModelViewSet):
    queryset = PassengerLocation.objects.all()
    serializer_class = PassengerLocationSerializer



def wait(request):
    request_ride=RequestRide.objects.get(passenger__user=request.user)
    if request_ride.recieved==True:
        return redirect('http://127.0.0.1:8000/passenger_map/')
    return render(request,'wait.html')

@xframe_options_exempt    
def passenger_map(request):
    try:
        recieve_ride=RecieveRide.objects.get(passenger__user=request.user)
    except RecieveRide.DoesNotExist:
        return redirect('http://127.0.0.1:8000/passenger_ride_map/')
    context = {'data':recieve_ride}
    if request.method == "GET":
        cancel = request.GET.get("cancel")
        if cancel == 'cancel': 
            recieve_ride.delete()
            RequestRide.objects.get(passenger=recieve_ride.passenger).delete()
            return redirect('http://127.0.0.1:8000/request_order/')
    return render(request,'passenger_map.html',context)

def driver_map(request):
    try:
        recieve_ride=RecieveRide.objects.get(driver__user=request.user)
        inf=RequestRide.objects.get(passenger=recieve_ride.passenger)
    except RecieveRide.DoesNotExist:
        return redirect('http://127.0.0.1:8000/ride_canceled/')
    context = {'data':recieve_ride}
    if request.method == "GET":
        pick = request.GET.get("pick")
        if pick == 'pick': 
            ride=Ride(passenger=recieve_ride.passenger, driver=recieve_ride.driver, departure_location=recieve_ride.passenger_location,
            destination_location=inf.destination_location, emission=inf.emission, cost=inf.cost, duration=inf.duration)
            ride.save()
            recieve_ride.delete()
            inf.delete()
            return redirect('http://127.0.0.1:8000/driver_ride_map/')
    return render(request, 'driver_map.html',context)

def driver_ride_map(request):
    ride=Ride.objects.get(driver__user=request.user)
    context = {'data':ride}
    if request.method == "GET":
        finish = request.GET.get("finish")
        if finish == 'finish': 
            ride.finished = True
            ride.save()
            return redirect('http://127.0.0.1:8000/driver_ride/')
    return render(request, 'driver_ride_map.html', context)

def passenger_ride_map(request):
    ride=Ride.objects.get(passenger__user=request.user)
    if ride.finished == True:
        return redirect('http://127.0.0.1:8000/passenger_ride/')

    context = {'data':ride}
    return render(request, 'passenger_ride_map.html', context)

def passenger_ride_info(request):
    ride=Ride.objects.get(passenger__user=request.user)
    context = {'data':ride}
    if request.method == "GET":
        rating = request.GET.get("rating")
        rated = request.GET.get("rate")
        if rated == 'rate': 
            ride=Ride.objects.get(passenger=Passenger.objects.get(user=request.user))
            ride.rating = rating
            ride.save()
            finished_ride=FinishedRide(passenger=ride.passenger, driver=ride.driver, departure_location=ride.departure_location,
                destination_location=ride.destination_location, emission=ride.emission, duration=ride.duration, cost=ride.cost, rating=rating)
            finished_ride.save()
            rat=Rate(rating=rating,passenger=Passenger.objects.get(user=request.user),ride=finished_ride)
            rat.save()
            return redirect('http://127.0.0.1:8000/passenger_rides/')
    return render(request, 'passenger_ride.html', context)

def driver_ride_info(request):
    ride=Ride.objects.get(driver__user=request.user)
    context = {'data':ride}
    if request.method == "GET":
        home = request.GET.get("home")
        if home == 'home':
            ride.delete()
            return redirect('http://127.0.0.1:8000/driver_rides/')
    return render(request, 'driver_ride.html', context)


def request_order(request):
    if request.method == 'POST':
        departure_location=request.POST.get('departure')
        destination_location=request.POST.get('destination')
        taxi_type=request.POST.get('taxi-type')
        promo=request.POST.get('promo')
        d = lnlg(departure_location, destination_location)
        c = cost(taxi_type)
        if promo == daily_promo_code:
            с = c-(с/100*30)
        l = route_calculator(coords=d,km_cost=c[0],depart_cost=c[1])
        request=RequestRide(passenger = Passenger.objects.get(user=request.user), 
        departure_location=departure_location, destination_location=destination_location, duration=l[1],cost=l[2],emission=l[3])
        request.save()
        return redirect('http://127.0.0.1:8000/wait/')
    return render(request, 'ridesharing.html')


def recieve_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ride_id = data.get('ride_id')
    if request.method == 'GET':
        ride_id = request.GET.get('ride_id')
    if ride_id:
        requests=RequestRide.objects.get(id=ride_id)
        drive=Driver.objects.get(user=request.user)
        driver_location='Absamat Masaliev'
        d=lnlg(driver_location, requests.departure_location)
        l=driver_calculator(d)
        requests.recieved=True
        requests.save()
        if drive.car.is_eco:
            ride=RecieveRide(driver=Driver.objects.get(user=request.user), driver_location=driver_location, 
            passenger=Passenger.objects.get(user=requests.passenger.user), 
            passenger_location=requests.departure_location, duration=l[1])
            ride.save()
        else:
            ride=RecieveRide(driver=Driver.objects.get(user=request.user), driver_location=driver_location, 
                passenger=Passenger.objects.get(user=requests.passenger.user), 
                passenger_location=requests.departure_location, duration=l[1],emission=l[2])
            ride.save()      
    return render(request, 'requests.html')

def cancel(request):
    if request.method == "GET":
        new = request.GET.get("new")
        if new == 'new': 
            return redirect('http://127.0.0.1:8000/recieve_order/')
    return render(request,'cancel.html')

def driver_rides(request):
    rides=FinishedRide.objects.filter(driver__user=request.user)
    context = {"rides": rides}
    return render(request, 'driver_rides.html', context)

def passenger_rides(request):
    rides=FinishedRide.objects.filter(passenger__user=request.user)
    context = {"rides": rides}
    return render(request, 'passenger_rides.html', context)

class UpdatePassengerLocation(APIView):
    @api_view(['POST'])
    def post(self, request):
        try:
            latitude = request.data.get['latitude']
            longitude = request.data.get['longitude']

            PassengerLocation.objects.update_or_create(user=request.user, defaults={'latitude': latitude, 'longitude': longitude})

            return Response({'message': 'Location updated successfully'}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'message': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class UpdateDriverLocation(APIView):
    def post(self, request):
        try:
            latitude = request.data['latitude']
            longitude = request.data['longitude']

            DriverLocation.objects.update_or_create(user=request.user, defaults={'latitude': latitude, 'longitude': longitude})

            return Response({'message': 'Location updated successfully'}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'message': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def promo_code(request):
    promo_code = {"promo_code": daily_promo_code}
    return render (request, 'promo_code.html', context=promo_code)
