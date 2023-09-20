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

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from services.route_calculator import *
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
                    if is_driver:
                        driver = Driver(user=user)
                        driver.save()
                    else:
                        passenger = Passenger(user=user)
                        passenger.save()
                    login(request, user)
                    return redirect('rideshare')  # Redirect to the rideshare page or another page as needed
                else:
                    return HttpResponse('User with this phone number already exists')
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}')
    
    return render(request, 'rideshare.html')

'''
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            phone_number = data.get('phone_number')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            is_driver = data.get('is_driver') == False
            is_passenger = data.get('is_passenger') == False

            if is_driver and phone_number and first_name and last_name:
                if not CustomUser.objects.filter(phone_number=phone_number).exists():
                    user = CustomUser(phone_number=phone_number, first_name=first_name, last_name=last_name)
                    user.save()
                    driver = Driver(user=user)
                    driver.save()   
                    login(request, user)
                    return HttpResponse('Success')  
                else:
                    return HttpResponse('Пользователь с таким именем уже зарегестрирован')  
            if is_passenger and phone_number and first_name and last_name:
                if not CustomUser.objects.filter(phone_number=phone_number).exists():
                    user = CustomUser(phone_number=phone_number, first_name=first_name, last_name=last_name)
                    user.save()
                    passenger = Passenger(user=user)
                    passenger.save()
                    login(request, user)
                    return render(request,'rideshare.html')
                else:
                    return JsonResponse({'error': 'Пользователь с таким именем уже зарегестрирован'})  
        except json.JSONDecodeError:
            return HttpResponse('Invalid JSON data.')
    else:
        return HttpResponse('This is not a POST request.')
'''
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
class RateViewSet(viewsets.ModelViewSet):
    queryset=Rate.objects.all()
    serializer_class = RateSerializer
class DriverLocationViewSet(viewsets.ModelViewSet):
    queryset = DriverLocation.objects.all()
    serializer_class = DriverLocationSerializer
class PassengerLocationViewSet(viewsets.ModelViewSet):
    queryset = PassengerLocation.objects.all()
    serializer_class = PassengerLocationSerializer


@api_view(['POST'])
def order(self, request):
    if request.method == 'POST':
        serializer = RideSerializer(data=request.data)
        try:
            destination_location=request.data.get['destination_location']
            d = route_location()
            RideSerializer.objects.create(passenger=request.user, driver=None,
            departure_location=PassengerLocation.objects.get(user=request.user).values_list('latitude','longitude'),
            destination_location=destination_location, in_process=False, duration = d[1], cost = d[2], emission = d[3])
            return Response({'success': 'Order given successfully. Wait for driver.'}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'error': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def driver_order(self,request):
    if request.method == 'POST':
        serializer = RideSerializer(data=request.data)
        try:
            ride_id=request.data.get['id']
            RideSerializer.objects.update(id=ride_id, driver=user.request, in_process=True)
            return Response({'success': 'Order recieved successfully'}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'error': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdatePassengerLocation(APIView):
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