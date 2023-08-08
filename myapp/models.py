from django.db import models

# Create your models here.

class Users(models.Model):
    readonly_fields = ('emp_id',)
    emp_id = models.AutoField(primary_key=True, editable=True, auto_created=True)
    emp_name = models.CharField(max_length=255)
    emp_pass = models.CharField(max_length=255)
    emp_addr = models.CharField(max_length=255)
    class Meta:
        db_table = 'User'
    
    def __str__(self) -> str:
        return self.emp_name
class Locations(models.Model):
    readonly_fields = ('loc_id',)
    loc_id = models.AutoField(primary_key=True, editable=True, auto_created=True)
    loc_name = models.CharField(max_length=255)
    loc_address = models.CharField(max_length=255)
    class Meta:
        db_table = 'Locations'

    def __str__(self) -> str:
        return self.loc_name
class Trips(models.Model):
    readonly_fields = ('travel_id',)
    trip_number  = models.AutoField(primary_key=True, editable=False)
    travel_id = models.IntegerField( editable=False)
    emp_id = models.IntegerField()
    travel_from = models.CharField(max_length=255)
    travel_to = models.CharField(max_length=255)
    travel_return_to = models.CharField(max_length=255)
    travel_distance = models.FloatField()
    cost = models.FloatField()
    fuel =  models.FloatField()
    class Meta:
        db_table = 'Trips'

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            last_trip = Trips.objects.filter(emp_id=self.emp_id).order_by('-travel_id').first()
            if last_trip:
                print('Hello')
                self.travel_id = last_trip.travel_id + 1
            else :
                print("Worlds")
                self.travel_id = 1
        super().save(*args, **kwargs)
   
    def __str__(self) -> str:
        return self.travel_from
        
class Fuel_Prices(models.Model):
    price_fields = ('emp_id',)

    price_id = models.AutoField(primary_key=True, editable=True, auto_created=True)
    fuel_type = models.CharField(max_length=255)
    fuel_price = models.FloatField()
    fuel_date = models.DateField(max_length=255)
    class Meta:
        db_table = 'Fuel_Prices'

    def __str__(self) -> str:
        return self.price_id
    