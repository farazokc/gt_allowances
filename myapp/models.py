from django.db import models

# Create your models here.

class Users(models.Model):
    emp_id = models.CharField(primary_key=True, max_length=255, unique=True, editable=False, auto_created=True)
    emp_name = models.CharField(max_length=255)
    emp_pass = models.CharField(max_length=255)
    emp_addr = models.CharField(max_length=255)
    class Meta:
        db_table = 'User'
class Locations(models.Model):
    loc_id = models.AutoField(primary_key=True, unique=True, editable=False, auto_created=True)
    loc_name = models.CharField(max_length=255)
    loc_address = models.CharField(max_length=255)
    class Meta:
        db_table = 'Locations'
class Trips(models.Model):
    travel_id = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=255)
    travel_from = models.CharField(max_length=255)
    travel_to = models.CharField(max_length=255)
    travel_return_to = models.CharField(max_length=255)
    travel_distance = models.FloatField(max_length=255)
    cost = models.FloatField(max_length=255)
    fuel =  models.FloatField(max_length=255)
    class Meta:
        db_table = 'Trips'
class Fuel_Prices(models.Model):
    price_id = models.AutoField(primary_key=True)
    fuel_type = models.CharField(max_length=255)
    fuel_price = models.FloatField(max_length=255)
    fuel_date = models.DateField(max_length=255)
    class Meta:
        db_table = 'Fuel_Prices'
    