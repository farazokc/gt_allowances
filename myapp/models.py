from django.db import models

# Create your models here.

class Users(models.Model):
    emp_id = models.CharField(primary_key=True, max_length=255)
    emp_name = models.CharField(max_length=255)
    emp_addr = models.CharField(max_length=255)

class Locations(models.Model):
    loc_id = models.AutoField(primary_key=True)
    loc_name = models.CharField(max_length=255)
    loc_address = models.CharField(max_length=255)

class Trips(models.Model):
    travel_id = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=255)
    travel_from = models.CharField(max_length=255)
    travel_to = models.CharField(max_length=255)
    travel_return_to = models.CharField(max_length=255)
    travel_distance = models.FloatField(max_length=255)
    cost = models.FloatField(max_length=255)

class Fuel_Prices(models.Model):
    price_id = models.AutoField(primary_key=True)
    fuel_type = models.CharField(primary_key=True, defualt="Petrol")
    emp_id = models.CharField(max_length=255)
    travel_from = models.CharField(max_length=255)