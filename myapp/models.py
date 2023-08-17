from django.db import models
from datetime import date

# Create your models here.

class Users(models.Model):
    readonly_fields = ('emp_id','Account_balance')
    emp_id = models.AutoField(primary_key=True, editable=True, auto_created=True)
    emp_name = models.CharField(max_length=255)
    emp_pass = models.CharField(max_length=255)
    emp_addr = models.CharField(max_length=255)
    Account_balance = models.FloatField(editable=False, null=True)
    class Meta:
        db_table = 'User'

    def __str__(self) -> str:
        return self.emp_name
class Locations(models.Model):
    readonly_fields = ('loc_id',)
    loc_id = models.AutoField(primary_key=True, editable=True, auto_created=True)
    loc_name = models.CharField(max_length=255)
    loc_address = models.CharField(max_length=255)
    emp_id = models.IntegerField()
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
    travel_distance = models.FloatField(default=0)
    cost = models.FloatField(default=0)
    fuel =  models.FloatField(default=0)
    travel_date = models.DateField()
    approved = models.BooleanField(default=False)
    class Meta:
        db_table = 'Trips'

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            last_trip = Trips.objects.filter(emp_id=self.emp_id).order_by('-travel_id').first()
            if last_trip:
                self.travel_id = last_trip.travel_id + 1
                self.travel_date = date.today()
            else :
                self.travel_id = 1
                self.travel_date = date.today()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return "emp_id: "+str(self.emp_id)+" "+ ("travel_id: ") + str(self.travel_id)




class Fuel_Prices(models.Model):
    price_fields = ('emp_id','fuel_date')
    price_id = models.AutoField(primary_key=True, editable=True, auto_created=True)
    fuel_type = models.CharField(max_length=255)
    fuel_price = models.IntegerField(default=0)
    fuel_date = models.DateField(max_length=255, editable= False)
    class Meta:
        db_table = 'Fuel_Prices'

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            self.fuel_date = date.today()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.fuel_type
class Reciepts(models.Model):
    reciept_id = models.IntegerField( primary_key=True, editable=False)
    sum_distance = models.IntegerField()
    trips = models.ManyToManyField(Trips)
    emp_id = models.IntegerField()
    dated = models.DateField()
    paid = models.BooleanField(default=False)
    Total_Cost = models.FloatField(null = True)
    No_of_Trips= models.IntegerField(null = True)

    class Meta:
        db_table = 'Reciepts'
    def __str__(self) -> str:
        return str(self.reciept_id)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            last_reciept = Reciepts.objects.order_by('-reciept_id').first()
            print(last_reciept)
            if last_reciept:
                self.reciept_id = last_reciept.reciept_id + 1
            else:
                self.reciept_id = 1
        super().save(*args, **kwargs)