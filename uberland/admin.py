from django.contrib import admin
from .models import *

admin.site.register(Driver)
admin.site.register(Passenger)
admin.site.register(Ride)
admin.site.register(FinishedRide)
admin.site.register(Class)
admin.site.register(Car)
admin.site.register(CustomUser)
admin.site.register(Rate)
admin.site.register(RecieveRide)
admin.site.register(RequestRide)