from django.db import models

# Create your models here.

class Users(models.Model):
    emp_id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

class Location(models.Model):
    plant_id = models.AutoField(primary_key=True)
    pla = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)