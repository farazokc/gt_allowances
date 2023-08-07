from django.db import models

# Create your models here.

class Users(models.Model):
    emp_id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    emp_name = models.CharField(max_length=255)
    emp_pass = models.CharField(max_length=255)
    emp_addr = models.CharField(max_length=255)
    class Meta:
        db_table = 'User'
    
    def __str__(self) -> str:
        return self.emp_name
class Locations(models.Model):
    loc_id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    loc_name = models.CharField(max_length=255)
    loc_address = models.CharField(max_length=255)
    class Meta:
        db_table = 'Locations'

    def __str__(self) -> str:
        return self.loc_name
class Trips(models.Model):
    travel_id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    emp_id = models.CharField(max_length=255)
    travel_from = models.CharField(max_length=255)
    travel_to = models.CharField(max_length=255)
    travel_return_to = models.CharField(max_length=255)
    travel_distance = models.FloatField()
    cost = models.FloatField()
    fuel =  models.FloatField()
    class Meta:
        db_table = 'Trips'
    
    def __str__(self) -> str:
        return self.travel_id
class Fuel_Prices(models.Model):
    price_id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    fuel_type = models.CharField(max_length=255)
    fuel_price = models.FloatField()
    fuel_date = models.DateField(max_length=255)
    class Meta:
        db_table = 'Fuel_Prices'

    def __str__(self) -> str:
        return self.price_id
    