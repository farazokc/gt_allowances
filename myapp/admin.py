from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Users)
admin.site.register(Locations)
admin.site.register(Trips)
admin.site.register(Fuel_Prices)
admin.site.register(Reciepts)

